from typing import Annotated

from app.core import db_helper
from app.core.auth import dependencies
from app.core.config import settings
from app.core.exceptions.http_exceptions import (
    RateLimitException,
)
from app.core.logger import logging
from app.core.utils.rate_limit import is_rate_limited
from app.crud.crud_rate_limits import crud_rate_limits
from app.crud.crud_tiers import crud_tiers
from app.models.user import User
from app.schemas.rate_limit import sanitize_path
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = settings.rate_limit.DEFAULT_LIMIT
DEFAULT_PERIOD = settings.rate_limit.DEFAULT_PERIOD


async def rate_limiter(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: User | None = Depends(dependencies.get_optional_user),
) -> None:
    path = sanitize_path(request.url.path)
    if user:
        user_id = user["id"]
        tier = await crud_tiers.get(db=session, id=user["tier_id"])
        if tier:
            rate_limit = await crud_rate_limits.get(
                db=session,
                tier_id=tier["id"],
                path=path,
            )
            if rate_limit:
                limit, period = rate_limit["limit"], rate_limit["period"]
            else:
                logger.warning(
                    f"User {user_id} with tier '{tier['name']}' has no specific rate limit for path '{path}'. \
                        Applying default rate limit."
                )
                limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD
        else:
            logger.warning(f"User {user_id} has no assigned tier. Applying default rate limit.")
            limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD
    else:
        user_id = request.client.host
        limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD

    is_limited = await is_rate_limited(
        user_id=user_id,
        path=path,
        limit=limit,
        period=period,
    )
    if is_limited:
        raise RateLimitException("Rate limit exceeded.")
