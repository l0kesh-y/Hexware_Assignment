from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    salary: float
    company_id: int

class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    salary: float | None = None
    company_id: int | None = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    salary: float
    company_id: int
    
    class Config:
        from_attributes = True
