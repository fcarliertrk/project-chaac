import logging

from project_chaac.celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(name="project_chaac.add")
def add(x: int, y: int) -> int:
    result = x + y
    logger.info("add(%s, %s) = %s", x, y, result)
    return result


@celery.task(name="project_chaac.process_job")
def process_job(job: dict) -> dict:
    # Thin task: log, "process", return. Step 8 swaps the body for a real DB write.
    logger.info("processing job for partner=%s", job.get("partner_id"))
    # ... real work would happen here ...
    logger.info("job processed: %s", job)
    return {"processed": True, "partner_id": job.get("partner_id")}