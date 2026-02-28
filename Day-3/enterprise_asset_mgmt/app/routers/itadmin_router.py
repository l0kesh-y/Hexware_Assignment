from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.controllers.itadmin_controller import ITAdminController
from app.dependencies.rbac import require_it_admin
from app.schemas.asset_schema import AssetCreate, AssetResponse
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn, AssignmentResponse
from app.schemas.request_schema import RequestApproval, RequestResponse
from app.models.user import User

router = APIRouter(prefix="/itadmin", tags=["IT Admin"])

@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate, current_user: User = Depends(require_it_admin), db: Session = Depends(get_db)):
    return ITAdminController.create_asset(asset, db)

@router.get("/assets", response_model=list[AssetResponse])
def get_all_assets(skip: int = 0, limit: int = 10, status: str = None, current_user: User = Depends(require_it_admin), db: Session = Depends(get_db)):
    return ITAdminController.get_all_assets(skip, limit, status, db)

@router.post("/assignments", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_asset(assignment: AssignmentCreate, current_user: User = Depends(require_it_admin), db: Session = Depends(get_db)):
    return ITAdminController.assign_asset(assignment, db)

@router.patch("/assignments/{assignment_id}/return", response_model=AssignmentResponse)
def return_asset(assignment_id: int, return_data: AssignmentReturn, current_user: User = Depends(require_it_admin), db: Session = Depends(get_db)):
    return ITAdminController.return_asset(assignment_id, return_data, db)

@router.get("/requests", response_model=list[RequestResponse])
def get_all_requests(skip: int = 0, limit: int = 10, status: str = None, current_user: User = Depends(require_it_admin), db: Session = Depends(get_db)):
    return ITAdminController.get_all_requests(skip, limit, status, db)

@router.patch("/requests/{request_id}/approve", response_model=RequestResponse)
def approve_request(request_id: int, approval: RequestApproval, current_user: User = Depends(require_it_admin), db: Session = Depends(get_db)):
    return ITAdminController.approve_request(request_id, approval, db)
