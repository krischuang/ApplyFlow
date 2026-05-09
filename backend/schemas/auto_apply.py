from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ApplicationResult(BaseModel):
    job_title: str
    company: str
    job_url: str
    match_score: int
    status: str   # SUBMITTED | FAILED | SKIPPED
    reason: str


class AutoApplyRunResponse(BaseModel):
    run_id: str
    status: str   # PENDING | RUNNING | COMPLETED | FAILED
    jobs_found: int
    jobs_matched: int
    applications_submitted: int
    applications_failed: int
    results: List[ApplicationResult]
    started_at: datetime
    completed_at: Optional[datetime]
    error: Optional[str]
