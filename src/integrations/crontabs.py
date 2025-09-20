import logging

from celery.schedules import crontab

from src.celery_app import app as celery_app
from src.integrations.tasks import sync_plugins_with_db

logger = logging.getLogger(__name__)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **_):
    """Setup periodic tasks for integrations."""
    sender.add_periodic_task(
        crontab(minute="*/1"),
        sync_plugins_with_db.s(),
        name="sync plugins with db every 1 minutes",
    )  # every 1 minutes
