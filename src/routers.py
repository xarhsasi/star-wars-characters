"""This module contains the base router for the FastAPI application."""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

base_router = APIRouter()


@base_router.get("/ht/", description="Health check", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint to check the status of the service."""
    return {"status": "UP"}


@base_router.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    """Redirect to the docs page."""
    return RedirectResponse(url="/docs")
