from typing import Annotated

from app.core import db_helper
from app.core.auth import helpers, validation
from app.core.auth.helpers import REFRESH_TOKEN_TYPE
from app.core.config import settings
from app.core.exceptions.http_exceptions import UnauthorizedException
from app.schemas.token_blacklist import TokenInfo
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login", response_model=TokenInfo)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await validation.authenticate_user(
        username_or_email=form_data.username,
        password=form_data.password,
        session=session,
    )
    if not user:
        raise UnauthorizedException("Wrong username, email or password.")
    access_token = await helpers.create_access_token(user)
    refresh_token = await helpers.create_refresh_token(user)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=settings.crypt.REFRESH_TOKEN_EXPIRE_DAYSА * 24 * 60 * 60,
    )

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


@router.post("/refresh", response_model=TokenInfo)
async def refresh_access_token(
    refresh_token: str,
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    refresh_token = refresh_token or request.cookies.get("refresh_token")
    payload = validation.get_refresh_token_payload(refresh_token)
    validation.validate_token_type(payload, REFRESH_TOKEN_TYPE)
    user = await validation.get_user_by_token_sub(
        session=session,
        payload=payload,
    )
    # todo: is token in blacklist?
    new_access_token = await helpers.create_access_token(user)
    return TokenInfo(
        access_token=new_access_token,
        token_type="Bearer",
    )
