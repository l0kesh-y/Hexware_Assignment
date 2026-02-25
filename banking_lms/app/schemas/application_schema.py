from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    user_id: int
    product_id: int
    requested_amount: float

class ApplicationStatusUpdate(BaseModel):
    status: str
    approved_amount: float | None = None
    processed_by: int | None = None

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    requested_amount: float
    approved_amount: float | None
    status: str
    processed_by: int | None
    
    class Config:
        from_attributes = True
