from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.external.db.models import Post, Vote
from src.utils_classes import VoteType
from src.api.posts.schemas import PostIn
from src.api.posts.utils import get_post_from_db, update_post_for_user


async def create_post(user_id: int, post_in: PostIn, db: AsyncSession) -> Post:
    """Creates user's post in 'db'."""
    new_post = Post(content=post_in.content, owner_id=user_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    await update_post_for_user(user_id, new_post, db)
    return new_post


async def get_all_posts(
    query: str | None, offset: int, limit: int, user_id: int, db: AsyncSession
) -> list[Post]:
    """
    Retrieves all posts from db filtered by 'query', offsetted and limited from 'db'.
    """
    db_query = (
        select(Post)
        .filter(Post.content.contains(query))
        .order_by(desc(Post.created_at))
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(db_query)
    posts = res.scalars().all()

    for post in posts:
        await update_post_for_user(user_id, post, db)

    return posts


async def get_single_post(user_id: int, post_id: int, db: AsyncSession) -> Post:
    """Retrieves one post by 'post_id' from 'db'."""
    post = await get_post_from_db(post_id, db)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")

    await update_post_for_user(user_id, post, db)
    return post


async def delete_post(post_id: int, user_id: int, db: AsyncSession) -> None:
    """Deletes post by 'post_id' and 'user_id' from 'db'."""
    post = await get_post_from_db(post_id, db)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")
    if post.owner_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "It's not your post.")

    await db.delete(post)
    await db.commit()


async def update_post(
    post_id: int, new_post: PostIn, user_id: int, db: AsyncSession
) -> Post:
    """Updates post by 'post_id' and 'user_id' in 'db'."""
    post = await get_post_from_db(post_id, db)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")
    if post.owner_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "It's not your post.")

    post.content = new_post.content
    post.updated_at = datetime.utcnow().astimezone()

    await db.commit()

    await update_post_for_user(user_id, post, db)
    return post


async def vote_post(vote_type: VoteType, user_id: int, post_id: int, db: AsyncSession):
    """
    Leaves vote for post in 'db'.

    If opposite vote exists then updates vote.
    If same vote exists then discards.
    """
    post = await get_post_from_db(post_id, db)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")
    if post.owner_id == user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "It's your post.")

    query = select(Vote).where(Vote.post_id == post_id, Vote.user_id == user_id)
    res = await db.execute(query)
    vote_old: Vote = res.scalars().first()

    if vote_old:

        if vote_old.vote_type != vote_type:
            vote_old.vote_type = vote_type
            await db.commit()
            return

        await db.delete(vote_old)
        await db.commit()
        return

    vote_new = Vote(post_id=post_id, user_id=user_id, vote_type=vote_type)
    db.add(vote_new)
    await db.commit()
