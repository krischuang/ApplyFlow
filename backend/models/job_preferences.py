from sqlalchemy import Column, DateTime, Integer, String
from database import Base, utcnow_naive


class JobPreferences(Base):
    __tablename__ = "job_preferences"

    id = Column(Integer, primary_key=True, index=True)
    preferred_location = Column(String, default="All Australia")
    min_salary_aud = Column(Integer)
    max_salary_aud = Column(Integer)
    tech_stack = Column(String)
    seniority_level = Column(String, default="MID")
    max_applications_per_run = Column(Integer, default=5)
    match_score_threshold = Column(Integer, default=70)
    created_at = Column(DateTime, default=utcnow_naive, nullable=False)
    updated_at = Column(DateTime, default=utcnow_naive, onupdate=utcnow_naive, nullable=False)
