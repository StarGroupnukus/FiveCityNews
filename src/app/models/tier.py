from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdPkMixin, SoftDeleteMixin, TimestampMixin


class Tier(IntIdPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
