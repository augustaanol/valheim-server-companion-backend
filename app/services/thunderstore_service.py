# app/services/thunderstore_service.py

import httpx
import logging
from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import THUNDERSTORE_API
from app.db.models.thunderstore import ThunderstorePackage

logger = logging.getLogger(__name__)


async def fetch_thunderstore_packages():
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(THUNDERSTORE_API)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else data.get("results", [])


async def refresh_thunderstore_cache(db: AsyncSession):
    logger.info("Refreshing Thunderstore cache...")

    packages = await fetch_thunderstore_packages()

    await db.execute(delete(ThunderstorePackage))

    for pkg in packages:
        versions = pkg.get("versions", [])
        latest = versions[0] if versions else {}

        db.add(
            ThunderstorePackage(
                full_name=pkg.get("full_name"),
                name=pkg.get("name"),
                owner=pkg.get("owner"),
                latest_version=latest.get("version_number"),
                package_url=pkg.get("package_url"),
                download_url=latest.get("download_url"),
                raw_data=pkg,
                updated_at=datetime.utcnow(),
            )
        )

    await db.commit()