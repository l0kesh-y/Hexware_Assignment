from sqlalchemy.orm import Session
from app.models.application import Application
from app.schemas.application_schema import ApplicationCreate

class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_application(self, application: ApplicationCreate):
        db_application = Application(**application.model_dump())
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application
    
    def get_application(self, application_id: int):
        return self.db.query(Application).filter(Application.id == application_id).first()
    
    def get_user_applications(self, user_id: int):
        return self.db.query(Application).filter(Application.user_id == user_id).all()
    
    def update_status(self, application_id: int, status: str):
        db_application = self.get_application(application_id)
        if db_application:
            db_application.status = status
            self.db.commit()
            self.db.refresh(db_application)
        return db_application
