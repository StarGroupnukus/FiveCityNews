from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin, SoftDeleteMixin, TimestampMixin


class Post(IntIdPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    title: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(String(63206))

    media_url: Mapped[str | None] = mapped_column(String, default=None)

    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
