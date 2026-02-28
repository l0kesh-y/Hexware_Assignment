from sqlalchemy.orm import Session
from app.models.application import Application
from typing import List

class ApplicationRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def create_application(self, application_data: dict) -> Application:
        application = Application(**application_data)
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application
    
    def get_application_by_id(self, application_id: int) -> Application | None:
        return self.db.query(Application).filter(Application.id == application_id).first()

    def get_all_applications(self) -> List[Application]:
        return self.db.query(Application).all()

    def get_applications_by_job(self, job_id: int) -> List[Application]:
        return self.db.query(Application).filter(Application.job_id == job_id).all()

    def get_applications_by_candidate(self, candidate_id: int) -> List[Application]:
        return self.db.query(Application).filter(Application.candidate_id == candidate_id).all()

    def update_application(self, application: Application, update_data: dict) -> Application:
        for key, value in update_data.items():
            if value is not None:
                setattr(application, key, value)
        self.db.commit()
        self.db.refresh(application)
        return application

    def delete_application(self, application: Application):
        self.db.delete(application)
        self.db.commit()
