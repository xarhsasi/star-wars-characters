"""This module contains the characters router for the FastAPI application."""

import logging

from fastapi import APIRouter, HTTPException, Path, Query

from src.characters.schemas import CharacterOut
from src.depends import CharacterServiceDI
from src.exceptions import ORMNotFoundException
from src.utils.schemas import Page

logger = logging.getLogger(__name__)

characters_router = APIRouter(
    prefix="/character",
    tags=["characters"],
)


@characters_router.get(
    "/search/", description="Search characters", response_model=list[CharacterOut]
)
async def search_characters(
    CharacterServiceDI: CharacterServiceDI,
    query: str = Query(min_length=1),
) -> list[CharacterOut]:
    """Search characters by name."""
    characters = await CharacterServiceDI.search(query=query)
    return characters


@characters_router.get(
    "/", description="GET characters", response_model=Page[CharacterOut]
)
async def list_characters(
    CharacterServiceDI: CharacterServiceDI,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
) -> Page[CharacterOut]:
    """Fetch and store all characters in DB."""
    characters = await CharacterServiceDI.list(page=page, page_size=page_size)
    return characters


@characters_router.get(
    "/{id}/", description="GET characters", response_model=CharacterOut
)
async def retrieve_character(
    CharacterServiceDI: CharacterServiceDI, id: int = Path(..., ge=1)
) -> CharacterOut:
    """Fetch and store all characters in DB."""
    try:
        character = await CharacterServiceDI.get(id=id)
    except ORMNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return CharacterOut.model_validate(character)
