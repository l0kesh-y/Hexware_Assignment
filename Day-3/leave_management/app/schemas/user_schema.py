from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    department_id: int | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department_id: int | None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
