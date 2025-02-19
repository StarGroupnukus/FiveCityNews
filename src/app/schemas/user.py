from datetime import datetime
from enum import IntEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

from .mixins import SoftDeleteSchema, TimestampSchema, UUIDSchema

# Константы
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 30
MIN_USERNAME_LENGTH = 2
MAX_USERNAME_LENGTH = 20
DEFAULT_PROFILE_IMAGE = "https://www.profileimageurl.com"


class UserTier(IntEnum):
    FREE = 1
    PREMIUM = 2
    ENTERPRISE = 3


# Общие поля с аннотациями
NAME_FIELD = Annotated[
    str,
    Field(
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
        examples=["User Userson"],
    ),
]
NAME_FIELD_UPDATE = Annotated[
    str | None,
    Field(
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
        examples=["User Userberg"],
        default=None,
    ),
]
USERNAME_FIELD = Annotated[
    str,
    Field(
        min_length=MIN_USERNAME_LENGTH,
        max_length=MAX_USERNAME_LENGTH,
        pattern=r"^[a-z0-9]+$",
        examples=["userson"],
    ),
]
USERNAME_FIELD_UPDATE = Annotated[
    str | None,
    Field(
        min_length=2,
        max_length=20,
        pattern=r"^[a-z0-9]+$",
        examples=["userberg"],
        default=None,
    ),
]
EMAIL_FIELD = Annotated[EmailStr, Field(examples=["userson@example.com"])]
EMAIL_FIELD_UPDATE = Annotated[EmailStr | None, Field(examples=["userberg@example.com"], default=None)]
PROFILE_IMAGE_FIELD = Annotated[HttpUrl, Field(default="https://www.profileimageurl.com")]
PROFILE_IMAGE_FIELD_UPDATE = Annotated[
    HttpUrl | None,
    Field(
        examples=["https://www.profileimageurl.com"],
        default=None,
    ),
]

PASSWORD_FIELD = Annotated[
    str,
    Field(
        pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
        examples=["pass123"],
    ),
]


class UserBase(BaseModel):
    """Базовая схема пользователя с основными полями."""

    name: NAME_FIELD
    username: USERNAME_FIELD_UPDATE
    email: EMAIL_FIELD


class User(UserBase, TimestampSchema, UUIDSchema, SoftDeleteSchema):
    profile_image_url: PROFILE_IMAGE_FIELD
    hashed_password: str
    is_superuser: bool = False
    tier_id: int | None = None


class UserRead(UserBase):
    id: int
    profile_image_url: str
    is_superuser: bool = False
    is_active: bool = True
    tier_id: int | None


class UserCreate(UserBase):
    """Схема создания пользователя."""

    model_config = ConfigDict(extra="forbid")

    password: PASSWORD_FIELD


class UserCreateInternal(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    """Схема обновления данных пользователя."""

    model_config = ConfigDict(extra="forbid")

    name: NAME_FIELD_UPDATE
    username: USERNAME_FIELD_UPDATE
    email: EMAIL_FIELD_UPDATE
    profile_image_url: PROFILE_IMAGE_FIELD_UPDATE


class UserUpdateInternal(UserUpdate):
    # updated_at: datetime
    updated_at: datetime | None = None


class UserTierUpdate(BaseModel):
    """Схема обновления уровня пользователя."""

    tier_id: int


class UserDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class UserRestoreDeleted(BaseModel):
    is_deleted: bool


class UserFilter(BaseModel):
    id: int | None = None
    name: str | None = None
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    tier_id: int | None = None
