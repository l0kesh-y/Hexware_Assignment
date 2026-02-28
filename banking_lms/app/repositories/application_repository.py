from sqlalchemy.orm import Session
from app.models.loan_application import LoanApplication
from app.schemas.application_schema import ApplicationCreate

class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_application(self, application: ApplicationCreate):
        db_application = LoanApplication(**application.model_dump())
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application
    
    def get_application(self, application_id: int):
        return self.db.query(LoanApplication).filter(LoanApplication.id == application_id).first()
    
    def get_all_applications(self, skip: int = 0, limit: int = 10):
        return self.db.query(LoanApplication).offset(skip).limit(limit).all()
    
    def update_application_status(self, application_id: int, status: str, approved_amount: float = None, processed_by: int = None):
        db_application = self.get_application(application_id)
        if db_application:
            db_application.status = status
            if approved_amount is not None:
                db_application.approved_amount = approved_amount
            if processed_by is not None:
                db_application.processed_by = processed_by
            self.db.commit()
            self.db.refresh(db_application)
        return db_application
