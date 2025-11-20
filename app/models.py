from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PlayerLog(Base):
    __tablename__ = "player_logs"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True)
    action = Column(String)
    timestamp = Column(DateTime)
