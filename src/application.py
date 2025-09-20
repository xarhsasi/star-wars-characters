"""Module containing FastAPI instance related functions and classes."""

import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.characters.router import characters_router
from src.films.router import films_router
from src.routers import base_router
from src.settings import settings
from src.starships.router import starships_router
from src.users.router import users_router

# from src.users.router import user_router
from src.version import __version__
from src.votes.router import votes_router

logger = logging.getLogger(__name__)


async def startup_handler() -> None:
    """Dummy startup event, it will be executed before the app is ready, such
    as loading ml model, creating superuser in DB etc."""
    logger.info("Starting up ...")


async def shutdown_handler() -> None:
    """Dummy shutdown event, it will be executed before the app is shutting
    down, such as removing temporary files, close DB connection etc."""
    logger.info("Shutting down ...")


def create_application() -> FastAPI:
    """Create a FastAPI instance.

    Returns:
        object of FastAPI: the fastapi application instance.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
        version=__version__,
        openapi_url=f"{settings.API_STR}/openapi.json",
    )

    # Set all CORS enabled origins
    if settings.CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # add defined routers
    application.include_router(base_router, prefix=settings.API_STR)
    application.include_router(characters_router, prefix=settings.API_STR)
    application.include_router(films_router, prefix=settings.API_STR)
    application.include_router(users_router, prefix=settings.API_STR)
    application.include_router(votes_router, prefix=settings.API_STR)
    application.include_router(starships_router, prefix=settings.API_STR)

    # event handler
    application.add_event_handler("startup", startup_handler)
    application.add_event_handler("shutdown", shutdown_handler)

    return application
