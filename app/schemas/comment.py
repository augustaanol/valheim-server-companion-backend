from datetime import datetime
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    task_id: int
    author_id: str


class CommentOut(CommentBase):
    id: int
    created_at: datetime
    author_id: str

    class Config:
        from_attributes = True
