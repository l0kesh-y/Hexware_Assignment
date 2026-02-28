from pydantic import BaseModel, ConfigDict
from typing import Optional

class JobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    company_id: int
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    status: Optional[str] = 'active'

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    status: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    company_id: int
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True)
