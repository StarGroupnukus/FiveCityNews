from datetime import datetime

from app.core.utils import auth_utils
from app.models.token_blacklist import TokenBlacklist
from app.schemas.token_blacklist import TokenBlacklistCreate, TokenBlacklistUpdate
from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

CRUDTokenBlacklist = FastCRUD[
    TokenBlacklist,
    TokenBlacklistCreate,
    TokenBlacklistUpdate,
    TokenBlacklistUpdate,
    None,
    None,
]
crud_token_blacklist = CRUDTokenBlacklist(TokenBlacklist)


async def add_to_blacklist(
    token: str,
    session: AsyncSession,
) -> None:
    payload = auth_utils.decode_jwt(token)
    expires_at = datetime.fromtimestamp(payload.get("exp"))
    await crud_token_blacklist.create(
        db=session,
        object=TokenBlacklistCreate(
            **{
                "jti": payload.get("jti"),
                "expires_at": expires_at,
            }
        ),
    )
