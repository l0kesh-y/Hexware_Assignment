from sqlalchemy.orm import Session
from app.repositories.job_repository import JobRepository
from app.schemas.job_schema import JobCreate, JobUpdate
from app.exceptions.custom_exceptions import JobNotFoundException

class JobService:
    def __init__(self, db: Session):
        self.repository = JobRepository(db)
        self.db = db
    
    def create_job(self, job: JobCreate):
        try:
            return self.repository.create_job(job)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_job(self, job_id: int):
        job = self.repository.get_job(job_id)
        if not job:
            raise JobNotFoundException(f"Job with id {job_id} not found")
        return job
    
    def get_all_jobs(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_jobs(skip, limit)
    
    def update_job(self, job_id: int, job_data: JobUpdate):
        job = self.repository.get_job(job_id)
        if not job:
            raise JobNotFoundException(f"Job with id {job_id} not found")
        
        try:
            return self.repository.update_job(job_id, job_data)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_job(self, job_id: int):
        job = self.repository.get_job(job_id)
        if not job:
            raise JobNotFoundException(f"Job with id {job_id} not found")
        return self.repository.delete_job(job_id)
