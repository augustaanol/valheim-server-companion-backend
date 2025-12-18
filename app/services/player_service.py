from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.db.models.player import Player
from app.schemas.player import PlayerCreate


async def get_players(db: AsyncSession) -> list[Player]:
    result = await db.execute(select(Player).order_by(Player.name))
    return result.scalars().all()


async def create_player(db: AsyncSession, data: PlayerCreate) -> Player:
    # sprawdzenie unikalności steam_id
    result = await db.execute(select(Player).where(Player.steam_id == data.steam_id))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=409, detail="Player with this steam_id already exists"
        )

    player = Player(
        name=data.name,
        steam_id=data.steam_id,
    )

    db.add(player)
    await db.commit()
    await db.refresh(player)

    return player


async def ensure_players_exist(
    db: AsyncSession,
    players: list[dict],
) -> None:
    """
    Automatycznie dodaje nowych graczy wykrytych na serwerze.
    Identyfikacja po steam_id.
    Funkcja jest idempotentna (można wołać wielokrotnie).
    """
    if not players:
        return

    # Wyciągnij steam_id
    steam_ids = [p["steam_id"] for p in players if p.get("steam_id")]

    if not steam_ids:
        return

    # Pobierz już istniejących graczy
    result = await db.execute(
        select(Player.steam_id).where(Player.steam_id.in_(steam_ids))
    )
    existing_steam_ids = set(result.scalars().all())

    # Przygotuj nowych
    new_players = [
        Player(
            name=p["name"],
            steam_id=p["steam_id"],
        )
        for p in players
        if (p.get("steam_id") not in existing_steam_ids and p.get("name"))
    ]

    if not new_players:
        return

    db.add_all(new_players)
    await db.commit()
