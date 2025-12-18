from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.db.models.player import Player
from app.schemas.player import PlayerCreate


async def get_players(db: AsyncSession) -> list[Player]:
    result = await db.execute(
        select(Player).order_by(Player.name)
    )
    return result.scalars().all()


async def create_player(db: AsyncSession, data: PlayerCreate) -> Player:
    # sprawdzenie unikalności steam_id
    result = await db.execute(
        select(Player).where(Player.steam_id == data.steam_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Player with this steam_id already exists")

    player = Player(
        name=data.name,
        steam_id=data.steam_id,
    )

    db.add(player)
    await db.commit()
    await db.refresh(player)

    return player
