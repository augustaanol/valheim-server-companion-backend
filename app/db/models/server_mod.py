# app/db/models/server_mod.py

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.db.models.base import Base

class ServerMod(Base):
    __tablename__ = "server_mods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dll_name = Column(String, index=True)
    matched = Column(Boolean)
    mod_name = Column(String)
    author = Column(String)
    latest_version = Column(String)
    url = Column(String)
    download_url = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)