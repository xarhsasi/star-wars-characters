import logging

import pytest

from conftest import StarshipFactory
from src.starships.models import Starship
from src.test_base import RouterTestList, RouterTestRetrieve, RouterTestSearch

logger = logging.getLogger(__name__)


class TestStarshipRouter(RouterTestList, RouterTestRetrieve, RouterTestSearch):
    """Integration tests for the character router."""

    path = "v1/starship/"
    entities: list[Starship]

    # Router Test Search config
    SEARCH_QUERY_ATTR = "name"

    @pytest.fixture(autouse=True)
    async def setup(self):
        self.entities = await StarshipFactory.create_batch(10)
