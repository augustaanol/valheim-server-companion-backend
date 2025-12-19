from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    func,
)
from sqlalchemy.orm import relationship
from app.db.models.base import Base
import enum


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in-progress"
    done = "done"


class TaskTag(str, enum.Enum):
    important = "important"
    normal = "normal"
    backlog = "backlog"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator_id = Column(String(32), nullable=False)

    status = Column(
        Enum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.todo,
    )

    tag = Column(
        Enum(TaskTag, name="task_tag"),
        nullable=False,
        default=TaskTag.normal,
    )

    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="Comment.created_at",
    )
