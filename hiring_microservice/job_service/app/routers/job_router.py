from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.job_service import JobService
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse
from typing import List, Optional

router = APIRouter(prefix="/jobs", tags=["Jobs"])

def get_job_service(db: Session = Depends(get_db)):
    return JobService(db)

@router.post("/", response_model=JobResponse)
def create_job(
    payload: JobCreate,
    job_service: JobService = Depends(get_job_service)
):
    return job_service.create_job(payload)

@router.get("/", response_model=List[JobResponse])
def get_all_jobs(
    company_id: Optional[int] = Query(None),
    job_service: JobService = Depends(get_job_service)
):
    if company_id:
        return job_service.get_jobs_by_company(company_id)
    return job_service.get_all_jobs()

@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    job_service: JobService = Depends(get_job_service)
):
    return job_service.get_job_by_id(job_id)

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    payload: JobUpdate,
    job_service: JobService = Depends(get_job_service)
):
    return job_service.update_job(job_id, payload)

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    job_service: JobService = Depends(get_job_service)
):
    job_service.delete_job(job_id)
    return {"message": "Job deleted successfully"}
