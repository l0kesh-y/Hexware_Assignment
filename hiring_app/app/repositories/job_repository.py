from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job_schema import JobCreate, JobUpdate

class JobRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_job(self, job: JobCreate):
        db_job = Job(**job.model_dump())
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job
    
    def get_job(self, job_id: int):
        return self.db.query(Job).filter(Job.id == job_id).first()
    
    def get_all_jobs(self, skip: int = 0, limit: int = 10):
        return self.db.query(Job).offset(skip).limit(limit).all()
    
    def update_job(self, job_id: int, job_data: JobUpdate):
        db_job = self.get_job(job_id)
        if db_job:
            for key, value in job_data.model_dump(exclude_unset=True).items():
                setattr(db_job, key, value)
            self.db.commit()
            self.db.refresh(db_job)
        return db_job
    
    def delete_job(self, job_id: int):
        db_job = self.get_job(job_id)
        if db_job:
            self.db.delete(db_job)
            self.db.commit()
        return db_job
