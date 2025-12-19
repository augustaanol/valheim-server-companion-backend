from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import (
    create_task,
    get_tasks,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_endpoint(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Tworzy nowe zadanie.
    ZWRACA DTO (TaskOut), a nie ORM.
    comments zawsze = [] (brak lazy load).
    """
    task = await create_task(db, data)
    return task


@router.get(
    "",
    response_model=List[TaskOut],
)
async def get_tasks_endpoint(
    db: AsyncSession = Depends(get_db),
):
    """
    Pobiera listę tasków.
    Service MUSI zadbać o eager load lub mapowanie do DTO.
    """
    tasks = await get_tasks(db)
    return tasks


@router.patch(
    "/{task_id}",
    response_model=TaskOut,
)
async def update_task_endpoint(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Aktualizuje task.
    Zwraca TaskOut (bez lazy-loadowanych relacji).
    """
    task = await update_task(db, task_id, data)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task_endpoint(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Usuwa task.
    Brak body w odpowiedzi (204).
    """
    await delete_task(db, task_id)
