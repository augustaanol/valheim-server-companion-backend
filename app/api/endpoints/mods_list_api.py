from fastapi import APIRouter
from app.services.mods_service import enrich_mods

router = APIRouter()


@router.get("/mods-list")
async def mods_list():
    return await enrich_mods()
