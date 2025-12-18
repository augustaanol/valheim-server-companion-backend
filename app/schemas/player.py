from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    steam_id: str = Field(min_length=5, max_length=32)


class PlayerOut(BaseModel):
    id: int
    name: str
    steam_id: str

    model_config = {"from_attributes": True}
