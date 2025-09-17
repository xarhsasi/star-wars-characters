import http
import logging

import pytest
from httpx import AsyncClient

from conftest import CharacterFactory

logger = logging.getLogger(__name__)


@pytest.mark.anyio
class TestRouterIntegration:
    """Integration tests for the character router."""

    @pytest.fixture(autouse=True)
    async def setup(self):
        self.characters = await CharacterFactory.create_batch(10)

    async def test_list_characters(self, client: AsyncClient) -> None:
        """Test listing characters."""
        response = await client.get("v1/character/")
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "page_size" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 10

    async def test_retrieve_character(self, client: AsyncClient) -> None:
        """Test retrieving a character by ID."""
        character_id = self.characters[0].id
        response = await client.get(f"v1/character/{character_id}/")
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert data["id"] == character_id
        assert data["name"] == self.characters[0].name
        assert data["height"] == self.characters[0].height
        assert data["hair_color"] == self.characters[0].hair_color
        assert data["skin_color"] == self.characters[0].skin_color
        assert data["eye_color"] == self.characters[0].eye_color
        assert data["birth_year"] == self.characters[0].birth_year
        assert data["gender"] == self.characters[0].gender

    async def test_retrieve_character_not_found(self, client: AsyncClient) -> None:
        """Test retrieving a non-existent character."""
        response = await client.get("v1/character/99999/")
        assert response.status_code == http.HTTPStatus.NOT_FOUND
        data = response.json()
        assert data["detail"] == "Character with ID 99999 not found."

    async def test_search_characters(self, client: AsyncClient) -> None:
        """Test searching for characters by name."""
        character_name = str(self.characters[0].name)
        logger.warning(character_name)
        response = await client.get(
            "v1/character/search/", params={"query": character_name}
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert any(char["name"] == character_name for char in data)

    async def test_search_characters_no_results(self, client: AsyncClient) -> None:
        """Test searching for characters with no matching results."""
        response = await client.get(
            "v1/character/search/", params={"query": "NonExistentName"}
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_search_characters_invalid_query(self, client: AsyncClient) -> None:
        """Test searching for characters with an invalid query."""
        response = await client.get("v1/character/search/", params={"query": ""})
        assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data
