from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None

class CompanyResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
