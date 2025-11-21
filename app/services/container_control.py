import httpx
from app.config import (
    PORTAINER_URL,
    PORTAINER_TOKEN,
    PORTAINER_CONTAINER_NAME,
    PORTAINER_ENDPOINT_ID,
)


async def control_portainer_container(action: str):
    headers = {"X-API-Key": PORTAINER_TOKEN}
    url = f"{PORTAINER_URL}/api/endpoints/{PORTAINER_ENDPOINT_ID}/docker/containers/{PORTAINER_CONTAINER_NAME}/"

    if action == "start":
        url += "start"
    elif action == "stop":
        url += "stop"
    else:
        raise ValueError("Invalid action, must be 'start' or 'stop'")

    async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
        try:
            response = await client.post(url, headers=headers)
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            print("Portainer control error:", e)
            return False
