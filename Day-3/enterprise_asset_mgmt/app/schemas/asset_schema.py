from pydantic import BaseModel
from datetime import date

class AssetCreate(BaseModel):
    asset_tag: str
    asset_type: str
    brand: str | None = None
    model: str | None = None
    purchase_date: date | None = None
    department_id: int | None = None

class AssetUpdate(BaseModel):
    asset_tag: str | None = None
    asset_type: str | None = None
    brand: str | None = None
    model: str | None = None
    status: str | None = None
    department_id: int | None = None

class AssetResponse(BaseModel):
    id: int
    asset_tag: str
    asset_type: str
    brand: str | None
    model: str | None
    purchase_date: date | None
    status: str
    department_id: int | None
    
    class Config:
        from_attributes = True
