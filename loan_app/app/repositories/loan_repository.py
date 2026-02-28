from sqlalchemy.orm import Session
from app.models.loan_model import LoanApplication
from app.schemas.loan_schema import LoanCreate
from typing import List, Optional

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, loan: LoanCreate, status: str = "PENDING") -> LoanApplication:
        db_loan = LoanApplication(
            applicant_name=loan.applicant_name,
            income=loan.income,
            loan_amount=loan.loan_amount,
            status=status
        )
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan

    def get_by_id(self, loan_id: int) -> Optional[LoanApplication]:
        return self.db.query(LoanApplication).filter(LoanApplication.id == loan_id).first()

    def get_all(self) -> List[LoanApplication]:
        return self.db.query(LoanApplication).all()

    def update_status(self, loan_id: int, status: str) -> Optional[LoanApplication]:
        loan = self.get_by_id(loan_id)
        if loan:
            loan.status = status
            self.db.commit()
            self.db.refresh(loan)
        return loan
