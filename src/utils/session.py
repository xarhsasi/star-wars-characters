"""Define a session instance for doing all database related operations inside the app."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings import settings

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class AsyncDBContextManager:
    """A context manager for creating an async session instance for database
    operations."""

    def __init__(self) -> None:
        session = sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.session = session()

    async def __aenter__(self) -> Any:
        return self.session

    async def __aexit__(self, *exc: Any) -> Any:
        await self.session.close()
