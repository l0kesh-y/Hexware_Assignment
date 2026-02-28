from app.repositories.loan_repository import LoanRepository
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanStatusUpdate
from app.core.config import MAX_LOAN_MULTIPLIER
from fastapi import HTTPException
from typing import List

class LoanService:
    def __init__(self, repository: LoanRepository):
        self.repository = repository

    def calculate_eligibility(self, income: float) -> float:
        """Calculate maximum eligible loan amount"""
        return income * MAX_LOAN_MULTIPLIER

    def submit_loan_application(self, loan: LoanCreate) -> LoanResponse:
        """Submit loan application with eligibility validation"""
        max_eligible = self.calculate_eligibility(loan.income)
        
        # Business Rule: Auto-reject if loan amount exceeds eligibility
        if loan.loan_amount > max_eligible:
            db_loan = self.repository.create(loan, status="REJECTED")
        else:
            db_loan = self.repository.create(loan, status="PENDING")
        
        return LoanResponse.model_validate(db_loan)

    def get_loan_by_id(self, loan_id: int) -> LoanResponse:
        """Get loan application by ID"""
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan application not found")
        return LoanResponse.model_validate(loan)

    def get_all_loans(self) -> List[LoanResponse]:
        """Get all loan applications"""
        loans = self.repository.get_all()
        return [LoanResponse.model_validate(loan) for loan in loans]

    def approve_loan(self, loan_id: int) -> LoanStatusUpdate:
        """Approve loan application with business rule validation"""
        loan = self.repository.get_by_id(loan_id)
        
        if not loan:
            raise HTTPException(status_code=404, detail="Loan application not found")
        
        # Business Rule: Only PENDING loans can be approved
        if loan.status != "PENDING":
            raise HTTPException(
                status_code=400, 
                detail="Only pending loans can be approved"
            )
        
        # Business Rule: Validate eligibility before approval
        max_eligible = self.calculate_eligibility(loan.income)
        if loan.loan_amount > max_eligible:
            raise HTTPException(
                status_code=400, 
                detail="Loan amount exceeds eligibility limit"
            )
        
        self.repository.update_status(loan_id, "APPROVED")
        return LoanStatusUpdate(
            message="Loan approved successfully",
            status="APPROVED"
        )

    def reject_loan(self, loan_id: int) -> LoanStatusUpdate:
        """Reject loan application"""
        loan = self.repository.get_by_id(loan_id)
        
        if not loan:
            raise HTTPException(status_code=404, detail="Loan application not found")
        
        # Business Rule: Only PENDING loans can be rejected
        if loan.status != "PENDING":
            raise HTTPException(
                status_code=400, 
                detail="Only pending loans can be rejected"
            )
        
        self.repository.update_status(loan_id, "REJECTED")
        return LoanStatusUpdate(
            message="Loan rejected",
            status="REJECTED"
        )
