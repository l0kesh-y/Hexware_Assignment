from fastapi import APIRouter, Depends
from app.controllers.manager_controller import ManagerController
from app.dependencies.rbac import require_manager
from app.schemas.asset_schema import AssetResponse
from app.models.user import User

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.get("/assets", response_model=list[AssetResponse])
def get_department_assets(current_user: User = Depends(require_manager)):
    return ManagerController.get_department_assets(current_user)
