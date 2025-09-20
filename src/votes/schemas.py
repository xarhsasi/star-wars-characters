from datetime import datetime

from pydantic import BaseModel


class VoteOut(BaseModel):
    """Vote output schema."""

    id: int
    value: int
    feedback: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True  # Allows parsing from ORM attributes in Pydantic v2
    }
