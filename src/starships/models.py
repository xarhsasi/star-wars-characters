from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Timestamps, starship_films

if TYPE_CHECKING:
    from src.films.models import Film  # noqa: F401


class Starship(Base, Timestamps):
    """Starship ORM model."""

    __tablename__ = "starships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    manufacturer: Mapped[str] = mapped_column(String, nullable=True)
    cost_in_credits: Mapped[int] = mapped_column(String, nullable=True)
    length: Mapped[int] = mapped_column(String, nullable=True)
    max_atmosphering_speed: Mapped[int] = mapped_column(String, nullable=True)
    crew: Mapped[int] = mapped_column(String, nullable=True)
    passengers: Mapped[int] = mapped_column(String, nullable=True)
    cargo_capacity: Mapped[int] = mapped_column(String, nullable=True)
    consumables: Mapped[str] = mapped_column(String, nullable=True)
    hyperdrive_rating: Mapped[float] = mapped_column(String, nullable=True)
    mglt: Mapped[int] = mapped_column(String, nullable=True)
    starship_class: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    films: Mapped[list["Film"]] = relationship(
        "Film", secondary=starship_films, back_populates="starships"
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Starship":
        """Create a Starship instance from a dictionary."""

        def norm_text_num(v: Any) -> str | None:
            if v is None:
                return None
            s = str(v).strip()
            if s.lower() in {"unknown", "n/a", "none", ""}:
                return None
            return s.replace(",", "")

        return cls(
            name=data["name"],
            model=data.get("model"),
            manufacturer=data.get("manufacturer"),
            cost_in_credits=norm_text_num(data.get("cost_in_credits")),
            length=norm_text_num(data.get("length")),
            max_atmosphering_speed=norm_text_num(data.get("max_atmosphering_speed")),
            crew=norm_text_num(data.get("crew")),
            passengers=norm_text_num(data.get("passengers")),
            cargo_capacity=norm_text_num(data.get("cargo_capacity")),
            consumables=data.get("consumables"),
            hyperdrive_rating=norm_text_num(data.get("hyperdrive_rating")),
            mglt=norm_text_num(data.get("MGLT")),
            starship_class=data.get("starship_class"),
            url=data.get("url"),
        )
