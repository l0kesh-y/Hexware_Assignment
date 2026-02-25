from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.job_service import JobService
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.create_job(job)

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.get_job(job_id)

@router.get("/", response_model=list[JobResponse])
def get_all_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.get_all_jobs(skip, limit)

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.update_job(job_id, job_data)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    service = JobService(db)
    service.delete_job(job_id)
