from fastapi import APIRouter, Depends
from app.controllers.employee_controller import EmployeeController
from app.dependencies.rbac import get_current_user
from app.schemas.leave_schema import LeaveCreate, LeaveResponse
from app.models.user import User

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("/leaves", response_model=LeaveResponse)
def apply_leave(leave: LeaveCreate, current_user: User = Depends(get_current_user)):
    return EmployeeController.apply_leave(leave, current_user)

@router.get("/leaves", response_model=list[LeaveResponse])
def get_my_leaves(current_user: User = Depends(get_current_user)):
    return EmployeeController.get_my_leaves(current_user)

@router.get("/leaves/{leave_id}", response_model=LeaveResponse)
def get_leave_by_id(leave_id: int, current_user: User = Depends(get_current_user)):
    return EmployeeController.get_leave_by_id(leave_id, current_user)
