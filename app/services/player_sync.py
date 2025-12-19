import asyncio
from app.db.session import AsyncSessionLocal
from app.services.player_service import ensure_players_exist
from app.utils.parse_players import parse_players
from app.services.rcon_connection import rcon_command


async def sync_players_loop():
    while True:
        try:
            async with AsyncSessionLocal() as db:
                raw = await rcon_command("players")
                players = parse_players(raw)
                await ensure_players_exist(db, players)
        except Exception as e:
            print("Player sync error:", e)

        await asyncio.sleep(30)
