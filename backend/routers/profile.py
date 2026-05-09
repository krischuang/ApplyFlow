import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from models.job_preferences import JobPreferences
from models.user_profile import UserProfile
from schemas.job_preferences import JobPreferencesResponse, JobPreferencesUpdate
from schemas.user_profile import UserProfileResponse, UserProfileUpdate
from services.resume_parser import process_resume

router = APIRouter()


# ── Resume ────────────────────────────────────────────────────────────────────

@router.post("/resume", response_model=UserProfileResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    try:
        content = await file.read()
        result = process_resume(content, file.filename or "resume.pdf")
        parsed = result["parsed"]

        profile = db.query(UserProfile).first() or UserProfile()
        profile.full_name = parsed.get("fullName", "")
        profile.email = parsed.get("email", "")
        profile.phone = parsed.get("phone", "")
        profile.current_location = parsed.get("location", "")
        profile.skills = json.dumps(parsed.get("skills", []))
        profile.experience_summary = parsed.get("experienceSummary", "")
        profile.education_summary = parsed.get("educationSummary", "")
        profile.raw_resume_text = result["raw_text"]
        profile.resume_file_path = result["file_path"]

        if not profile.id:
            db.add(profile)
        db.commit()
        db.refresh(profile)
        return _profile_response(profile)
    except Exception as e:
        raise HTTPException(500, f"Resume processing failed: {e}")


# ── Profile ───────────────────────────────────────────────────────────────────

@router.get("", response_model=UserProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    p = db.query(UserProfile).first()
    if not p:
        raise HTTPException(404, "No profile found — upload your resume first")
    return _profile_response(p)


@router.put("", response_model=UserProfileResponse)
def update_profile(data: UserProfileUpdate, db: Session = Depends(get_db)):
    p = db.query(UserProfile).first() or UserProfile()
    if data.full_name is not None: p.full_name = data.full_name
    if data.email is not None: p.email = data.email
    if data.phone is not None: p.phone = data.phone
    if data.current_location is not None: p.current_location = data.current_location
    if data.skills is not None: p.skills = json.dumps(data.skills)
    if data.experience_summary is not None: p.experience_summary = data.experience_summary
    if data.education_summary is not None: p.education_summary = data.education_summary
    if not p.id:
        db.add(p)
    db.commit()
    db.refresh(p)
    return _profile_response(p)


# ── Preferences ───────────────────────────────────────────────────────────────

@router.get("/preferences", response_model=JobPreferencesResponse)
def get_preferences(db: Session = Depends(get_db)):
    prefs = db.query(JobPreferences).first()
    if not prefs:
        return JobPreferencesResponse(
            id=None, preferred_location="All Australia", min_salary_aud=None,
            max_salary_aud=None, tech_stack=None, seniority_level="MID",
            max_applications_per_run=5, match_score_threshold=70,
        )
    return prefs


@router.put("/preferences", response_model=JobPreferencesResponse)
def update_preferences(data: JobPreferencesUpdate, db: Session = Depends(get_db)):
    prefs = db.query(JobPreferences).first() or JobPreferences()
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(prefs, k, v)
    if not prefs.id:
        db.add(prefs)
    db.commit()
    db.refresh(prefs)
    return prefs


# ── Helpers ───────────────────────────────────────────────────────────────────

def _profile_response(p: UserProfile) -> UserProfileResponse:
    skills: list = []
    if p.skills:
        try:
            skills = json.loads(p.skills)
        except Exception:
            skills = [s.strip() for s in p.skills.split(",") if s.strip()]
    return UserProfileResponse(
        id=p.id,
        full_name=p.full_name,
        email=p.email,
        phone=p.phone,
        current_location=p.current_location,
        skills=skills,
        experience_summary=p.experience_summary,
        education_summary=p.education_summary,
        has_resume=bool(p.resume_file_path),
        created_at=p.created_at,
        updated_at=p.updated_at,
    )
