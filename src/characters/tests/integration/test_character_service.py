import logging

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import CharacterFactory
from src.characters.models import Character
from src.characters.service import CharacterService

logger = logging.getLogger(__name__)


@pytest.mark.anyio
class TestCharacterServce:
    """Integration tests for the film service."""

    entities: list[Character]

    @pytest.fixture(autouse=True)
    async def setup(self, session: AsyncSession) -> None:
        self.entities = await CharacterFactory.create_batch(10)
        self.service = CharacterService(session=session)

    async def test_list(self) -> None:
        """Test listing characters."""
        result = await self.service.list(page=1, page_size=5)
        assert result.page == 1
        assert result.page_size == 5
        assert result.total >= 10
        assert len(result.items) == 5

    async def test_get(self) -> None:
        """Test getting a character by ID."""
        character = self.entities[0]
        fetched_character = await self.service.get(character.id)
        assert fetched_character.id == character.id
        assert fetched_character.name == character.name

    async def test_by_url(self) -> None:
        """Test getting a character by URL."""
        character = self.entities[0]
        fetched_character = await self.service.by_url(character.url)
        assert fetched_character.id == character.id
        assert fetched_character.name == character.name

    async def test_create(self) -> None:
        """Test creating a new film."""
        new_character_data = {
            "name": "New Character",
            "height": 7,
            "hair_color": "black",
            "skin_color": "black",
            "eye_color": "black",
            "birth_year": "1996",
            "gender": "n/a",
            "url": "http://swapi.dev/api/character/99/",
        }
        new_film = Character.from_dict(new_character_data)
        created_character = await self.service.create(new_film)
        assert created_character.id is not None
        assert created_character.name == new_character_data["name"]

    async def test_search(self) -> None:
        """Test searching characters by name."""
        character = self.entities[0]
        results = await self.service.search(query=character.name[:3])
        assert len(results) >= 1
