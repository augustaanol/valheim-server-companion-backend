from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.db.models.task import TaskStatus, TaskTag


# ===== BASE =====


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = ""
    tag: TaskTag


# ===== CREATE =====


class TaskCreate(TaskBase):
    creator_id: str


# ===== UPDATE (TaskUpdate z frontu) =====


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    tag: Optional[TaskTag] = None


# ===== OUTPUT =====


class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: str

    class Config:
        from_attributes = True


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    creator_id: str
    status: str
    tag: str
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True
