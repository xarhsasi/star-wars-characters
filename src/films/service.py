import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.characters.repository import CharacterRepository
from src.exceptions import ORMNotFoundException
from src.films.models import Film
from src.films.repository import FilmRepository
from src.integrations.swapi.plugin import SwapiPlugin
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    SearchORMService,
)
from src.starships.repository import StarshipRepository

logger = logging.getLogger(__name__)


class FilmService(
    CreateORMService[Film],
    GetORMService[Film],
    ListPaginationORMService[Film],
    SearchORMService[Film],
):
    """Film service."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = FilmRepository(session)
        super().__init__(repository=self._repository)

    async def add_films(self, films: list[dict]) -> None:
        """Add multiple films in DB."""
        async with self.session.begin():
            for film_data in films:
                film = Film.from_dict(data=film_data)
                logger.debug(f"Syncing film: {film.title}")
                try:
                    film = await self.by_url(url=film.url)
                except ORMNotFoundException:
                    film = await self.create(obj=film)

    async def create_relationships(self, film_id: int) -> None:
        """Create relationships between film and characters."""
        character_repo = CharacterRepository(self.session)
        starship_repo = StarshipRepository(self.session)
        plugin = SwapiPlugin()

        # Find the relationships from the plugin
        film_data = await plugin.film(film_id)
        async with self.session.begin():
            film = await self.get(id=film_id)

            await self.session.refresh(film, attribute_names=["characters"])
            for character_url in film_data["characters"]:
                character = await character_repo.by_url(url=character_url)
                if character not in film.characters:
                    logger.debug(
                        f"Linking character {character.name} to film {film.title}"
                    )
                    film.characters.append(character)

            await self.session.refresh(film, attribute_names=["starships"])
            for starship_url in film_data["starships"]:
                starship = await starship_repo.by_url(url=starship_url)
                if starship not in film.starships:
                    logger.debug(
                        f"Linking starship {starship.name} to film {film.title}"
                    )
                    film.starships.append(starship)
