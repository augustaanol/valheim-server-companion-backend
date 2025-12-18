from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.db.models.base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    steam_id: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False
    )
