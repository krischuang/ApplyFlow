from typing import Optional
from pydantic import BaseModel


class JobPreferencesUpdate(BaseModel):
    preferred_location: Optional[str] = None
    min_salary_aud: Optional[int] = None
    max_salary_aud: Optional[int] = None
    tech_stack: Optional[str] = None
    seniority_level: Optional[str] = None
    max_applications_per_run: Optional[int] = None
    match_score_threshold: Optional[int] = None


class JobPreferencesResponse(BaseModel):
    id: Optional[int]
    preferred_location: str
    min_salary_aud: Optional[int]
    max_salary_aud: Optional[int]
    tech_stack: Optional[str]
    seniority_level: str
    max_applications_per_run: int
    match_score_threshold: int

    model_config = {"from_attributes": True}
