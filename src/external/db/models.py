from loguru import logger
from sqlalchemy import Column, Enum, ForeignKey, func, Integer, String, TIMESTAMP
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.orm import Mapped, relationship

from ...utils_classes import VoteType
from .session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner: "User" = relationship("User", back_populates="posts")
    votes: list["Vote"] = relationship(
        "Vote",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @property
    def like_count(self) -> int:
        try:
            return sum(
                map(
                    lambda x: True if x.vote_type is VoteType.LIKE else False,
                    self.votes,
                )
            )
        except MissingGreenlet:
            logger.warning("Likes can't be loaded. MissingGreenlet error.")
            return 0

    @property
    def dislike_count(self) -> int:
        try:
            return sum(
                map(
                    lambda x: True if x.vote_type is VoteType.DISLIKE else False,
                    self.votes,
                )
            )
        except MissingGreenlet:
            logger.warning("Dislikes can't be loaded. MissingGreenlet error.")
            return 0


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    vote_type = Column(Enum(VoteType), nullable=False)
