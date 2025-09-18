"""This module contains the characters router for the FastAPI application."""

import logging

from fastapi import APIRouter, HTTPException, Path, Query

from src.characters.exceptions import CharacterNotFoundException
from src.depends import FilmServiceDI, StarshipServiceDI
from src.films.schemas import FilmOut
from src.starships.schemas import StarshipOut
from src.utils.schemas import Page

logger = logging.getLogger(__name__)

starships_router = APIRouter(
    prefix="/starship",
    tags=["starships"],
)


@starships_router.get(
    "/search/", description="Search starships", response_model=list[StarshipOut]
)
async def search_starships(
    StarshipServiceDI: StarshipServiceDI,
    query: str = Query(min_length=1),
) -> list[StarshipOut]:
    """Search starships by name."""
    characters = await StarshipServiceDI.search(query=query)
    return characters


@starships_router.get(
    "/", description="GET all starships", response_model=Page[StarshipOut]
)
async def list_starships(
    StarshipServiceDI: StarshipServiceDI,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
) -> Page[StarshipOut]:
    """Fetch and store all starships in DB."""
    characters = await StarshipServiceDI.list(page=page, page_size=page_size)
    return characters


@starships_router.get("/{id}/", description="GET starship", response_model=StarshipOut)
async def retrieve_starship(
    StarshipServiceDI: StarshipServiceDI, id: int = Path(..., ge=1)
) -> StarshipOut:
    """Fetch and store all starships in DB."""
    try:
        character = await StarshipServiceDI.get(id=id)
    except CharacterNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return StarshipOut.model_validate(character)
