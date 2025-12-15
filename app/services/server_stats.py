from app.services.rcon_connection import rcon_command
import re


def extract_day_number(text: str):
    if not text:
        return None
    match = re.search(r"Day:\s*(\d+)", text)
    return int(match.group(1)) if match else None


async def assemble_server_stats():
    result = {
        "server_stats": [
            {"name": "Day", "value": extract_day_number(await rcon_command("time"))},
        ]
    }

    return result
