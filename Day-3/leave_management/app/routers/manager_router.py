from fastapi import APIRouter, Depends
from app.controllers.manager_controller import ManagerController
from app.dependencies.rbac import require_manager
from app.schemas.user_schema import UserResponse
from app.schemas.leave_schema import LeaveResponse
from app.models.user import User

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.get("/employees", response_model=list[UserResponse])
def get_department_employees(current_user: User = Depends(require_manager)):
    return ManagerController.get_department_employees(current_user)

@router.get("/leaves", response_model=list[LeaveResponse])
def get_department_leaves(current_user: User = Depends(require_manager)):
    return ManagerController.get_department_leaves(current_user)

@router.patch("/leaves/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(leave_id: int, status: str, current_user: User = Depends(require_manager)):
    return ManagerController.approve_leave(leave_id, status, current_user)
