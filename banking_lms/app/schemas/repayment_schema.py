from pydantic import BaseModel
from datetime import date

class RepaymentCreate(BaseModel):
    loan_application_id: int
    amount_paid: float
    payment_date: date
    payment_status: str = "completed"

class RepaymentResponse(BaseModel):
    id: int
    loan_application_id: int
    amount_paid: float
    payment_date: date
    payment_status: str
    
    class Config:
        from_attributes = True
