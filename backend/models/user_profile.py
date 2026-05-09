from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    current_location = Column(String)
    skills = Column(Text)           # JSON array string
    experience_summary = Column(Text)
    education_summary = Column(Text)
    raw_resume_text = Column(Text)
    resume_file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
