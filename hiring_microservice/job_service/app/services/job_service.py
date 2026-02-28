from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.job_repository import JobRepository
from app.schemas.job_schema import (
    JobCreate,
    JobUpdate,
    JobResponse,
)
from typing import List


class JobService:

    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)

    def create_job(self, payload: JobCreate) -> JobResponse:
        job_dict = payload.model_dump()
        job = self.job_repo.create_job(job_dict)
        return JobResponse.model_validate(job)

    def get_job_by_id(self, job_id: int) -> JobResponse:
        job = self.job_repo.get_job_by_id(job_id)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )

        return JobResponse.model_validate(job)

    def get_all_jobs(self) -> List[JobResponse]:
        jobs = self.job_repo.get_all_jobs()
        return [JobResponse.model_validate(job) for job in jobs]

    def get_jobs_by_company(self, company_id: int) -> List[JobResponse]:
        jobs = self.job_repo.get_jobs_by_company(company_id)
        return [JobResponse.model_validate(job) for job in jobs]

    def update_job(self, job_id: int, payload: JobUpdate) -> JobResponse:
        job = self.job_repo.get_job_by_id(job_id)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )

        update_data = payload.model_dump(exclude_unset=True)
        updated_job = self.job_repo.update_job(job, update_data)

        return JobResponse.model_validate(updated_job)

    def delete_job(self, job_id: int):
        job = self.job_repo.get_job_by_id(job_id)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )

        self.job_repo.delete_job(job)

        return {"message": "Job deleted successfully"}
