from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from models.job_application import ApplicationStatus


class JobApplicationCreate(BaseModel):
    job_title: str
    company_name: str
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: Optional[ApplicationStatus] = ApplicationStatus.SAVED
    notes: Optional[str] = None
    applied_date: Optional[date] = None


class JobApplicationUpdate(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    applied_date: Optional[date] = None


class JobApplicationResponse(BaseModel):
    id: int
    job_title: str
    company_name: str
    job_url: Optional[str]
    location: Optional[str]
    salary_range: Optional[str]
    status: ApplicationStatus
    notes: Optional[str]
    applied_date: Optional[date]
    match_score: Optional[int]
    auto_applied: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
