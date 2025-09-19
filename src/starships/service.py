from sqlalchemy.ext.asyncio import AsyncSession

from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)
from src.starships.models import Starship
from src.starships.repository import StarshipRepository


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
