from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.server_mod import ServerMod
from app.services.thunderstore_service import refresh_thunderstore_cache
from app.services.server_mod_service import refresh_server_mods

router = APIRouter(prefix="/mods", tags=["Mods"])


@router.get("/")
async def get_mods(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ServerMod))
    return result.scalars().all()


@router.post("/refresh")
async def manual_refresh(db: AsyncSession = Depends(get_db)):
    await refresh_thunderstore_cache(db)
    await refresh_server_mods(db)
    return {"status": "ok"}