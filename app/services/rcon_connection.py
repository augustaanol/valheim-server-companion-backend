from rcon.source import rcon
from app.config import (
    VALHEIM_HOST_IP,
    VALHEIM_RCON_PORT,
    VALHEIM_RCON_PASSWORD
)

async def rcon_connection():
    response = await rcon(
        'some_command', 'with', 'some', 'arguments',
        host=VALHEIM_HOST_IP, port=VALHEIM_RCON_PORT, passwd=VALHEIM_RCON_PASSWORD
    )
    print(response)