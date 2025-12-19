from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.comment import CommentCreate, CommentOut
from app.services.comment_service import (
    add_comment,
    delete_comment,
)

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_comment_endpoint(
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await add_comment(db, data)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment_endpoint(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    await delete_comment(db, comment_id)
