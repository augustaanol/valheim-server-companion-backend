from rcon.source import rcon
from app.config import VALHEIM_HOST_IP, VALHEIM_RCON_PORT, VALHEIM_RCON_PASSWORD


async def rcon_command(command: str, *args):
    try:
        response = await rcon(
            command,
            *args,
            host=VALHEIM_HOST_IP,
            port=VALHEIM_RCON_PORT,
            passwd=VALHEIM_RCON_PASSWORD,
        )

        # RCON czasem zwraca None – zamieniamy na pusty string,
        # dzięki czemu regex nie wywali backendu
        return response or ""

    except Exception as e:
        print(f"❌ RCON ERROR ({command}): {e}")
        return f"❌ RCON ERROR ({command}): {e}"  # zawsze zwróć string, żeby backend się nie wysypał
