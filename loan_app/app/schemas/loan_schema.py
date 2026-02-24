from pydantic import BaseModel, Field
from typing import Literal

class LoanCreate(BaseModel):
    applicant_name: str = Field(..., min_length=1)
    income: float = Field(..., gt=0)
    loan_amount: float = Field(..., gt=0)

class LoanResponse(BaseModel):
    id: int
    applicant_name: str
    income: float
    loan_amount: float
    status: str

    class Config:
        from_attributes = True

class LoanStatusUpdate(BaseModel):
    message: str
    status: str
