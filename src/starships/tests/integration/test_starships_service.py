import logging

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import StarshipFactory
from src.starships.models import Starship
from src.starships.service import StarshipService

logger = logging.getLogger(__name__)


@pytest.mark.anyio
class TestStarshipServce:
    """Integration tests for the film service."""

    entities: list[Starship]

    @pytest.fixture(autouse=True)
    async def setup(self, session: AsyncSession) -> None:
        self.entities = await StarshipFactory.create_batch(10)
        self.service = StarshipService(session=session)

    async def test_list(self) -> None:
        """Test listing characters."""
        result = await self.service.list(page=1, page_size=5)
        assert result.page == 1
        assert result.page_size == 5
        assert result.total >= 10
        assert len(result.items) == 5

    async def test_get(self) -> None:
        """Test getting a character by ID."""
        starship = self.entities[0]
        fetched_starship = await self.service.get(starship.id)
        assert fetched_starship.id == starship.id
        assert fetched_starship.name == starship.name

    async def test_by_url(self) -> None:
        """Test getting a character by URL."""
        starship = self.entities[0]
        fetched_starship = await self.service.by_url(starship.url)
        assert fetched_starship.id == starship.id
        assert fetched_starship.name == starship.name

    async def test_create(self) -> None:
        """Test creating a new starship."""
        new_starship_data = {
            "name": "New Starship",
            "model": "Model X",
            "manufacturer": "Starship Corp",
            "cost_in_credits": "100000",
            "length": "150",
            "max_atmosphering_speed": "900",
            "crew": "5",
            "passengers": "20",
            "cargo_capacity": "50000",
            "consumables": "2 months",
            "hyperdrive_rating": "1.0",
            "MGLT": "75",
            "starship_class": "Freighter",
            "url": "http://swapi.dev/api/starships/99/",
        }
        new_starship = Starship.from_dict(new_starship_data)
        created_starship = await self.service.create(new_starship)
        assert created_starship.id is not None
        assert created_starship.name == new_starship_data["name"]

    async def test_search(self) -> None:
        """Test searching characters by name."""
        starship = self.entities[0]
        results = await self.service.search(query=starship.name[:3])
        assert len(results) >= 1

    async def test_add_starships(self) -> None:
        """Test adding multiple starships."""
        new_starships_data = [
            {
                "name": "Another New Starship",
                "model": "Model Y",
                "manufacturer": "Starship Inc",
                "cost_in_credits": "150000",
                "length": "200",
                "max_atmosphering_speed": "850",
                "crew": "10",
                "passengers": "30",
                "cargo_capacity": "60000",
                "consumables": "3 months",
                "hyperdrive_rating": "1.5",
                "MGLT": "70",
                "starship_class": "Cruiser",
                "url": "http://swapi.dev/api/starships/100/",
            },
            {
                "name": "Yet Another Starship",
                "model": "Model Z",
                "manufacturer": "Galactic Ships",
                "cost_in_credits": "200000",
                "length": "250",
                "max_atmosphering_speed": "800",
                "crew": "15",
                "passengers": "40",
                "cargo_capacity": "70000",
                "consumables": "4 months",
                "hyperdrive_rating": "2.0",
                "MGLT": "65",
                "starship_class": "Battleship",
                "url": "http://swapi.dev/api/starships/101/",
            },
        ]
        await self.service.add_starships(new_starships_data)
        for starship_data in new_starships_data:
            starship = await self.service.by_url(starship_data["url"])
            assert starship.name == starship_data["name"]
