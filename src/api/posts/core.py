from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils_classes import VoteType

from ...external.db.models import Post, Vote
from .schemas import PostIn, VoteIn


async def create_post(user_id: int, post_in: PostIn, db: AsyncSession) -> Post:
    """Creates user's post in 'db'."""
    new_post = Post(content=post_in.content, owner_id=user_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


async def get_all_posts(
    query: str | None, offset: int, limit: int, db: AsyncSession
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
        .options(selectinload(Post.votes))
    )
    res = await db.execute(db_query)
    posts = res.scalars().all()

    return posts


async def get_single_post(post_id: int, db: AsyncSession) -> Post:
    """Retrieves one post by 'post_id' from 'db'."""
    db_query = select(Post).where(Post.id == post_id).options(selectinload(Post.votes))
    res = await db.execute(db_query)
    post = res.scalars().first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")

    return post


async def delete_post(post_id: int, user_id: int, db: AsyncSession) -> None:
    """Deletes post by 'post_id' and 'user_id' from 'db'."""
    db_query = select(Post).where(Post.id == post_id).options(selectinload(Post.votes))
    res = await db.execute(db_query)
    post: Post = res.scalars().first()

    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")
    if post.owner_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "It's not your post.")

    await db.delete(post)
    await db.commit()


async def update_post(
    post_id: int, new_post: PostIn, user_id: int, db: AsyncSession
) -> Post:
    """Updates post by 'post_id' and 'user_id' in 'db'."""
    db_query = select(Post).where(Post.id == post_id).options(selectinload(Post.votes))
    res = await db.execute(db_query)
    post: Post = res.scalars().first()

    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")
    if post.owner_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "It's not your post.")

    post.content = new_post.content
    post.updated_at = datetime.utcnow().astimezone()

    await db.commit()

    return post


async def vote_post(
    vote_in: VoteIn, user_id: int, post_id: int, db: AsyncSession
) -> Vote | None:
    """Leave vote for post in 'db'."""
    db_query = select(Post).where(Post.id == post_id)
    res = await db.execute(db_query)
    post: Post = res.scalars().first()

    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such post.")
    if post.owner_id == user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "It's your post.")

    query = select(Vote).where(Vote.post_id == post_id and Vote.user_id == user_id)
    res = await db.execute(query)
    vote_old: Vote = res.scalars().first()

    if vote_old is not None:

        if vote_in.vote_type is VoteType.NEUTRAL:
            await db.delete(vote_old)
            await db.commit()
            return None

        vote_old.vote_type = vote_in.vote_type
        await db.commit()
        return vote_old

    if vote_in.vote_type is VoteType.NEUTRAL:
        return None

    vote_new = Vote(post_id=post_id, user_id=user_id, vote_type=vote_in.vote_type)
    db.add(vote_new)
    await db.commit()
    await db.refresh(vote_new)

    return vote_new
