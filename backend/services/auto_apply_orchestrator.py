import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from services import seek_scraper, seek_applier, claude_service

logger = logging.getLogger(__name__)


@dataclass
class ApplicationResult:
    job_title: str
    company: str
    job_url: str
    match_score: int
    status: str   # SUBMITTED | FAILED | SKIPPED
    reason: str


@dataclass
class RunState:
    run_id: str
    status: str = "PENDING"
    jobs_found: int = 0
    jobs_matched: int = 0
    applications_submitted: int = 0
    applications_failed: int = 0
    results: list = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


_runs: dict[str, RunState] = {}
_lock = threading.Lock()


def start_run(db) -> str:
    from models.user_profile import UserProfile
    from models.job_preferences import JobPreferences

    profile = db.query(UserProfile).first()
    if not profile:
        raise ValueError("No user profile found. Upload your resume at POST /api/v1/profile/resume first.")

    prefs = db.query(JobPreferences).first()

    run_id = str(uuid.uuid4())
    state = RunState(run_id=run_id)
    with _lock:
        _runs[run_id] = state

    # Snapshot DB objects as plain dicts before passing to background thread
    profile_dict = {
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "current_location": profile.current_location,
        "skills": profile.skills,
        "experience_summary": profile.experience_summary,
        "resume_file_path": profile.resume_file_path,
    }
    prefs_dict = {
        "preferred_location": (prefs.preferred_location if prefs else None) or "All Australia",
        "max_applications_per_run": (prefs.max_applications_per_run if prefs else None) or 5,
        "match_score_threshold": (prefs.match_score_threshold if prefs else None) or 70,
    }

    thread = threading.Thread(target=_run, args=(run_id, state, profile_dict, prefs_dict), daemon=True)
    thread.start()
    return run_id


def _run(run_id: str, state: RunState, profile: dict, prefs: dict) -> None:
    from database import SessionLocal
    from models.job_application import JobApplication, ApplicationStatus

    db = SessionLocal()
    try:
        state.status = "RUNNING"
        logger.info("Run %s started", run_id)

        # 1. Scrape Seek
        raw_jobs = seek_scraper.scrape_jobs(prefs["preferred_location"])
        state.jobs_found = len(raw_jobs)

        # 2. Enrich descriptions and score each job
        scored: list[tuple] = []
        for job in raw_jobs:
            enriched = seek_scraper.enrich_with_description(job)
            if enriched.description:
                score = claude_service.score_job_match(enriched.description, profile)
                logger.debug("'%s' scored %d", job.title, score)
                if score >= prefs["match_score_threshold"]:
                    scored.append((enriched, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        state.jobs_matched = len(scored)

        # 3. Apply to top-N matches
        limit: int = prefs["max_applications_per_run"]
        for job, score in scored[:limit]:
            already = db.query(JobApplication).filter_by(source_job_id=job.seek_job_id).first()
            if already:
                state.results.append(ApplicationResult(job.title, job.company, job.job_url, score, "SKIPPED", "Already applied"))
                continue

            try:
                cover_letter = claude_service.generate_cover_letter(job.description, profile)
                success = seek_applier.apply(job, profile, cover_letter)

                application = JobApplication(
                    job_title=job.title,
                    company_name=job.company,
                    job_url=job.job_url,
                    location=job.location,
                    salary_range=job.salary_range,
                    status=ApplicationStatus.APPLIED if success else ApplicationStatus.FAILED,
                    match_score=score,
                    auto_applied=True,
                    cover_letter_used=cover_letter,
                    source_job_id=job.seek_job_id,
                    applied_date=date.today() if success else None,
                )
                db.add(application)
                db.commit()

                if success:
                    state.applications_submitted += 1
                else:
                    state.applications_failed += 1

                state.results.append(ApplicationResult(
                    job.title, job.company, job.job_url, score,
                    "SUBMITTED" if success else "FAILED",
                    "Applied via Seek Quick Apply" if success else "Form submission failed",
                ))
                time.sleep(3)   # polite delay between submissions

            except Exception as e:
                logger.error("Apply error for '%s': %s", job.title, e)
                state.applications_failed += 1
                state.results.append(ApplicationResult(job.title, job.company, job.job_url, score, "FAILED", str(e)))

        state.status = "COMPLETED"
        state.completed_at = datetime.now()
        logger.info("Run %s completed — %d submitted, %d failed", run_id, state.applications_submitted, state.applications_failed)

    except Exception as e:
        logger.error("Run %s crashed: %s", run_id, e)
        state.status = "FAILED"
        state.error = str(e)
        state.completed_at = datetime.now()
    finally:
        db.close()


def get_run(run_id: str) -> Optional[RunState]:
    return _runs.get(run_id)


def get_all_runs() -> list[RunState]:
    return list(_runs.values())
