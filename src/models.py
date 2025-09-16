"""The base classes for all models."""

from datetime import datetime
from typing import Any, Callable, ClassVar

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql import func

# Guide mypy to know that func is indeed a callable method
func: Callable  # type:ignore[no-redef]


class Base(DeclarativeBase):
    """The base class for all models."""

    id: Any
    __name__: ClassVar[str]

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Timestamps:
    """Abstract base class for timestamp columns."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
