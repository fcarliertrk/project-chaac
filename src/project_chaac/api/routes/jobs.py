from fastapi import APIRouter, Depends, status

from project_chaac.api.dependencies import verify_api_key, verify_client_ip
from project_chaac.api.schemas import JobAccepted, JobRequest
from project_chaac.tasks import process_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post(
    "",
    response_model=JobAccepted,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(verify_client_ip)],
)
async def create_job(
    request: JobRequest,
    api_key: str = Depends(verify_api_key),
) -> JobAccepted:
    # validated + authenticated by this point. Enqueue and return immediately.
    result = process_job.delay(request.model_dump())
    return JobAccepted(task_id=result.id)