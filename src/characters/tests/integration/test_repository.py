import http
import logging

import pytest
from httpx import AsyncClient

from conftest import CharacterFactory

logger = logging.getLogger(__name__)


@pytest.mark.anyio
class TestRepositoryIntegration:
    """Integration tests for the character router."""

    @pytest.fixture(autouse=True)
    async def setup(self):
        self.characters = await CharacterFactory.create_batch(10)
