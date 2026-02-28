from fastapi import APIRouter, Depends, status
from app.controllers.employee_controller import EmployeeController
from app.dependencies.rbac import get_current_user
from app.schemas.request_schema import RequestCreate, RequestResponse
from app.schemas.assignment_schema import AssignmentResponse
from app.models.user import User

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("/requests", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
def request_asset(request: RequestCreate, current_user: User = Depends(get_current_user)):
    return EmployeeController.request_asset(request, current_user)

@router.get("/requests", response_model=list[RequestResponse])
def get_my_requests(current_user: User = Depends(get_current_user)):
    return EmployeeController.get_my_requests(current_user)

@router.get("/assets", response_model=list[AssignmentResponse])
def get_my_assets(current_user: User = Depends(get_current_user)):
    return EmployeeController.get_my_assets(current_user)
