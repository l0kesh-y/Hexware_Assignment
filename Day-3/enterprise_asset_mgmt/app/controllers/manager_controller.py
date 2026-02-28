from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.asset_service import AssetService
from app.models.user import User

class ManagerController:
    @staticmethod
    def get_department_assets(current_user: User, db: Session = Depends(get_db)):
        if not current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager not assigned to any department"
            )
        service = AssetService(db)
        return service.get_assets_by_department(current_user.department_id)
