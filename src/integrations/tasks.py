import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.celery_app import app
from src.characters.service import CharacterService
from src.films.service import FilmService
from src.integrations.swapi.plugin import SwapiPlugin
from src.settings import settings
from src.starships.service import StarshipService

logger = logging.getLogger(__name__)


@app.task
def sync_films() -> None:
    """Sync films from a plugin to the database."""
    # Create a new async engine and session for this task
    # otherwise sessions may be shared between tasks
    _engine = create_async_engine(settings.DATABASE_URL, echo=False)
    _Session = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

    async def run():
        plugin = SwapiPlugin()
        async with _Session() as session:
            service = FilmService(session)
            films = await plugin.films()
            await service.add_films(films=films)

    return asyncio.run(run())


@app.task
def sync_characters() -> None:
    """Sync films from a plugin to the database."""
    # Create a new async engine and session for this task
    # otherwise sessions may be shared between tasks
    _engine = create_async_engine(settings.DATABASE_URL, echo=False)
    _Session = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

    async def run():
        plugin = SwapiPlugin()
        async with _Session() as session:
            service = CharacterService(session)
            characters = await plugin.characters()
            await service.add_characters(characters=characters)

    return asyncio.run(run())


@app.task
def sync_starships() -> None:
    """Sync films from a plugin to the database."""
    # Create a new async engine and session for this task
    # otherwise sessions may be shared between tasks
    _engine = create_async_engine(settings.DATABASE_URL, echo=False)
    _Session = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

    async def run():
        plugin = SwapiPlugin()
        async with _Session() as session:
            service = StarshipService(session)
            starships = await plugin.starships()
            await service.add_starships(starships=starships)

    return asyncio.run(run())


@app.task
def sync_relationships() -> None:
    """Sync relationships between films, characters and starships."""
    # Create a new async engine and session for this task
    # otherwise sessions may be shared between tasks
    _engine = create_async_engine(settings.DATABASE_URL, echo=False)
    _Session = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

    async def run():
        async with _Session() as session:
            film_service = FilmService(session)
            async for film in film_service.list_all():
                sync_film_relationships.delay(film_id=film.id)

    return asyncio.run(run())


@app.task
def sync_film_relationships(film_id: int) -> None:
    """Sync relationships for a specific film between films, characters and starships."""
    # Create a new async engine and session for this task
    # otherwise sessions may be shared between tasks
    _engine = create_async_engine(settings.DATABASE_URL, echo=False)
    _Session = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)

    async def run():
        async with _Session() as session:
            film_service = FilmService(session)
            await film_service.create_relationships(film_id=film_id)

    return asyncio.run(run())


@app.task
def sync_plugins_with_db() -> None:
    async def run():
        sync_films.delay()
        sync_characters.delay()
        sync_starships.delay()
        sync_relationships.delay()

    return asyncio.run(run())
