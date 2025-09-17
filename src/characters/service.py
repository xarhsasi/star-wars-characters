from math import ceil
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.characters.exceptions import CharacterNotFoundException
from src.characters.models import Character
from src.characters.repository import CharacterRepository
from src.utils.schemas import Page


class CharacterService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = CharacterRepository(session)

    async def get(self, id: int) -> Character:
        """Retrieve a character by ID."""
        obj = await self._repository.get(id=id)
        if not obj:
            raise CharacterNotFoundException(id=id)
        return obj

    async def list(self, *, page: int = 1, page_size: int = 50) -> Page:
        """List all characters."""
        page = max(1, page)
        page_size = max(1, min(page_size, 1000))
        offset = (page - 1) * page_size
        items = await self._repository.list(limit=page_size, offset=offset)
        total = await self._repository.count()

        return Page(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if total else 1,
        )

    async def search(self, query: str) -> Sequence[Character]:
        """Search characters by name."""
        items = await self._repository.search(query=query)
        return items
