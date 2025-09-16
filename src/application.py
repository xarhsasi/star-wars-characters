"""Module containing FastAPI instance related functions and classes."""

# mypy: ignore-errors
import logging

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

# from src.db.session import engine
# from src.middlewares.log import log_time
from src.models import Base
from src.routers import base_router
from src.settings import settings

# from src.users.router import user_router
from src.version import __version__

logger = logging.getLogger(__name__)


async def startup_handler() -> None:
    """Dummy startup event, it will be executed before the app is ready, such
    as loading ml model, creating superuser in DB etc."""
    logger.info("Starting up ...")


async def shutdown_handler() -> None:
    """Dummy shutdown event, it will be executed before the app is shutting
    down, such as removing temporary files, close DB connection etc."""
    logger.info("Shutting down ...")


# def create_db_tables():
#     """Create all tables in database."""
#     Base.metadata.create_all(bind=engine)


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
    # application.include_router(user_router, prefix=settings.API_STR)

    # event handler
    application.add_event_handler("startup", startup_handler)
    application.add_event_handler("shutdown", shutdown_handler)

    # load logging config
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # add defined middleware functions
    # application.add_middleware(BaseHTTPMiddleware, dispatch=log_time)

    return application
