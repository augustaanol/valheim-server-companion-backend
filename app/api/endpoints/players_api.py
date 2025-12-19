from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.player import PlayerOut
from app.services.player_service import get_players

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[PlayerOut])
async def list_players(db: AsyncSession = Depends(get_db)):
    return await get_players(db)
