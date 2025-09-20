import logging

import pytest

from conftest import CharacterFactory
from src.characters.models import Character
from src.test_router_base import RouterTestList, RouterTestRetrieve, RouterTestSearch

logger = logging.getLogger(__name__)


class TestCharacterRouter(RouterTestList, RouterTestRetrieve, RouterTestSearch):
    """Integration tests for the character router."""

    path = "v1/character/"
    entities: list[Character]

    # Router Test Search config
    SEARCH_QUERY_ATTR = "name"

    @pytest.fixture(autouse=True)
    async def setup(self):
        self.entities = await CharacterFactory.create_batch(10)
