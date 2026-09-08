import enum
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Integer, String, Text
from database import Base, utcnow_naive


class ApplicationStatus(str, enum.Enum):
    SAVED = "SAVED"
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    FAILED = "FAILED"


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    job_url = Column(String)
    location = Column(String)
    salary_range = Column(String)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.SAVED, nullable=False)
    notes = Column(Text)
    applied_date = Column(Date)
    match_score = Column(Integer)
    auto_applied = Column(Boolean, default=False)
    cover_letter_used = Column(Text)
    source_job_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=utcnow_naive, nullable=False)
    updated_at = Column(DateTime, default=utcnow_naive, onupdate=utcnow_naive, nullable=False)
