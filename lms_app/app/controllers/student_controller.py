from fastapi import APIRouter, Depends, status
from app.schemas.student_schema import StudentCreate, StudentResponse
from app.services.student_service import StudentService
from app.dependencies.dependencies import get_student_service

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register_student(
    student: StudentCreate,
    service: StudentService = Depends(get_student_service)
):
    return service.create_student(student)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    return service.get_student(student_id)
