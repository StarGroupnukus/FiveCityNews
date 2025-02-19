from app.crud.crud_token_blacklist import crud_token_blacklist
from app.crud.crud_users import crud_users
from app.schemas.user import UserBase
from fastapi import (
    Cookie,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

# from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils import auth_utils
from .helpers import (
    TOKEN_TYPE_FIELD,
)

# http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


def get_current_token_payload(
    access_token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        # Extract the token from the credentials object
        if access_token and hasattr(access_token, "credentials"):
            token = access_token.credentials
        else:
            token = access_token

        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return payload


async def get_refresh_token_payload(
    refresh_token: str | None = Cookie(alias="refresh_token", default=None),
) -> dict:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    try:
        # Extract the token if it's a credentials object
        if hasattr(refresh_token, "credentials"):
            token = refresh_token.credentials
        else:
            token = refresh_token

        payload = auth_utils.decode_jwt(
            token=token,
        )
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {e}",
        )


async def get_user_by_token_sub(session: AsyncSession, payload: dict) -> UserBase:
    user_id: str | None = payload.get("sub")
    # todo: check token blacklist
    jti = payload.get("jti")
    is_blacklisted = await crud_token_blacklist.exists(
        db=session,
        jti=jti,
    )
    if is_blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token (blacklisted)",
        )
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token (user not found)",
        )
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )

    user = await crud_users.get(
        db=session,
        id=user_id_int,
        is_deleted=False,
    )
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token (user not found)",
    )


async def authenticate_user(
    username_or_email: str,
    password: str,
    session: AsyncSession,
) -> UserBase | None:
    if "@" in username_or_email:
        db_user = await crud_users.get(
            db=session,
            email=username_or_email,
            is_deleted=False,
        )
    else:
        db_user = await crud_users.get(
            db=session,
            username=username_or_email,
            is_deleted=False,
        )
    if not db_user:
        return None

    elif not await auth_utils.verify_password(
        password=password,
        hashed_password=db_user["hashed_password"],
    ):
        return None

    return db_user
