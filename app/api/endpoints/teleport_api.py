from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rcon_connection import rcon_command

router = APIRouter()


class TeleportPayload(BaseModel):
    data: str  # np. "steamid x y z"


@router.post("/teleport")
async def teleport_player(payload: TeleportPayload):
    try:
        command = f"teleport {payload.data}"

        response = await rcon_command(command)

        return {"success": True, "command": command, "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
