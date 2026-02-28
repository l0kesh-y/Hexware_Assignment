from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.admin_controller import AdminController
from app.dependencies.rbac import require_admin
from app.schemas.user_schema import UserResponse
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.leave_schema import LeaveResponse
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, current_user: User = Depends(require_admin)):
    return AdminController.get_all_users(skip, limit)

@router.post("/departments", response_model=DepartmentResponse)
def create_department(department: DepartmentCreate, current_user: User = Depends(require_admin)):
    return AdminController.create_department(department)

@router.get("/departments", response_model=list[DepartmentResponse])
def get_all_departments(skip: int = 0, limit: int = 10, current_user: User = Depends(require_admin)):
    return AdminController.get_all_departments(skip, limit)

@router.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, department_data: DepartmentUpdate, current_user: User = Depends(require_admin)):
    return AdminController.update_department(department_id, department_data)

@router.delete("/departments/{department_id}")
def delete_department(department_id: int, current_user: User = Depends(require_admin)):
    return AdminController.delete_department(department_id)

@router.get("/leaves", response_model=list[LeaveResponse])
def get_all_leaves(skip: int = 0, limit: int = 10, current_user: User = Depends(require_admin)):
    return AdminController.get_all_leaves(skip, limit)

@router.patch("/leaves/{leave_id}/status", response_model=LeaveResponse)
def override_leave_status(leave_id: int, status: str, current_user: User = Depends(require_admin)):
    return AdminController.override_leave_status(leave_id, status)
