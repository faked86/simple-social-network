from datetime import datetime

from pydantic import BaseModel


class PostIn(BaseModel):
    content: str


class PostOut(BaseModel):
    id: int
    content: str
    owner_id: int
    like_count: int
    dislike_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
