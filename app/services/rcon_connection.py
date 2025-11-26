from rcon.source import rcon
from app.config import (
    VALHEIM_HOST_IP,
    VALHEIM_RCON_PORT,
    VALHEIM_RCON_PASSWORD
)

async def rcon_command(command: str, *args):
    response = await rcon(
        command, 
        *args,   # przekazuje tylko istniejące argumenty
        host=VALHEIM_HOST_IP,
        port=VALHEIM_RCON_PORT,
        passwd=VALHEIM_RCON_PASSWORD
    )
    print(response)
    return response