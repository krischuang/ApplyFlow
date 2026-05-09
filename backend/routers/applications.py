from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.job_application import ApplicationStatus, JobApplication
from schemas.job_application import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate

router = APIRouter()


@router.post("", response_model=JobApplicationResponse, status_code=201)
def create(data: JobApplicationCreate, db: Session = Depends(get_db)):
    app = JobApplication(**data.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.get("", response_model=List[JobApplicationResponse])
def list_all(status: Optional[ApplicationStatus] = None, db: Session = Depends(get_db)):
    q = db.query(JobApplication)
    if status:
        q = q.filter(JobApplication.status == status)
    return q.order_by(JobApplication.created_at.desc()).all()


@router.get("/{app_id}", response_model=JobApplicationResponse)
def get_one(app_id: int, db: Session = Depends(get_db)):
    app = db.get(JobApplication, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    return app


@router.put("/{app_id}", response_model=JobApplicationResponse)
def update(app_id: int, data: JobApplicationUpdate, db: Session = Depends(get_db)):
    app = db.get(JobApplication, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(app, k, v)
    db.commit()
    db.refresh(app)
    return app


@router.delete("/{app_id}", status_code=204)
def delete(app_id: int, db: Session = Depends(get_db)):
    app = db.get(JobApplication, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    db.delete(app)
    db.commit()


@router.patch("/{app_id}/status", response_model=JobApplicationResponse)
def update_status(app_id: int, status: ApplicationStatus, db: Session = Depends(get_db)):
    app = db.get(JobApplication, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    app.status = status
    db.commit()
    db.refresh(app)
    return app
