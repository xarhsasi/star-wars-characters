import http
from typing import Annotated

from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.characters.service import CharacterService
from src.films.service import FilmService
from src.starships.service import StarshipService
from src.users.service import UserService
from src.utils.jwt import JwtAuthenticationService, JwtHTTPBearer
from src.utils.session import get_session
from src.votes.service import VoteService


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


def get_starship_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> StarshipService:
    return StarshipService(session)


StarshipServiceDI = Annotated[StarshipService, Depends(get_starship_service)]


def get_vote_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> VoteService:
    return VoteService(session)


VoteServiceDI = Annotated[VoteService, Depends(get_vote_service)]


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    return UserService(session)


UserServiceDI = Annotated[UserService, Depends(get_user_service)]


jwt_bearer = JwtHTTPBearer(auth_service=JwtAuthenticationService())


async def get_user_id(
    token: Annotated[str, Depends(jwt_bearer)],
):
    """
    Decode token again to read claims (JwtHTTPBearer only checks validity).
    Fetch the user and return it, or raise 401/403 as needed.
    """
    auth = JwtAuthenticationService()
    try:
        payload = auth.verify(token)
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
