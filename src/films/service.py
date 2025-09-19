from sqlalchemy.ext.asyncio import AsyncSession

from src.films.models import Film
from src.films.repository import FilmRepository
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)


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
