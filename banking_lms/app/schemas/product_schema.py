from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_name: str
    interest_rate: float
    max_amount: float
    tenure_months: int
    description: str | None = None

class ProductUpdate(BaseModel):
    product_name: str | None = None
    interest_rate: float | None = None
    max_amount: float | None = None
    tenure_months: int | None = None
    description: str | None = None

class ProductResponse(BaseModel):
    id: int
    product_name: str
    interest_rate: float
    max_amount: float
    tenure_months: int
    description: str | None
    
    class Config:
        from_attributes = True
