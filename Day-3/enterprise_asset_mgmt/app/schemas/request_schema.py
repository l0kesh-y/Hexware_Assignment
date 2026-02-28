from pydantic import BaseModel

class RequestCreate(BaseModel):
    asset_type: str
    reason: str

class RequestApproval(BaseModel):
    status: str  # APPROVED or REJECTED
    approved_by: int

class RequestResponse(BaseModel):
    id: int
    employee_id: int
    asset_type: str
    reason: str
    status: str
    approved_by: int | None
    
    class Config:
        from_attributes = True
