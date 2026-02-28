from pydantic import BaseModel
from datetime import date

class AssignmentCreate(BaseModel):
    asset_id: int
    user_id: int
    assigned_date: date

class AssignmentReturn(BaseModel):
    returned_date: date
    condition_on_return: str

class AssignmentResponse(BaseModel):
    id: int
    asset_id: int
    user_id: int
    assigned_date: date
    returned_date: date | None
    condition_on_return: str | None
    
    class Config:
        from_attributes = True
