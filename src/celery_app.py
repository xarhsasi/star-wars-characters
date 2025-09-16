from logging.config import dictConfig
from typing import Any

from celery import Celery
from celery.signals import setup_logging

from src.settings import settings

app = Celery("mailgenie", broker=settings.CELERY_CONFIG.broker_url)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings.CELERY_CONFIG)

# Load task modules from all domains.
app.autodiscover_tasks(packages=[])


@setup_logging.connect
def config_loggers(*args: Any, **kwags: Any) -> None:
    """
    Configures the loggers for the application using the logging configuration
    specified in the settings.
    """
    dictConfig(settings.LOGGING_CONFIG)
