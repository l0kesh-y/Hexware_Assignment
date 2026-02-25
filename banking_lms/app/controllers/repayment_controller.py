from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.repayment_service import RepaymentService
from app.schemas.repayment_schema import RepaymentCreate, RepaymentResponse

router = APIRouter()

@router.post("/", response_model=RepaymentResponse, status_code=status.HTTP_201_CREATED)
def create_repayment(repayment: RepaymentCreate, db: Session = Depends(get_db)):
    service = RepaymentService(db)
    return service.create_repayment(repayment)

@router.get("/loan-applications/{loan_application_id}/repayments", response_model=list[RepaymentResponse])
def get_repayments_by_loan(loan_application_id: int, db: Session = Depends(get_db)):
    service = RepaymentService(db)
    return service.get_repayments_by_loan(loan_application_id)
