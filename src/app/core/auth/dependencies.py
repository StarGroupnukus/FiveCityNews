from app.core import db_helper
from app.core.logger import logging
from app.schemas.user import UserBase
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .helpers import (
    ACCESS_TOKEN_TYPE,
)

# REFRESH_TOKEN_TYPE,
from .validation import (
    get_current_token_payload,
    # get_refresh_token_payload,
    get_user_by_token_sub,
    validate_token_type,
)

logger = logging.getLogger(__name__)


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.session_getter),
    ):
        validate_token_type(payload, self.token_type)
        user = await get_user_by_token_sub(session, payload)
        # if not user.is_active:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )
        return user


# class RefreshTokenUserGetter:
#     async def __call__(
#         self,
#         payload: dict = Depends(get_refresh_token_payload),
#         session: AsyncSession = Depends(db_helper.session_getter),
#     ):
#         validate_token_type(payload, REFRESH_TOKEN_TYPE)
#         user = await get_user_by_token_sub(session, payload)
#         # if not user.is_active:
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Inactive user",
#             )
#         return user


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
# get_current_auth_user_for_refresh = RefreshTokenUserGetter()


async def get_current_active_auth_user(
    user: UserBase = Depends(get_current_auth_user),
):
    if user["is_active"]:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )


async def get_current_superadmin_user(
    user: UserBase = Depends(get_current_auth_user),
):
    if user["is_superuser"]:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not superadmin",
    )


async def get_optional_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> dict | None:
    try:
        validate_token_type(payload, ACCESS_TOKEN_TYPE)
        user = await get_user_by_token_sub(
            session=session,
            payload=payload,
        )
        if not user:
            return None
        return user
    except HTTPException as http_exc:
        if http_exc.status_code != 401:
            logger.exception(f"Unexpected HTTPException in get_optional_user: {http_exc.detail}")
        return None
    except Exception as exc:
        logger.exception(f"Unexpected error in get_optional_user: {exc}")
        return None
