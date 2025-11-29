from app.services.rcon_connection import rcon_command
import re


def extract_day_number(text: str) -> int | None:
    match = re.search(r"Day:\s*(\d+)", text)
    if match:
        return str(match.group(1))
    return None


async def assemble_server_stats():
    result = {
        "stats": [
            {"name": "Day", "value": extract_day_number(await rcon_command("time"))},
        ]
    }

    return result
