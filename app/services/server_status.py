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
import re
from math import floor


def parse_players(text: str):
    players = []

    # Podziel po liniach, pomijając pierwszą (Online X)
    lines = text.strip().split("\n")[1:]

    for line in lines:
        player = {}

        # Name = pierwsze słowo w linii
        match_name = re.match(r"(\S+)\s", line)
        if match_name:
            player["name"] = match_name.group(1)

        # Steam ID
        match_steam = re.search(r"Steam ID:(\d+)", line)
        if match_steam:
            player["steam_id"] = match_steam.group(1)

        # Position (x y z)
        match_pos = re.search(
            r"Position:\s*\(([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\)", line
        )
        if match_pos:
            player["position"] = (
                float(match_pos.group(1)),
                float(match_pos.group(2)),
                float(match_pos.group(3)),
            )

        # Rotation (0,16)
        match_rot = re.search(r"Position:.*\)\((\d+),(\d+)\)", line)
        if match_rot:
            player["rotation"] = (
                float(match_rot.group(1)),
                float(match_rot.group(2)),
            )

        # Player ID
        match_pid = re.search(r"Player ID:(\d+)", line)
        if match_pid:
            player["player_id"] = int(match_pid.group(1))

        # HP
        match_hp = re.search(r"HP:([-\d\.]+)/([-\d\.]+)", line)
        if match_hp:
            player["hp"] = (
                int(float(match_hp.group(1))),
                int(float(match_hp.group(2))),
            )

        players.append(player)

    return players


async def get_valheim_status():
    url = f"http://{VALHEIM_HOST_IP}:{VALHEIM_STATUS_PORT}/status.json"
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


async def assemble_server_status():
    container_status = await get_portainer_container_status()
    valheim_status = await get_valheim_status()

    # Ustalenie server_status
    if container_status != "running":
        server_status = "offline"
    elif valheim_status is None:
        server_status = "starting"
    else:
        server_status = "online"

    result = {
        "server_name": valheim_status.get("server_name") if valheim_status else None,
        "server_status": server_status,
        "steam_id": valheim_status.get("steam_id") if valheim_status else None,
        "player_count": valheim_status.get("player_count") if valheim_status else 0,
        "players": (
            parse_players(await rcon_command("players"))
            if server_status == "online"
            else []
        ),
    }

    return result
