from typing import Annotated

from app.core import db_helper
from app.core.exceptions.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
)
from app.crud.crud_rate_limits import crud_rate_limits
from app.crud.crud_tiers import crud_tiers
from app.schemas.rate_limit import (
    RateLimitCreate,
    RateLimitCreateInternal,
    RateLimitRead,
    RateLimitUpdate,
)
from fastapi import APIRouter, Depends, status
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "/{tier_name}/list",
    response_model=PaginatedListResponse[RateLimitRead],
)
async def get_rate_limits(
    tier_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    page: int = 1,
    items_per_page: int = 10,
):
    db_tier = await crud_tiers.get(
        db=session,
        name=tier_name,
    )
    if not db_tier:
        raise NotFoundException("Tier not found")

    rate_limits_data = await crud_rate_limits.get_multi(
        db=session,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=RateLimitRead,
        tier_id=db_tier["id"],
    )

    return paginated_response(
        crud_data=rate_limits_data,
        page=page,
        items_per_page=items_per_page,
    )


@router.get(
    "/{tier_name}/{rate_limit_id}",
    response_model=RateLimitRead,
)
async def get_rate_limit_by_id(
    tier_name: str,
    rate_limit_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier = await crud_tiers.get(
        db=session,
        name=tier_name,
    )
    if not db_tier:
        raise NotFoundException("Tier not found")

    db_rate_limit: dict | None = await crud_rate_limits.get(
        db=session,
        schema_to_select=RateLimitRead,
        tier_id=db_tier["id"],
        id=rate_limit_id,
    )
    if db_rate_limit is None:
        raise NotFoundException("Rate Limit not found")

    return db_rate_limit


@router.post(
    "/{tier_name}/",
    status_code=status.HTTP_201_CREATED,
)
async def create_rate_limit(
    tier_name: str,
    rate_limit: RateLimitCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier = await crud_tiers.get(
        db=session,
        name=tier_name,
    )
    if not db_tier:
        raise NotFoundException("Tier not found")

    rate_limit_internal_dict = rate_limit.model_dump()
    rate_limit_internal_dict["tier_id"] = db_tier["id"]

    db_rate_limit = await crud_rate_limits.exists(
        db=session,
        name=rate_limit_internal_dict["name"],
    )
    if db_rate_limit:
        raise DuplicateValueException("Rate Limit Name not available")

    rate_limit_internal = RateLimitCreateInternal(**rate_limit_internal_dict)
    created_rate_limit: RateLimitRead = await crud_rate_limits.create(
        db=session,
        object=rate_limit_internal,
    )
    return created_rate_limit


@router.patch(
    "/{tier_name}/{rate_limit_id}",
)
async def update_rate_limit(
    tier_name: str,
    rate_limit_id: int,
    values: RateLimitUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier = await crud_tiers.get(db=session, name=tier_name)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    db_rate_limit = await crud_rate_limits.get(
        db=session,
        schema_to_select=RateLimitRead,
        tier_id=db_tier["id"],
        id=rate_limit_id,
    )
    if db_rate_limit is None:
        raise NotFoundException("Rate Limit not found")

    db_rate_limit_path = await crud_rate_limits.exists(
        db=session,
        tier_id=db_tier["id"],
        path=values.path,
    )
    if db_rate_limit_path:
        raise DuplicateValueException("There is already a rate limit for this path")

    await crud_rate_limits.exists(db=session)
    if db_rate_limit_path:
        raise DuplicateValueException("There is already a rate limit with this name")

    await crud_rate_limits.update(
        db=session,
        object=values,
        id=db_rate_limit["id"],
    )
    return {"message": "Rate Limit updated"}


@router.delete(
    "/{tier_name}/{rate_limit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_rate_limit(
    tier_name: str,
    rate_limit_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier = await crud_tiers.get(
        db=session,
        name=tier_name,
    )
    if not db_tier:
        raise NotFoundException("Tier not found")

    db_rate_limit = await crud_rate_limits.get(
        db=session,
        schema_to_select=RateLimitRead,
        tier_id=db_tier["id"],
        id=rate_limit_id,
    )
    if db_rate_limit is None:
        raise NotFoundException("Rate Limit not found")

    await crud_rate_limits.delete(
        db=session,
        id=db_rate_limit["id"],
    )
    return {"message": "Rate Limit deleted"}
