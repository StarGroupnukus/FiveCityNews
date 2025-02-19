import uuid as uuid_pkg
from datetime import datetime

from pydantic import BaseModel, Field


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class Token(BaseModel):
    jti: uuid_pkg.UUID = Field(default=uuid_pkg.uuid4)
    token_type: str


class TokenData(BaseModel):
    username_or_email: str


class TokenBlacklistBase(Token, BaseModel):
    expires_at: datetime


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenBlacklistUpdate(TokenBlacklistBase):
    pass
