import logging

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import FilmFactory
from src.films.models import Film
from src.films.service import FilmService

logger = logging.getLogger(__name__)


@pytest.mark.anyio
class TestFilmServce:
    """Integration tests for the film service."""

    entities: list[Film]

    @pytest.fixture(autouse=True)
    async def setup(self, session: AsyncSession) -> None:
        self.entities = await FilmFactory.create_batch(10)
        self.service = FilmService(session=session)

    async def test_list(self) -> None:
        """Test listing films."""
        result = await self.service.list(page=1, page_size=5)
        assert result.page == 1
        assert result.page_size == 5
        assert result.total >= 10
        assert len(result.items) == 5

    async def test_get(self) -> None:
        """Test getting a film by ID."""
        film = self.entities[0]
        fetched_film = await self.service.get(film.id)
        assert fetched_film.id == film.id
        assert fetched_film.title == film.title

    async def test_by_url(self) -> None:
        """Test getting a film by URL."""
        film = self.entities[0]
        fetched_film = await self.service.by_url(film.url)
        assert fetched_film.id == film.id
        assert fetched_film.title == film.title

    async def test_create(self) -> None:
        """Test creating a new film."""
        new_film_data = {
            "title": "New Film",
            "episode_id": 7,
            "opening_crawl": "A long time ago in a galaxy far, far away...",
            "director": "New Director",
            "producer": "New Producer",
            "release_date": "2025-01-01",
            "url": "http://swapi.dev/api/films/99/",
        }
        new_film = Film.from_dict(new_film_data)
        created_film = await self.service.create(new_film)
        assert created_film.id is not None
        assert created_film.title == new_film_data["title"]

    async def test_search(self) -> None:
        """Test searching for films."""
        film = self.entities[0]
        search_results = await self.service.search(query=film.title[:3])
        assert len(search_results) >= 1

    async def test_add_films(self) -> None:
        """Test adding multiple films."""
        new_films_data = [
            {
                "title": "Another New Film",
                "episode_id": 8,
                "opening_crawl": "Another long time ago in a galaxy far, far away...",
                "director": "Another Director",
                "producer": "Another Producer",
                "release_date": "2026-01-01",
                "url": "http://swapi.dev/api/films/100/",
            }
        ]
        await self.service.add_films(new_films_data)
        added_film = await self.service.by_url("http://swapi.dev/api/films/100/")
        assert added_film.title == "Another New Film"
