# app/services/server_mod_service.py

import httpx
import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import VALHEIM_HOST_IP, VALHEIM_STATUS_PORT
from app.db.models.server_mod import ServerMod
from app.db.models.thunderstore import ThunderstorePackage
from app.utils.mods_match_utils import normalize, build_index

logger = logging.getLogger(__name__)


async def extract_server_mods():
    url = f"http://{VALHEIM_HOST_IP}:{VALHEIM_STATUS_PORT}/status"

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("bepinex", {}).get("mods", [])
        except Exception as e:
            logger.error(f"Valheim error: {e}")
            return []


async def refresh_server_mods(db: AsyncSession):
    server_mods = await extract_server_mods()

    result = await db.execute(select(ThunderstorePackage))
    packages = result.scalars().all()

    index = build_index(packages)

    await db.execute(delete(ServerMod))

    for mod in server_mods:
        raw_name = mod.get("name", "")
        clean = normalize(raw_name)

        match = index.get(clean)

        if match:
            db.add(
                ServerMod(
                    dll_name=raw_name,
                    matched=True,
                    mod_name=match.name,
                    author=match.owner,
                    latest_version=match.latest_version,
                    url=match.package_url,
                    download_url=match.download_url,
                )
            )
        else:
            db.add(ServerMod(dll_name=raw_name, matched=False))

    await db.commit()