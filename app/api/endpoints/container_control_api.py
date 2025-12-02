from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.container_control import control_portainer_container

router = APIRouter()


class ContainerActionRequest(BaseModel):
    action: str  # "start" | "stop"


@router.post("/container-control")
async def container_status(request: ContainerActionRequest):
    success = await control_portainer_container(request.action)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to control container")
    return {"success": True, "action": request.action}
