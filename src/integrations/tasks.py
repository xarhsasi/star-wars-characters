import asyncio
import logging

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.characters.models import Character
from src.characters.service import CharacterService
from src.films.models import Film
from src.films.service import FilmService
from src.integrations.swapi.plugin import SwapiPlugin
from src.settings import settings
from src.starships.models import Starship
from src.starships.service import StarshipService

_engine = create_async_engine(settings.DATABASE_URL, echo=False)
_Session = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)


logger = logging.getLogger(__name__)


@shared_task
def sync_films() -> int:
    """Sync films from a plugin to the database."""

    async def run():
        plugin = SwapiPlugin()
        async with _Session() as session:
            service = FilmService(session)
            films = await plugin.films()
            for film in films:
                isntance_obj = Film.from_dict(data=film)
                logger.debug(f"Syncing film: {film.title}")
                await service.create(obj=isntance_obj)
            await session.commit()

    return asyncio.run(run())


@shared_task
def sync_characters() -> int:
    """Sync films from a plugin to the database."""

    async def run():
        plugin = SwapiPlugin()
        async with _Session() as session:
            service = CharacterService(session)
            characters = await plugin.characters()
            for character in characters:
                instance_obj = Character.from_dict(data=character)
                logger.debug(f"Syncing character: {instance_obj.name}")
                await service.create(obj=instance_obj)
            await session.commit()

    return asyncio.run(run())


@shared_task
def sync_starships() -> int:
    """Sync films from a plugin to the database."""

    async def run():
        plugin = SwapiPlugin()
        async with _Session() as session:
            service = StarshipService(session)
            starships = await plugin.starships()
            for starship in starships:
                instance_obj = Starship.from_dict(data=starship)
                logger.debug(f"Syncing starship: {instance_obj.name}")
                await service.create(obj=instance_obj)
            await session.commit()

    return asyncio.run(run())


@shared_task
def sync_plugins_with_db() -> int:
    async def run():
        sync_films.delay()
        sync_characters.delay()
        sync_starships.delay()

    return asyncio.run(run())
