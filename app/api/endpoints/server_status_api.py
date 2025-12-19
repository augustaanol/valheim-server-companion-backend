from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.services.server_status import assemble_server_status
from app.services.player_service import ensure_players_exist

router = APIRouter()


@router.get("/server-status")
async def server_status(db: AsyncSession = Depends(get_db)):

    result = await assemble_server_status(db)

    return result
