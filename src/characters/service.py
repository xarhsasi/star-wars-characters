import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.characters.models import Character
from src.characters.repository import CharacterRepository
from src.exceptions import ORMNotFoundException
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)

logger = logging.getLogger(__name__)


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

    async def add_characters(self, characters: list[dict]) -> None:
        """Add multiple characters in DB."""
        async with self.session.begin():
            for character_data in characters:
                character = Character.from_dict(data=character_data)
                logger.debug(f"Syncing character: {character.name}")
                try:
                    await self.by_url(url=character.url)
                except ORMNotFoundException:
                    await self.create(obj=character)
