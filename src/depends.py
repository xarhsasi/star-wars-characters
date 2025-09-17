from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.characters.service import CharacterService
from src.films.service import FilmService
from src.utils.session import get_session


# --- DI helpers ---
def get_character_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CharacterService:
    return CharacterService(session)


CharacterServiceDI = Annotated[CharacterService, Depends(get_character_service)]


def get_film_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FilmService:
    return FilmService(session)


FilmServiceDI = Annotated[FilmService, Depends(get_film_service)]
