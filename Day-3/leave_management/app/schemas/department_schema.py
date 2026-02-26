from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str
    manager_id: int | None = None

class DepartmentUpdate(BaseModel):
    name: str | None = None
    manager_id: int | None = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    manager_id: int | None
    
    class Config:
        from_attributes = True
