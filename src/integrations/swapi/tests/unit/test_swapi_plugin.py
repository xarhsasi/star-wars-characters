from unittest.mock import AsyncMock, patch

import pytest

from src.integrations.swapi.plugin import SwapiPlugin


@pytest.mark.anyio
class TestSwapiPlugin:
    """Unit tests for the SwapiPlugin class."""

    @pytest.fixture(autouse=True)
    def plugin(self) -> SwapiPlugin:
        """Fixture to create a SwapiPlugin instance."""
        self.plugin = SwapiPlugin()

    @patch("src.integrations.api.Plugin._get", new_callable=AsyncMock)
    async def test_starships(self, mock_get):
        """Test fetching starships."""
        mock_get.return_value = [{"name": "X-Wing"}, {"name": "TIE Fighter"}]
        result = await self.plugin.starships()
        mock_get.assert_called_once_with("starships/")
        assert result == [{"name": "X-Wing"}, {"name": "TIE Fighter"}]

    @patch("src.integrations.api.Plugin._get", new_callable=AsyncMock)
    async def test_starship(self, mock_get):
        """Test fetching a specific starship by ID."""
        mock_get.return_value = {"name": "Millennium Falcon"}
        result = await self.plugin.starship(10)
        mock_get.assert_called_once_with("starships/10/")
        assert result == {"name": "Millennium Falcon"}

    @patch("src.integrations.api.Plugin._get", new_callable=AsyncMock)
    async def test_characters(self, mock_get):
        """Test fetching characters."""
        mock_get.return_value = [{"name": "Luke Skywalker"}, {"name": "Darth Vader"}]
        result = await self.plugin.characters()
        mock_get.assert_called_once_with("people/")
        assert result == [{"name": "Luke Skywalker"}, {"name": "Darth Vader"}]

    @patch("src.integrations.api.Plugin._get", new_callable=AsyncMock)
    async def test_character(self, mock_get):
        """Test fetching a specific character by ID."""
        mock_get.return_value = {"name": "Leia Organa"}
        result = await self.plugin.character(5)
        mock_get.assert_called_once_with("people/5/")
        assert result == {"name": "Leia Organa"}

    @patch("src.integrations.api.Plugin._get", new_callable=AsyncMock)
    async def test_films(self, mock_get):
        """Test fetching films."""
        mock_get.return_value = [
            {"title": "A New Hope"},
            {"title": "The Empire Strikes Back"},
        ]
        result = await self.plugin.films()
        mock_get.assert_called_once_with("films/")
        assert result == [{"title": "A New Hope"}, {"title": "The Empire Strikes Back"}]

    @patch("src.integrations.api.Plugin._get", new_callable=AsyncMock)
    async def test_film(self, mock_get):
        """Test fetching a specific film by ID."""
        mock_get.return_value = {"title": "Return of the Jedi"}
        result = await self.plugin.film(3)
        mock_get.assert_called_once_with("films/3/")
        assert result == {"title": "Return of the Jedi"}
