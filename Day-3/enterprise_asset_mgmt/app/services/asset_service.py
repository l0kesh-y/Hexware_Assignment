from sqlalchemy.orm import Session
from app.repositories.asset_repo import AssetRepository
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from fastapi import HTTPException, status

class AssetService:
    def __init__(self, db: Session):
        self.repository = AssetRepository(db)
        self.db = db
    
    def create_asset(self, asset: AssetCreate):
        # Check for duplicate asset_tag
        if self.repository.get_asset_by_tag(asset.asset_tag):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with tag {asset.asset_tag} already exists"
            )
        
        try:
            return self.repository.create_asset(asset)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_asset(self, asset_id: int):
        asset = self.repository.get_asset_by_id(asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        return asset
    
    def get_all_assets(self, skip: int = 0, limit: int = 10, status: str = None):
        return self.repository.get_all_assets(skip, limit, status)
    
    def get_assets_by_department(self, department_id: int):
        return self.repository.get_assets_by_department(department_id)
    
    def update_asset(self, asset_id: int, asset_data: AssetUpdate):
        asset = self.repository.get_asset_by_id(asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        try:
            return self.repository.update_asset(asset_id, asset_data)
        except Exception as e:
            self.db.rollback()
            raise e
