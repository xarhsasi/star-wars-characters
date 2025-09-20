from __future__ import annotations

from math import ceil
from typing import AsyncGenerator, Generic, Sequence, TypeVar

import sqlalchemy
import sqlalchemy.exc

from src.exceptions import ORMDuplicateException, ORMNotFoundException
from src.repository import Repository
from src.utils.schemas import Page

_T = TypeVar("_T")  # ORM model type


class ORMBaseService(Generic[_T]):
    """Base service for ORM models."""

    def __init__(self, repository: Repository):
        self._repository = repository


class CreateORMService(ORMBaseService, Generic[_T]):
    """Create a new ORM model."""

    async def create(self, obj: _T) -> _T:
        """Create an new orm."""
        try:
            model = await self._repository.create(obj=obj)
        except sqlalchemy.exc.IntegrityError as e:
            raise ORMDuplicateException() from e
        return model


class GetORMService(ORMBaseService, Generic[_T]):
    """Get a single ORM model by ID."""

    async def get(self, id: int) -> _T:
        """Retrieve an orm by ID."""
        obj = await self._repository.get(id=id)
        if not obj:
            raise ORMNotFoundException(id=id)
        return obj

    async def by_url(self, url: str) -> _T:
        """Retrieve an orm by URL."""
        obj = await self._repository.by_url(url=url)
        if not obj:
            raise ORMNotFoundException(id=url)
        return obj


class ListPaginationORMService(ORMBaseService, Generic[_T]):
    """List all ORM models with pagination."""

    BATCH_SIZE = 50

    async def list(self, *, page: int = 1, page_size: int = BATCH_SIZE) -> Page:
        """List all orm."""
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

    async def list_all(self) -> AsyncGenerator[Sequence[_T]]:
        """List all orm without pagination."""
        offset = 0
        while True:
            batch = await self._repository.list(limit=self.BATCH_SIZE, offset=offset)
            if not batch:
                break
            for item in batch:
                yield item
            offset += self.BATCH_SIZE


class UpdateORMService(ORMBaseService, Generic[_T]):
    """Update an existing ORM model."""

    async def update(self, id: int, attrs: dict) -> _T:
        """Update an existing orm."""
        existing_obj = await self._repository.get(id=id)
        if not existing_obj:
            raise ORMNotFoundException(id=id)

        return await self._repository.update(id=id, attrs=attrs)


class SearchORMService(ORMBaseService, Generic[_T]):
    """Search ORM models by a specific attribute."""

    async def search(self, query: str) -> Sequence[_T]:
        """Search orm by name."""
        items = await self._repository.search(query=query)
        return items
