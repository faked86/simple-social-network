from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_models import Post, Vote
from src.utils_classes import VoteType


async def get_post_from_db(post_id: int, db: AsyncSession) -> Post:
    db_query = select(Post).where(Post.id == post_id)
    res = await db.execute(db_query)
    return res.scalars().first()


async def get_vote_count_from_db(
    vote_type: VoteType, post: Post, db: AsyncSession
) -> int:
    query_likes = select(func.count(Vote.user_id)).where(
        Vote.post_id == post.id, Vote.vote_type == vote_type
    )
    res = await db.execute(query_likes)
    return res.scalars().first()


async def update_votes(post: Post, db: AsyncSession) -> None:
    post.like_count = await get_vote_count_from_db(VoteType.LIKE, post, db)
    post.dislike_count = await get_vote_count_from_db(VoteType.DISLIKE, post, db)


async def get_user_vote_from_db(
    user_id: int, post: Post, db: AsyncSession
) -> VoteType | None:
    db_query = select(Vote).where(Vote.post_id == post.id, Vote.user_id == user_id)
    res = await db.execute(db_query)
    vote: Vote = res.scalars().first()
    if vote:
        return vote.vote_type
    return None


async def update_voted_by_user(user_id: int, post: Post, db: AsyncSession) -> None:
    vote_type = await get_user_vote_from_db(user_id, post, db)
    post.voted = vote_type


async def update_post_for_user(user_id: int, post: Post, db: AsyncSession) -> None:
    await update_votes(post, db)
    await update_voted_by_user(user_id, post, db)
