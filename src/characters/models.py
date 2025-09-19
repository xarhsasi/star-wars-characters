from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Timestamps, film_characters

if TYPE_CHECKING:
    from src.films.models import Film  # noqa: F401

logger = logging.getLogger(__name__)


class Character(Base, Timestamps):
    """Character ORM model."""

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    hair_color: Mapped[str] = mapped_column(String, nullable=True)
    skin_color: Mapped[str] = mapped_column(String, nullable=True)
    eye_color: Mapped[str] = mapped_column(String, nullable=True)
    birth_year: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)

    films: Mapped[list["Film"]] = relationship(
        "Film", secondary=film_characters, back_populates="characters"
    )

    @classmethod
    def from_dict(cls, data: dict) -> "Film":
        """Create a Character instance from a dictionary."""
        height = data.get("height")
        if height not in {"unknown", "n/a", "none", ""}:
            height = int(height)
        else:
            height = None

        return cls(
            name=data["name"],
            height=height,
            hair_color=data.get("hair_color"),
            skin_color=data.get("skin_color"),
            eye_color=data.get("eye_color"),
            birth_year=data.get("birth_year"),
            gender=data.get("gender"),
            url=data.get("url"),
        )
