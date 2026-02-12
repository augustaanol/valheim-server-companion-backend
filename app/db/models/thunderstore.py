# app/db/models/thunderstore.py

from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.db.models.base import Base

class ThunderstorePackage(Base):
    __tablename__ = "thunderstore_packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, index=True)
    name = Column(String, index=True)
    owner = Column(String, index=True)
    latest_version = Column(String)
    package_url = Column(String)
    download_url = Column(String)
    raw_data = Column(JSON)  # opcjonalnie
    updated_at = Column(DateTime, default=datetime.utcnow)