from enum import Enum


class VoteType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
