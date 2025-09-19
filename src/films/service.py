import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ORMNotFoundException
from src.films.models import Film
from src.films.repository import FilmRepository
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)

logger = logging.getLogger(__name__)


class FilmService(
    CreateORMService[Film],
    GetORMService[Film],
    ListPaginationORMService[Film],
    SearchORMService[Film],
):
    """Film service."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = FilmRepository(session)
        super().__init__(repository=self._repository)

    async def add_films(self, films: list[dict]) -> None:
        """Add multiple films in DB."""
        async with self.session.begin():
            for film_data in films:
                film = Film.from_dict(data=film_data)
                logger.debug(f"Syncing film: {film.title}")
                try:
                    await self.by_url(url=film.url)
                except ORMNotFoundException:
                    await self.create(obj=film)

            await self.session.commit()
