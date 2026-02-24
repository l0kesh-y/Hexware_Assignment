from fastapi import APIRouter, Depends, status
from app.schemas.course_schema import CourseCreate, CourseResponse
from app.services.course_service import CourseService
from app.dependencies.dependencies import get_course_service
from typing import List

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    service: CourseService = Depends(get_course_service)
):
    return service.create_course(course)

@router.get("", response_model=List[CourseResponse])
def get_all_courses(
    service: CourseService = Depends(get_course_service)
):
    return service.get_all_courses()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    service: CourseService = Depends(get_course_service)
):
    return service.get_course(course_id)
