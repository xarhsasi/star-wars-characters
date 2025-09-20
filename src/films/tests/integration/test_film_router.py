import logging

import pytest

from conftest import FilmFactory
from src.films.models import Film
from src.test_router_base import RouterTestList, RouterTestRetrieve, RouterTestSearch

logger = logging.getLogger(__name__)


class TestFilmRouter(RouterTestList, RouterTestRetrieve, RouterTestSearch):
    """Integration tests for the character router."""

    path = "v1/film/"
    entities: list[Film]

    # Router Test Search config
    SEARCH_QUERY_ATTR = "title"

    @pytest.fixture(autouse=True)
    async def setup(self):
        self.entities = await FilmFactory.create_batch(10)
