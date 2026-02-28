from sqlalchemy.orm import Session
from app.models.repayment import Repayment
from app.schemas.repayment_schema import RepaymentCreate

class RepaymentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_repayment(self, repayment: RepaymentCreate):
        db_repayment = Repayment(**repayment.model_dump())
        self.db.add(db_repayment)
        self.db.commit()
        self.db.refresh(db_repayment)
        return db_repayment
    
    def get_repayments_by_loan(self, loan_application_id: int):
        return self.db.query(Repayment).filter(Repayment.loan_application_id == loan_application_id).all()
    
    def get_total_repaid(self, loan_application_id: int):
        repayments = self.get_repayments_by_loan(loan_application_id)
        return sum(r.amount_paid for r in repayments if r.payment_status == "completed")
