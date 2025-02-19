from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .mixins import SoftDeleteSchema, TimestampSchema, UUIDSchema

# Константы
MIN_TITLE_LENGTH = 2
MAX_TITLE_LENGTH = 30
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 63206
DEFAULT_MEDIA_URL = "https://www.postimageurl.com"

# Общие поля с аннотациями
TITLE_FIELD = Annotated[
    str,
    Field(
        min_length=MIN_TITLE_LENGTH,
        max_length=MAX_TITLE_LENGTH,
        examples=["This is my post"],
    ),
]
TITLE_FIELD_UPDATE = Annotated[
    str | None,
    Field(
        min_length=MIN_TITLE_LENGTH,
        max_length=MAX_TITLE_LENGTH,
        examples=["This is my updated post"],
        default=None,
    ),
]
TEXT_FIELD = Annotated[
    str,
    Field(
        min_length=MIN_TEXT_LENGTH,
        max_length=MAX_TEXT_LENGTH,
        examples=["This is the content of my post."],
    ),
]
TEXT_FIELD_UPDATE = Annotated[
    str | None,
    Field(
        min_length=MIN_TEXT_LENGTH,
        max_length=MAX_TEXT_LENGTH,
        examples=["This is the updated content of my post."],
        default=None,
    ),
]
MEDIA_URL_FIELD = Annotated[
    HttpUrl | None,
    Field(
        examples=[DEFAULT_MEDIA_URL],
        default=None,
    ),
]


class PostBase(BaseModel):
    """Базовая схема поста с основными полями."""

    title: TITLE_FIELD
    text: TEXT_FIELD


class Post(PostBase, TimestampSchema, UUIDSchema, SoftDeleteSchema):
    """Схема поста с расширенными полями."""

    media_url: MEDIA_URL_FIELD
    created_by_user_id: int


class PostRead(PostBase):
    """Схема чтения поста."""

    id: int
    media_url: str | None
    created_by_user_id: int
    created_at: datetime


class PostCreate(PostBase):
    """Схема создания поста."""

    model_config = ConfigDict(extra="forbid")

    media_url: MEDIA_URL_FIELD


class PostCreateInternal(PostCreate):
    """Схема внутреннего создания поста."""

    created_by_user_id: int


class PostUpdate(BaseModel):
    """Схема обновления поста."""

    model_config = ConfigDict(extra="forbid")

    title: TITLE_FIELD_UPDATE
    text: TEXT_FIELD_UPDATE
    media_url: MEDIA_URL_FIELD


class PostUpdateInternal(PostUpdate):
    """Схема внутреннего обновления поста."""

    updated_at: datetime | None = None


class PostDelete(BaseModel):
    """Схема удаления поста."""

    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class PostFilter(BaseModel):
    """Схема фильтрации постов."""

    id: int | None = None
    title: str | None = None
    text: str | None = None
    created_by_user_id: int | None = None
    is_active: bool | None = None
    is_deleted: bool | None = None
