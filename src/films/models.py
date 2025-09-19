from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Timestamps, film_characters, starship_films

if TYPE_CHECKING:
    from src.characters.models import Character  # noqa: F401
    from src.starships.models import Starship  # noqa: F401


class Film(Base, Timestamps):
    """Starship ORM model."""

    __tablename__ = "films"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    opening_crawl: Mapped[str] = mapped_column(String, nullable=True)
    director: Mapped[str] = mapped_column(String, nullable=True)
    producer: Mapped[str] = mapped_column(String, nullable=True)
    release_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    characters: Mapped[list["Character"]] = relationship(
        "Character", secondary=film_characters, back_populates="films"
    )
    starships: Mapped[list["Starship"]] = relationship(
        "Starship", secondary=starship_films, back_populates="films"
    )

    @classmethod
    def from_dict(cls, data: dict) -> "Film":
        """Create a Film instance from a dictionary."""
        release_date = data.get("release_date")
        if release_date:
            release_date = datetime.datetime.fromisoformat(release_date)

        return cls(
            title=data["title"],
            opening_crawl=data.get("opening_crawl"),
            director=data.get("director"),
            producer=data.get("producer"),
            release_date=release_date,
            url=data.get("url"),
        )
