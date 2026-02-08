import httpx
from app.config import (
    VALHEIM_HOST_IP,
    VALHEIM_STATUS_PORT,
    PORTAINER_URL,
    PORTAINER_TOKEN,
    PORTAINER_CONTAINER_NAME,
    PORTAINER_ENDPOINT_ID,
)
from app.services.rcon_connection import rcon_command
from app.utils.parse_players import parse_players
from app.services.player_service import get_players
from sqlalchemy.ext.asyncio import AsyncSession


async def get_valheim_status():
    url = f"http://{VALHEIM_HOST_IP}:{VALHEIM_STATUS_PORT}/status"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except (httpx.RequestError, httpx.HTTPStatusError):
            return None  # status.json niedostępny


async def get_portainer_container_status():
    headers = {"X-API-Key": PORTAINER_TOKEN}
    async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
        try:
            url = f"{PORTAINER_URL}/api/endpoints/{PORTAINER_ENDPOINT_ID}/docker/containers/json?all=1"
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            containers = response.json()
            for container in containers:
                if any(
                    f"/{PORTAINER_CONTAINER_NAME}" == name
                    for name in container["Names"]
                ):
                    return container["State"]  # np. "running", "exited"
            return "not_found"
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print("Portainer API error:", e)
            return "error"


async def getServerStatus():
    container_status = await get_portainer_container_status()
    valheim_status = await get_valheim_status()

    # Ustalenie server_status
    if container_status != "running":
        server_status = "offline"
    elif valheim_status is None:
        server_status = "starting"
    else:
        server_status = "online"

    return server_status, valheim_status


async def assemble_server_status(db: AsyncSession):
    status = await getServerStatus()
    server_status = status[0]
    valheim_status = status[1]

    result = {
        "server_name": valheim_status.get("server_name") if valheim_status else None,
        "server_status": server_status,
        "steam_id": valheim_status.get("steam_id") if valheim_status else None,
        "player_count": valheim_status.get("player_count") if valheim_status else 0,
        "active_players": (
            parse_players(await rcon_command("players"))
            if server_status == "online"
            else []
        ),
        "all_players": await get_players(db),
    }

    return result
