from fastapi import APIRouter
from app.services.server_stats import assemble_server_stats

router = APIRouter()


@router.get("/server-stats")
async def server_stats():
    return await assemble_server_stats()
