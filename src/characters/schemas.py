from datetime import datetime
from urllib.parse import urlsplit

from pydantic import BaseModel, model_validator


class CharacterOut(BaseModel):
    """Schema for character output."""

    id: int | None = None
    name: str
    height: int | None = None
    hair_color: str | None = None
    skin_color: str | None = None
    eye_color: str | None = None
    birth_year: str | None = None
    gender: str | None = None
    edited: datetime | None = None
    created: datetime | None = None
    url: str | None = None

    @model_validator(mode="after")
    def ensure_id(self):
        """Extract the ID from the URL.

        No, this is not a mistake, the ID does not belong in the response body
        and should extracted from the url property.

        E.g: https://swapi.info/api/people/1/ -> 1
        """
        if self.id is None:
            try:
                seg = urlsplit(self.url).path.rstrip("/").split("/")[-1]
                self.id = int(seg)
            except Exception as e:
                raise ValueError("Could not derive 'id' from 'url'") from e
        return self

    model_config = {"from_attributes": True}
