from datetime import datetime

from pydantic import BaseModel


class FilmOut(BaseModel):
    """Schema for character output."""

    id: int | None = None
    title: str
    opening_crawl: str | None = None
    director: str | None = None
    producer: str | None = None
    release_date: datetime | None = None
    url: str | None = None

    model_config = {"from_attributes": True}
