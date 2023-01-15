from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...external.db.models import Post, Vote
from ...utils_classes import VoteType


async def update_vote_count(post: Post, db: AsyncSession) -> None:
    query_likes = select(func.count(Vote.user_id).label("like_count")).where(
        Vote.post_id == post.id, Vote.vote_type == VoteType.LIKE
    )
    res = await db.execute(query_likes)
    like_count = res.scalars().first()
    post.like_count = like_count

    query_dislikes = select(func.count(Vote.user_id).label("dislike_count")).where(
        Vote.post_id == post.id, Vote.vote_type == VoteType.DISLIKE
    )
    res = await db.execute(query_dislikes)
    dislike_count = res.scalars().first()
    post.dislike_count = dislike_count


async def get_post_from_db(post_id: int, db: AsyncSession) -> Post:
    db_query = select(Post).where(Post.id == post_id)
    res = await db.execute(db_query)
    return res.scalars().first()
