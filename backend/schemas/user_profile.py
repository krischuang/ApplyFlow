from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    current_location: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_summary: Optional[str] = None
    education_summary: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    current_location: Optional[str]
    skills: Optional[List[str]]
    experience_summary: Optional[str]
    education_summary: Optional[str]
    has_resume: bool
    created_at: datetime
    updated_at: Optional[datetime]
