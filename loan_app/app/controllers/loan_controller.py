from fastapi import APIRouter, Depends, status
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanStatusUpdate
from app.services.loan_service import LoanService
from app.dependencies.loan_dependency import get_loan_service
from typing import List

router = APIRouter(prefix="/loans", tags=["Loan Management"])

@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def submit_loan_application(
    loan: LoanCreate,
    service: LoanService = Depends(get_loan_service)
):
    """Submit a new loan application"""
    return service.submit_loan_application(loan)

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan_application(
    loan_id: int,
    service: LoanService = Depends(get_loan_service)
):
    """Get loan application by ID"""
    return service.get_loan_by_id(loan_id)

@router.get("", response_model=List[LoanResponse])
def get_all_loan_applications(
    service: LoanService = Depends(get_loan_service)
):
    """Get all loan applications"""
    return service.get_all_loans()

@router.put("/{loan_id}/approve", response_model=LoanStatusUpdate)
def approve_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service)
):
    """Approve a loan application"""
    return service.approve_loan(loan_id)

@router.put("/{loan_id}/reject", response_model=LoanStatusUpdate)
def reject_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service)
):
    """Reject a loan application"""
    return service.reject_loan(loan_id)
