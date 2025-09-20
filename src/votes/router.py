"""This module contains the characters router for the FastAPI application."""

import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query

from src.depends import VoteServiceDI, get_user_id
from src.exceptions import (
    ORMDuplicateException,
    ORMNotFoundException,
    ServicePermissionDenied,
)
from src.utils.schemas import Page
from src.votes.schemas import VoteOut

logger = logging.getLogger(__name__)

votes_router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)


@votes_router.post("/vote", description="Vote a film", response_model=VoteOut)
async def vote_film(
    VoteServiceDI: VoteServiceDI,
    user_id: int = Depends(get_user_id),
    vote_id: int = Body(..., ge=1),
    score: int = Body(..., ge=1, le=5),
    feedback: str | None = Body(None, max_length=500),
) -> VoteOut:
    """Fetch and store all characters in DB."""
    try:
        vote = await VoteServiceDI.vote(
            vote_id=vote_id, user_id=user_id, score=score, feedback=feedback
        )
    except ORMDuplicateException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) from e
    except ServicePermissionDenied as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) from e

    return VoteOut.model_validate(vote)


@votes_router.get("/", description="GET all votes", response_model=Page[VoteOut])
async def list_films(
    VoteServiceDI: VoteServiceDI,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
) -> Page[VoteOut]:
    """Fetch and store all characters in DB."""
    votes = await VoteServiceDI.list(page=page, page_size=page_size)
    return votes


@votes_router.get("/{id}/", description="GET vote", response_model=VoteOut)
async def retrieve_vote(
    VoteServiceDI: VoteServiceDI, id: int = Path(..., ge=1)
) -> VoteOut:
    """Fetch and store all characters in DB."""
    try:
        vote = await VoteServiceDI.get(id=id)
    except ORMNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e

    return VoteOut.model_validate(vote)
