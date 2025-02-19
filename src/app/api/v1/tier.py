from typing import Annotated

from app.core import db_helper
from app.core.auth import dependencies
from app.core.exceptions.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
)
from app.crud.crud_tiers import crud_tiers
from app.schemas.tier import (
    TierCreate,
    TierCreateInternal,
    TierRead,
    TierUpdate,
)
from fastapi import APIRouter, Depends, status
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "/list",
    response_model=PaginatedListResponse[TierRead],
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
)
async def get_tiers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    page: int = 1,
    items_per_page: int = 10,
):
    tiers_data = await crud_tiers.get_multi(
        db=session,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=TierRead,
    )

    return paginated_response(
        crud_data=tiers_data,
        page=page,
        items_per_page=items_per_page,
    )


@router.get(
    "/{name}",
    response_model=TierRead,
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
)
async def get_tier(
    name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier: dict | None = await crud_tiers.get(
        db=session,
        schema_to_select=TierRead,
        name=name,
    )
    if db_tier is None:
        raise NotFoundException("Tier not found")

    return db_tier


@router.post(
    "",
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    status_code=status.HTTP_201_CREATED,
)
async def create_tier(
    tier: TierCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    tier_internal_dict = tier.model_dump()
    db_tier = await crud_tiers.exists(
        db=session,
        name=tier_internal_dict["name"],
    )
    if db_tier:
        raise DuplicateValueException("Tier Name not available")

    tier_internal = TierCreateInternal(**tier_internal_dict)
    created_tier: TierRead = await crud_tiers.create(
        db=session,
        object=tier_internal,
    )
    return created_tier


@router.patch(
    "/{name}",
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
)
async def update_tier(
    values: TierUpdate,
    name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier = await crud_tiers.get(
        db=session,
        schema_to_select=TierRead,
        name=name,
    )
    if db_tier is None:
        raise NotFoundException("Tier not found")

    await crud_tiers.update(
        db=session,
        object=values,
        name=name,
    )
    return {"message": "Tier updated"}


@router.delete(
    "/{name}",
    dependencies=[Depends(dependencies.get_current_superadmin_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tier(
    name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    db_tier = await crud_tiers.get(
        db=session,
        schema_to_select=TierRead,
        name=name,
    )
    if db_tier is None:
        raise NotFoundException("Tier not found")

    await crud_tiers.delete(
        db=session,
        name=name,
    )
    return {"message": "Tier deleted"}
