from celery import Celery

from project_chaac.config import settings

celery = Celery(
    "project_chaac",
    broker=settings.broker_url,
    backend=settings.result_backend,   # <-- now set
    include=["project_chaac.tasks"],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,   # results auto-expire after 1h (see note)
)