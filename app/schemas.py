from pydantic import BaseModel
from datetime import datetime


class PlayerLogCreate(BaseModel):
    player_name: str
    action: str
    timestamp: datetime
