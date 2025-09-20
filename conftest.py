from typing import AsyncGenerator

import factory
import pytest
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.characters.models import Base, Character
from src.films.models import Film
from src.main import app
from src.starships.models import Starship
from src.utils.session import get_session

# Use an in-memory SQLite database for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


# ---------------------------------------------------------------------------- #
#                               DB Fixtures                                    #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
async def engine():
    async_engine = create_async_engine(
        TEST_DB_URL,
        poolclass=StaticPool,  # keep one connection for memory
        future=True,
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield async_engine
    finally:
        await async_engine.dispose()


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


# ---------------------------------------------------------------------------- #
#                                 Factories                                    #
# ---------------------------------------------------------------------------- #
class CharacterFactory(AsyncSQLAlchemyFactory):
    """Factory for creating Character instances."""

    class Meta:
        model = Character

    name = factory.Faker("name")
    height = factory.Faker("random_int", min=100, max=220)
    hair_color = factory.Faker("color_name")
    skin_color = factory.Faker("color_name")
    eye_color = factory.Faker("color_name")
    url = factory.Sequence(lambda n: f"https://example.invalid/film-{n}")


class FilmFactory(AsyncSQLAlchemyFactory):
    """Factory for creating Film instances."""

    class Meta:
        model = Film

    title = factory.Faker("sentence", nb_words=3)
    director = factory.Faker("name")
    producer = factory.Faker("name")
    url = factory.Sequence(lambda n: f"https://example.invalid/film-{n}")


class StarshipFactory(AsyncSQLAlchemyFactory):
    """Factory for creating Starship instances."""

    class Meta:
        model = Starship

    name = factory.Faker("word")
    model = factory.Faker("word")
    starship_class = factory.Faker("word")
    url = factory.Sequence(lambda n: f"https://example.invalid/film-{n}")


@pytest.fixture(autouse=True)
async def _wire_factories(session: AsyncSession):
    """Automatically wire factories to the test session."""
    CharacterFactory._meta.sqlalchemy_session = session
    FilmFactory._meta.sqlalchemy_session = session
    StarshipFactory._meta.sqlalchemy_session = session
    yield
