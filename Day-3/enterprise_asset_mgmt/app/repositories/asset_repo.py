from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset_schema import AssetCreate, AssetUpdate

class AssetRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_asset(self, asset: AssetCreate):
        db_asset = Asset(**asset.model_dump())
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
    
    def get_asset_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    
    def get_asset_by_tag(self, asset_tag: str):
        return self.db.query(Asset).filter(Asset.asset_tag == asset_tag).first()
    
    def get_all_assets(self, skip: int = 0, limit: int = 10, status: str = None):
        query = self.db.query(Asset)
        if status:
            query = query.filter(Asset.status == status)
        return query.offset(skip).limit(limit).all()
    
    def get_assets_by_department(self, department_id: int):
        return self.db.query(Asset).filter(Asset.department_id == department_id).all()
    
    def update_asset(self, asset_id: int, asset_data: AssetUpdate):
        db_asset = self.get_asset_by_id(asset_id)
        if db_asset:
            for key, value in asset_data.model_dump(exclude_unset=True).items():
                setattr(db_asset, key, value)
            self.db.commit()
            self.db.refresh(db_asset)
        return db_asset
    
    def update_asset_status(self, asset_id: int, status: str):
        db_asset = self.get_asset_by_id(asset_id)
        if db_asset:
            db_asset.status = status
            self.db.commit()
            self.db.refresh(db_asset)
        return db_asset
