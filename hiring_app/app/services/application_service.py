from sqlalchemy.orm import Session
from app.repositories.application_repository import ApplicationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.job_repository import JobRepository
from app.schemas.application_schema import ApplicationCreate
from app.exceptions.custom_exceptions import UserNotFoundException, JobNotFoundException, ApplicationNotFoundException

class ApplicationService:
    def __init__(self, db: Session):
        self.repository = ApplicationRepository(db)
        self.user_repository = UserRepository(db)
        self.job_repository = JobRepository(db)
        self.db = db
    
    def create_application(self, application: ApplicationCreate):
        if not self.user_repository.get_user(application.user_id):
            raise UserNotFoundException(f"User with id {application.user_id} not found")
        
        if not self.job_repository.get_job(application.job_id):
            raise JobNotFoundException(f"Job with id {application.job_id} not found")
        
        try:
            return self.repository.create_application(application)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_application(self, application_id: int):
        application = self.repository.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with id {application_id} not found")
        return application
    
    def get_user_applications(self, user_id: int):
        if not self.user_repository.get_user(user_id):
            raise UserNotFoundException(f"User with id {user_id} not found")
        return self.repository.get_user_applications(user_id)
    
    def update_status(self, application_id: int, status: str):
        application = self.repository.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with id {application_id} not found")
        
        try:
            return self.repository.update_status(application_id, status)
        except Exception as e:
            self.db.rollback()
            raise e
