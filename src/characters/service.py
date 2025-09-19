from sqlalchemy.ext.asyncio import AsyncSession

from src.characters.models import Character
from src.characters.repository import CharacterRepository
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)


class CharacterService(
    CreateORMService[Character],
    GetORMService[Character],
    ListPaginationORMService[Character],
    SearchORMService[Character],
):
    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = CharacterRepository(session)
        super().__init__(repository=self._repository)
