from fastapi import APIRouter
from app.services.server_status import assemble_server_status

router = APIRouter()


@router.get("/server_status")
async def server_status():
    return await assemble_server_status()
