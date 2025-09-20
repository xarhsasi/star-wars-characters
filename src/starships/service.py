import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ORMNotFoundException
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)
from src.starships.models import Starship
from src.starships.repository import StarshipRepository

logger = logging.getLogger(__name__)


class StarshipService(
    CreateORMService[Starship],
    GetORMService[Starship],
    ListPaginationORMService[Starship],
    SearchORMService[Starship],
):
    """Starship service."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = StarshipRepository(session)
        super().__init__(repository=self._repository)

    async def add_starships(self, starships: list[dict]) -> None:
        """Add multiple starships in DB."""
        async with self.session.begin():
            for starship_data in starships:
                starship = Starship.from_dict(data=starship_data)
                logger.debug(f"Syncing starship: {starship.name}")
                try:
                    await self.by_url(url=starship.url)
                except ORMNotFoundException:
                    await self.create(obj=starship)
