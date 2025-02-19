from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(IntIdPkMixin, UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    profile_image_url: Mapped[str] = mapped_column(String, default="https://profileimageurl.com")
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default="true",
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        server_default="false",
    )

    tier_id: Mapped[int | None] = mapped_column(
        ForeignKey("tiers.id"),
    )
