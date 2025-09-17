"""The base classes for all models."""

from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import Column, DateTime, ForeignKey, Table
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql import func


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


# Association Tables

film_characters = Table(
    "film_characters",
    Base.metadata,
    Column("film_id", ForeignKey("films.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "character_id",
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


starship_films = Table(
    "starship_films",
    Base.metadata,
    Column("film_id", ForeignKey("films.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "startship_id", ForeignKey("starships.id", ondelete="CASCADE"), primary_key=True
    ),
)
