from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.characters.models import Base
from src.main import app
from src.utils.session import get_session

# Use an in-memory SQLite database for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


# ---------------------------------------------------------------------------- #
#                               DB Fixtures                                    #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        TEST_DB_URL,
        poolclass=StaticPool,  # keep one connection for :memory:
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with Session() as s:
        yield s


@pytest.fixture
async def client(session: AsyncSession):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------- #
#                           Generic Fixtures                                   #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Fixture to specify the backend for AnyIO.

    Returns:
        str: The backend name for AnyIO, which is 'asyncio'.
    """
    return "asyncio"
