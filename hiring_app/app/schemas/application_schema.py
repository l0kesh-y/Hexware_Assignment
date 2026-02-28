from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    
    class Config:
        from_attributes = True
