from datetime import datetime

from pydantic import BaseModel

from src.characters.schemas import CharacterOut
from src.starships.schemas import StarshipOut


class FilmOut(BaseModel):
    """Schema for character output."""

    id: int | None = None
    title: str
    opening_crawl: str | None = None
    director: str | None = None
    producer: str | None = None
    release_date: datetime | None = None
    url: str | None = None

    # nested relationships
    characters: list["CharacterOut"] = []
    starships: list["StarshipOut"] = []

    model_config = {"from_attributes": True}
