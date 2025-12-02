from fastapi import APIRouter
from app.services.container_resources import get_container_resources

router = APIRouter()


@router.get("/container-resources/{container_name}")
async def container_resources(container_name: str):
    """
    Zwraca statystyki CPU/RAM kontenera Docker.
    """
    return get_container_resources(container_name)
