from datetime import datetime

from pydantic import BaseModel


class StarshipOut(BaseModel):
    """Schema for character output."""

    id: int | None = None
    name: str
    model: str | None = None
    manufacturer: str | None = None
    cost_in_credits: str | None = None
    length: str | None = None
    max_atmosphering_speed: str | None = None
    crew: str | None = None
    passengers: str | None = None
    cargo_capacity: str | None = None
    consumables: str | None = None
    hyperdrive_rating: str | None = None
    mglt: str | None = None
    starship_class: str | None = None
    url: str | None = None

    model_config = {"from_attributes": True}
