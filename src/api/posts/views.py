from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_models import PostIn, PostOutForUser
from src.db.session import get_session
from src.oauth2.core import get_current_user
from src.utils_classes import VoteType
from src.api.posts.core import (
    create_post,
    delete_post,
    vote_post,
    update_post,
    get_all_posts,
    get_single_post,
)


posts_router = APIRouter(prefix="/posts", tags=["Posts"])


# Not using common_responses because mypy does not allow it
# common_responses = {401: {"description": "Could not validate credentials"}}


@posts_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PostOutForUser,
    responses={401: {"description": "Could not validate credentials"}},
)
async def create_post_view(
    post: PostIn,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Create user's post."""
    return await create_post(user_id, post, db)


@posts_router.get(
    "",
    response_model=list[PostOutForUser],
    responses={401: {"description": "Could not validate credentials"}},
)
async def get_all_posts_view(
    query: str = "",
    offset: int = 0,
    limit: int = 10,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Retrieve all posts from db filtered by 'query', offsetted and limited."""
    return await get_all_posts(query, offset, limit, user_id, db)


@posts_router.get(
    "/{post_id}",
    response_model=PostOutForUser,
    responses={
        401: {"description": "Could not validate credentials"},
        404: {"description": "No such post."},
    },
)
async def get_single_post_view(
    post_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Retrieve one post by 'post_id'."""
    return await get_single_post(user_id, post_id, db)


@posts_router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "Could not validate credentials"},
        403: {"description": "It's not your post."},
        404: {"description": "No such post."},
    },
)
async def delete_post_view(
    post_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Delete post by 'post_id' and 'user_id'."""
    await delete_post(post_id, user_id, db)


@posts_router.patch(
    "/{post_id}",
    response_model=PostOutForUser,
    responses={
        401: {"description": "Could not validate credentials"},
        403: {"description": "It's not your post."},
        404: {"description": "No such post."},
    },
)
async def update_post_view(
    post_id: int,
    new_post: PostIn,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """Update post by 'post_id' and 'user_id'."""
    return await update_post(post_id, new_post, user_id, db)


@posts_router.post(
    "/{post_id}/{vote_type}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "Could not validate credentials"},
        403: {"description": "It's your post."},
        404: {"description": "No such post."},
    },
)
async def vote_post_view(
    vote_type: VoteType,
    post_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Vote for post.

    If opposite vote exists then updates vote.
    If same vote exists then discards.
    """
    await vote_post(vote_type, user_id, post_id, db)
