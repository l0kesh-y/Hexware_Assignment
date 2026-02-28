from sqlalchemy.orm import Session
from app.core.config import get_db
from app.repositories.loan_repository import LoanRepository
from app.services.loan_service import LoanService
from fastapi import Depends

def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    """Dependency injection for LoanService"""
    repository = LoanRepository(db)
    return LoanService(repository)
