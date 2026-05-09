from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.auto_apply import ApplicationResult, AutoApplyRunResponse
from services.auto_apply_orchestrator import RunState, get_all_runs, get_run, start_run

router = APIRouter()


@router.post("/run", status_code=202)
def trigger_run(db: Session = Depends(get_db)):
    try:
        run_id = start_run(db)
        return {
            "run_id": run_id,
            "status": "RUNNING",
            "message": f"Run started. Poll GET /api/v1/auto-apply/runs/{run_id} for status.",
        }
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/runs/{run_id}", response_model=AutoApplyRunResponse)
def get_run_status(run_id: str):
    state = get_run(run_id)
    if not state:
        raise HTTPException(404, "Run not found")
    return _to_response(state)


@router.get("/runs", response_model=List[AutoApplyRunResponse])
def list_runs():
    return [_to_response(s) for s in get_all_runs()]


def _to_response(s: RunState) -> AutoApplyRunResponse:
    return AutoApplyRunResponse(
        run_id=s.run_id,
        status=s.status,
        jobs_found=s.jobs_found,
        jobs_matched=s.jobs_matched,
        applications_submitted=s.applications_submitted,
        applications_failed=s.applications_failed,
        results=[ApplicationResult(**r.__dict__) for r in s.results],
        started_at=s.started_at,
        completed_at=s.completed_at,
        error=s.error,
    )
