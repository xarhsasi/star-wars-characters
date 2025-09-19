from __future__ import annotations

from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

_T = TypeVar("_T")  # ORM model type


class Repository(Generic[_T]):
    """Generic repository.

    Subclasses must set `model` to the mapped class, e.g.:

        class UserRepository(Repository[User]):
            _model = User

    This class does not handle transactions and commits .
    """

    SEARCH_QUERY_ATTR: str  # Attribute to search by in `search()`

    _model: Type[_T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: _T) -> _T:
        """Create a new object and persist it (does not commit)."""
        self.session.add(obj)
        # Ensure PKs/defaults are populated without committing.
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: int) -> _T | None:
        """Get a model by primary key."""
        return await self.session.get(self._model, id)

    async def by_url(self, url: str) -> _T | None:
        """Get a model by URL."""
        result = await self.session.execute(
            select(self._model).where(self._model.url == url)
        )
        return result.scalars().first()

    async def update(self, obj: _T) -> _T:
        """Persist changes to an object."""
        merged = await self.session.merge(obj)  # returns the persistent instance
        await self.session.flush()
        await self.session.refresh(merged)
        return merged

    async def delete(self, obj: _T) -> None:
        """Delete an object."""
        await self.session.delete(obj)
        await self.session.flush()

    async def list(self, *, limit: int, offset: int) -> Sequence[_T]:
        """Return all rows of the model."""
        result = await self.session.execute(
            select(self._model).order_by(self._model.id).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self._model)
        return await self.session.scalar(stmt)

    async def search(self, query: str) -> Sequence[_T]:
        """Search rows of the model by name. Default limit is 100."""
        attr = getattr(self._model, self.SEARCH_QUERY_ATTR)
        if not attr:
            raise RuntimeError("Query attribute is not set")
        stmt = (
            select(self._model)
            .where(attr.ilike(f"%{query}%"))
            .order_by(self._model.id)
            .limit(50)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
