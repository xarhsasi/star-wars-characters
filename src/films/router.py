"""This module contains the characters router for the FastAPI application."""

import logging

from fastapi import APIRouter, HTTPException, Path, Query

from src.depends import FilmServiceDI
from src.exceptions import ORMNotFoundException
from src.films.schemas import FilmOut
from src.utils.schemas import Page

logger = logging.getLogger(__name__)

films_router = APIRouter(
    prefix="/film",
    tags=["films"],
)


@films_router.get("/search/", description="Search films", response_model=list[FilmOut])
async def search_films(
    FilmServiceDI: FilmServiceDI,
    query: str = Query(min_length=1),
) -> list[FilmOut]:
    """Search characters by name."""
    characters = await FilmServiceDI.search(query=query)
    return characters


@films_router.get("/", description="GET films", response_model=Page[FilmOut])
async def list_films(
    FilmServiceDI: FilmServiceDI,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
) -> Page[FilmOut]:
    """Fetch and store all characters in DB."""
    characters = await FilmServiceDI.list(page=page, page_size=page_size)
    return characters


@films_router.get("/{id}/", description="GET films", response_model=FilmOut)
async def retrieve_films(
    FilmServiceDI: FilmServiceDI, id: int = Path(..., ge=1)
) -> FilmOut:
    """Fetch and store all characters in DB."""
    try:
        character = await FilmServiceDI.get(id=id)
    except ORMNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return FilmOut.model_validate(character)
