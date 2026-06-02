from pydantic import BaseModel, ConfigDict, Field


class JobRequest(BaseModel):
    # forbid unknown fields — strict format validation, rejects typo'd/extra keys with 422
    model_config = ConfigDict(extra="forbid")

    partner_id: str = Field(min_length=1, description="Identifier of the requesting partner")
    payload: dict = Field(description="Arbitrary job data to be processed by the worker")
    priority: int = Field(default=5, ge=1, le=10, description="1 (highest) to 10 (lowest)")


class JobAccepted(BaseModel):
    task_id: str
    status: str = "accepted"

class JobResult(BaseModel):
    task_id: str
    status: str            # PENDING, STARTED, SUCCESS, FAILURE, etc.
    result: dict | None = None