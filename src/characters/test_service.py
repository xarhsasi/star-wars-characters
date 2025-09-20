from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.characters.models import Character
from src.characters.service import CharacterService
from src.exceptions import ORMNotFoundException


@pytest.mark.asyncio
async def test_add_characters():
    # Mock dependencies
    mock_session = AsyncMock()
    mock_repository = MagicMock()
    mock_character = MagicMock()
    mock_character.name = "Luke Skywalker"
    mock_character.url = "http://swapi.dev/api/people/1/"

    # Patch Character.from_dict to return a mock character
    with patch(
        "src.characters.models.Character.from_dict", return_value=mock_character
    ):
        # Instantiate the service
        service = CharacterService(session=mock_session)
        service._repository = mock_repository
        service.by_url = AsyncMock(side_effect=ORMNotFoundException)
        service.create = AsyncMock()

        # Input data
        characters = [
            {"name": "Luke Skywalker", "url": "http://swapi.dev/api/people/1/"}
        ]

        # Call the method
        await service.add_characters(characters=characters)

        # Assertions
        mock_session.begin.assert_called_once()
        service.by_url.assert_awaited_once_with(url="http://swapi.dev/api/people/1/")
        service.create.assert_awaited_once_with(obj=mock_character)
        mock_repository.create.assert_not_called()  # Ensure repository create is not directly called
