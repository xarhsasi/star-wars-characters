from datetime import datetime

from pydantic import BaseModel


class StarshipOut(BaseModel):
    """Schema for character output."""

    id: int | None = None
    name: str
    model: str | None = None
    manufacturer: str | None = None
    cost_in_credits: int | None = None
    length: int | None = None
    max_atmosphering_speed: int | None = None
    crew: int | None = None
    passengers: int | None = None
    cargo_capacity: int | None = None
    consumables: str | None = None
    hyperdrive_rating: float | None = None
    mglt: int | None = None
    url: str | None = None

    model_config = {"from_attributes": True}
