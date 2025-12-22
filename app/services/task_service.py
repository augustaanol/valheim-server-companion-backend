from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.db.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_events import task_events


async def create_task(db: AsyncSession, data: TaskCreate):
    task = Task(
        title=data.title,
        description=data.description,
        tag=data.tag,
        creator_id=data.creator_id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    # 🔥 PONOWNIE POBIERAMY TASKA JAK W GET
    result = await db.execute(
        select(Task)
        .where(Task.id == task.id)
        .options(
            selectinload(Task.comments),
        )
    )

    await task_events.notify("tasks_updated")

    return result.scalar_one()


async def get_tasks(db: AsyncSession) -> list[Task]:
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.comments))  # 🔥 KLUCZ
        .order_by(Task.created_at.desc())
    )
    return result.scalars().all()


async def update_task(
    db: AsyncSession,
    task_id: int,
    data: TaskUpdate,
) -> Task:
    task = await db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await db.commit()

    # 🔁 RE-FETCH Z RELACJAMI
    result = await db.execute(
        select(Task).options(selectinload(Task.comments)).where(Task.id == task_id)
    )

    await task_events.notify("tasks_updated")

    return result.scalar_one()


async def delete_task(
    db: AsyncSession,
    task_id: int,
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    await task_events.notify("tasks_updated")
