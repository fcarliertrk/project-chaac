from celery import Celery

from project_chaac.config import settings

celery = Celery(
    "project_chaac",
    broker=settings.broker_url,
    include=["project_chaac.tasks"],  # explicit registration — imported at worker startup
    # no `backend=` — we're skipping the result backend for v1
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)