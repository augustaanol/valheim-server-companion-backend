from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.db.models.comment import Comment
from app.schemas.comment import CommentCreate
from app.services.task_events import task_events


async def add_comment(
    db: AsyncSession,
    data: CommentCreate,
) -> Comment:
    comment = Comment(
        task_id=data.task_id,
        content=data.content,
        author_id=data.author_id,
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    await task_events.notify("tasks_updated")

    return comment


async def delete_comment(
    db: AsyncSession,
    comment_id: int,
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    await db.delete(comment)
    await db.commit()

    await task_events.notify("tasks_updated")
