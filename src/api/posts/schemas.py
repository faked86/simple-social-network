from datetime import datetime

from pydantic import BaseModel

from src.utils_classes import VoteType


class PostIn(BaseModel):
    content: str


class PostOutForUser(BaseModel):
    id: int
    content: str
    owner_id: int
    voted: VoteType | None
    like_count: int
    dislike_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
