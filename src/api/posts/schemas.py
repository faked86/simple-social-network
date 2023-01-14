from datetime import datetime

from pydantic import BaseModel

from ...utils_classes import VoteType


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


class VoteIn(BaseModel):
    vote_type: VoteType


class VoteOut(BaseModel):
    post_id: int
    user_id: int
    vote_type: VoteType

    class Config:
        orm_mode = True
