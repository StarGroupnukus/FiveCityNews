from datetime import UTC, datetime
from typing import Annotated

from app.core import db_helper
from app.core.auth import dependencies
from app.core.exceptions.http_exceptions import NotFoundException
from app.core.logger import logging
from app.crud.crud_posts import crud_posts
from app.crud.crud_users import crud_users
from app.schemas.post import (
    PostCreate,
    PostCreateInternal,
    PostRead,
    PostUpdate,
    PostUpdateInternal,
)
from app.schemas.user import UserRead
from fastapi import APIRouter, Depends, Request, status
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import rate_limiter

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/{username}/list",
    response_model=PaginatedListResponse[PostRead],
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    tags=["Admin"],
)
async def get_user_posts(
    request: Request,
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    page: int = 1,
    items_per_page: int = 10,
):
    logger.info(f"Fetching posts for user {username}, page {page}")  # Add logging
    user = await crud_users.get(
        db=session,
        schema_to_select=UserRead,
        username=username,
        is_deleted=False,
    )
    if not user:
        raise NotFoundException("User not found")

    posts_data = await crud_posts.get_multi(
        db=session,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=PostRead,
        created_by_user_id=user["id"],
        is_deleted=False,
    )
    response = paginated_response(
        crud_data=posts_data,
        page=page,
        items_per_page=items_per_page,
    )
    logger.info("Cache miss - executing database query")  # Add logging
    return response


@router.get("/list", response_model=PaginatedListResponse[PostRead])
async def get_my_posts(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    page: int = 1,
    items_per_page: int = 10,
    current_user: UserRead = Depends(dependencies.get_current_active_auth_user),
):
    posts_data = await crud_posts.get_multi(
        db=session,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=PostRead,
        created_by_user_id=current_user.id,
        is_deleted=False,
    )

    response = paginated_response(
        crud_data=posts_data,
        page=page,
        items_per_page=items_per_page,
    )
    return response


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter)],
)
async def create_my_post(
    post: PostCreate,
    current_user: Annotated[UserRead, Depends(dependencies.get_current_active_auth_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    post_internal_dict = post.model_dump()
    post_internal_dict["created_by_user_id"] = current_user["id"]

    post_internal = PostCreateInternal(**post_internal_dict)
    created_post: PostRead = await crud_posts.create(
        db=session,
        object=post_internal,
    )
    print("Returned post from create")
    return created_post


@router.patch("/{id}")
async def update_my_post(
    post_id: int,
    values: PostUpdate,
    current_user: Annotated[UserRead, Depends(dependencies.get_current_active_auth_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    post = await crud_posts.get(
        db=session,
        schema_to_select=PostRead,
        id=post_id,
        is_deleted=False,
        created_by_user_id=current_user["id"],
    )
    if post is None:
        raise NotFoundException("Post not found")

    update_data = values.model_dump(
        exclude_unset=True,
    )
    update_internal = PostUpdateInternal(
        **update_data,
        updated_at=datetime.now(UTC),
    )

    await crud_posts.update(
        db=session,
        object=update_internal,
        id=post_id,
    )
    return {"message": "Post updated"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_post(
    post_id: int,
    current_user: Annotated[UserRead, Depends(dependencies.get_current_active_auth_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    post = await crud_posts.get(
        db=session,
        schema_to_select=PostRead,
        id=post_id,
        is_deleted=False,
        created_by_user_id=current_user.id,
    )
    if post is None:
        raise NotFoundException("Post not found")

    await crud_posts.db_delete(
        db=session,
        id=post_id,
    )
    return {
        "message": "Post deleted from the database",
    }


@router.delete(
    "/{username}/{id}/",
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    tags=["Admin"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_post(
    username: str,
    post_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await crud_users.get(
        db=session,
        schema_to_select=UserRead,
        username=username,
        is_deleted=False,
    )
    if user is None:
        raise NotFoundException("User not found")

    post = await crud_posts.get(
        db=session,
        schema_to_select=PostRead,
        id=post_id,
        is_deleted=False,
        created_by_user_id=user.id,
    )
    if post is None:
        raise NotFoundException("Post not found")
    await crud_posts.db_delete(
        db=session,
        id=post_id,
    )
    return {
        "message": "Post deleted from the database",
    }
