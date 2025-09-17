from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Timestamps, film_characters, starship_films


class Film(Base, Timestamps):
    """Starship ORM model."""

    __tablename__ = "films"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    opening_crawl: Mapped[str] = mapped_column(String)
    director: Mapped[str] = mapped_column(String)
    producer: Mapped[str] = mapped_column(String)
    release_date: Mapped[DateTime] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String, unique=True)
    characters: Mapped[list["Character"]] = relationship(
        "Character", secondary=film_characters, back_populates="films"
    )
    starships: Mapped[list["Starship"]] = relationship(
        "Starship", secondary=starship_films, back_populates="films"
    )
