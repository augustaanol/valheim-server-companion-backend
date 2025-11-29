from fastapi import APIRouter
from app.services.rcon_connection import rcon_command

router = APIRouter()


@router.get("/rcon")
async def server_status():
    responses = []
    responses.append(await rcon_command("serverStats"))
    responses.append(await rcon_command("currentEvent"))
    responses.append(await rcon_command("eventsList"))
    responses.append(await rcon_command("players"))
    responses.append(await rcon_command("findPlayer 76561198271197381"))
    return responses
