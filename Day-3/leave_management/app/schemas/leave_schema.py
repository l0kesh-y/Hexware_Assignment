from pydantic import BaseModel
from datetime import date

class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveUpdate(BaseModel):
    status: str
    approved_by: int | None = None

class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: str
    status: str
    approved_by: int | None
    
    class Config:
        from_attributes = True
