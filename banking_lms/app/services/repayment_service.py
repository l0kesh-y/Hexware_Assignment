from sqlalchemy.orm import Session
from app.repositories.repayment_repository import RepaymentRepository
from app.repositories.application_repository import ApplicationRepository
from app.schemas.repayment_schema import RepaymentCreate
from app.exceptions.custom_exceptions import ApplicationNotFoundException, InvalidRepaymentException

class RepaymentService:
    def __init__(self, db: Session):
        self.repository = RepaymentRepository(db)
        self.application_repository = ApplicationRepository(db)
        self.db = db
    
    def create_repayment(self, repayment: RepaymentCreate):
        application = self.application_repository.get_application(repayment.loan_application_id)
        if not application:
            raise ApplicationNotFoundException(f"Loan application with id {repayment.loan_application_id} not found")
        
        # Business rule: Cannot repay if not disbursed
        if application.status not in ["disbursed", "closed"]:
            raise InvalidRepaymentException("Cannot make repayment for loan that is not disbursed")
        
        try:
            new_repayment = self.repository.create_repayment(repayment)
            
            # Check if loan is fully repaid
            total_repaid = self.repository.get_total_repaid(repayment.loan_application_id)
            if total_repaid >= application.approved_amount:
                application.status = "closed"
                self.db.commit()
            
            return new_repayment
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_repayments_by_loan(self, loan_application_id: int):
        application = self.application_repository.get_application(loan_application_id)
        if not application:
            raise ApplicationNotFoundException(f"Loan application with id {loan_application_id} not found")
        
        return self.repository.get_repayments_by_loan(loan_application_id)
