import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        index=True,
    )


class UUIDMixin:
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid_pkg.uuid4,
        server_default=text("gen_random_uuid()"),
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(UTC),
        server_default=text("current_timestamp(0)"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
        server_default=text("current_timestamp(0)"),
        onupdate=datetime.now(UTC),
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
        server_default=None,
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        server_default="false",
    )
