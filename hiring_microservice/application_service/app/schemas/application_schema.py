from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    job_id: int
    candidate_id: int
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None

class ApplicationUpdate(BaseModel):
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    status: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    status: str
    applied_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
