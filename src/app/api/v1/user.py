from datetime import UTC, datetime
from typing import Annotated

from app.core import db_helper
from app.core.auth import dependencies
from app.core.exceptions.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
)
from app.core.utils.auth_utils import hash_password
from app.crud.crud_rate_limits import crud_rate_limits
from app.crud.crud_tiers import crud_tiers
from app.crud.crud_users import crud_users
from app.models.tier import Tier
from app.schemas.tier import TierRead
from app.schemas.user import (
    UserCreate,
    UserCreateInternal,
    UserRead,
    UserTierUpdate,
    UserUpdate,
    UserUpdateInternal,
)
from fastapi import APIRouter, Depends, status
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(
    user: UserCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserRead:
    email_row = await crud_users.exists(
        db=session,
        email=user.email,
    )
    if email_row:
        raise DuplicateValueException("Email is already registered")

    username_row = await crud_users.exists(
        db=session,
        username=user.username,
    )
    if username_row:
        raise DuplicateValueException("Username not available")

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = hash_password(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    created_user: UserRead = await crud_users.create(
        db=session,
        object=user_internal,
    )
    return created_user


@router.get("/me/", response_model=UserRead)
async def get_my_profile(
    user: UserRead = Depends(dependencies.get_current_active_auth_user),
) -> UserRead:
    return user


@router.get(
    "/",
    response_model=PaginatedListResponse[UserRead],
    tags=["Admin"],
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
)
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    page: int = 1,
    items_per_page: int = 10,
):
    users_data = await crud_users.get_multi(
        db=session,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead,
        is_deleted=False,
    )

    return paginated_response(
        crud_data=users_data,
        page=page,
        items_per_page=items_per_page,
    )


@router.get(
    "/{username}",
    response_model=UserRead,
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    tags=["Admin"],
)
async def get_user(
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user: UserRead | None = await crud_users.get(
        db=session,
        schema_to_select=UserRead,
        username=username,
        is_deleted=False,
    )
    if user is None:
        raise NotFoundException("User not found")

    return user


@router.patch("/", status_code=status.HTTP_200_OK)
async def update_my_profile(
    values: UserUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: UserRead = Depends(dependencies.get_current_active_auth_user),
):
    if values.username and values.username != current_user.username:
        existing_username = await crud_users.exists(db=session, username=values.username)
        if existing_username:
            raise DuplicateValueException("Username not available")

    if values.email != current_user.email:
        existing_email = await crud_users.exists(
            db=session,
            email=values.email,
        )
        if existing_email:
            raise DuplicateValueException("Email is already registered")

    update_data = values.model_dump(
        exclude_unset=True,
    )
    update_internal = UserUpdateInternal(
        **update_data,
        updated_at=datetime.now(UTC),
    )

    await crud_users.update(
        db=session,
        object=update_internal,
        username=current_user.username,
    )
    return {"message": "User updated"}


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_my_profile(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: UserRead = Depends(dependencies.get_current_active_auth_user),
):
    await crud_users.delete(
        db=session,
        username=current_user.username,
    )
    # todo: add token to  blacklist
    return {
        "message": "User deleted",
    }


@router.delete(
    "/{username}",
    status_code=status.HTTP_200_OK,
    tags=["Admin"],
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
)
async def delete_user(
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await crud_users.exists(
        db=session,
        username=username,
    )
    if not user:
        raise NotFoundException("User not found")

    await crud_users.db_delete(
        db=session,
        username=username,
    )

    # todo: add token to  blacklist
    return {
        "message": "User deleted from the database",
    }


@router.get(
    "/{username}/rate_limits",
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    tags=["Admin"],
)
async def get_user_rate_limits(
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_user: dict | None = await crud_users.get(
        db=session,
        username=username,
        schema_to_select=UserRead,
    )
    if db_user is None:
        raise NotFoundException("User not found")

    if db_user["tier_id"] is None:
        db_user["tier_rate_limits"] = []
        return db_user

    db_tier = await crud_tiers.get(
        db=session,
        id=db_user["tier_id"],
    )
    if db_tier is None:
        raise NotFoundException("Tier not found")

    db_rate_limits = await crud_rate_limits.get_multi(
        db=session,
        tier_id=db_tier["id"],
    )

    db_user["tier_rate_limits"] = db_rate_limits["data"]

    return db_user


@router.get(
    "/{username}/tier",
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    tags=["Admin"],
)
async def get_user_tier(
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_user = await crud_users.get(
        db=session,
        username=username,
        schema_to_select=UserRead,
    )
    if db_user is None:
        raise NotFoundException("User not found")

    db_tier = await crud_tiers.exists(
        db=session,
        id=db_user["tier_id"],
    )
    if not db_tier:
        raise NotFoundException("Tier not found")

    return await crud_users.get_joined(
        db=session,
        join_model=Tier,
        join_prefix="tier_",
        schema_to_select=UserRead,
        join_schema_to_select=TierRead,
        username=username,
    )


@router.patch(
    "/{username}/tier",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    tags=["Admin"],
)
async def update_user_tier(
    username: str,
    values: UserTierUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> dict[str, str]:
    db_user = await crud_users.get(
        db=session,
        username=username,
        schema_to_select=UserRead,
    )
    if not db_user:
        raise NotFoundException("User not found")

    db_tier = await crud_tiers.exists(
        db=session,
        id=values.tier_id,
    )
    if not db_tier:
        raise NotFoundException("Tier not found")

    await crud_users.update(
        db=session,
        object=values,
        username=username,
    )
    return {
        "message": f"User {db_user['name']} Tier updated",
    }
