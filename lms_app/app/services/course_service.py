from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import CourseCreate, CourseResponse
from fastapi import HTTPException
from typing import List

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def create_course(self, course: CourseCreate) -> CourseResponse:
        db_course = self.repository.create(course)
        return CourseResponse.model_validate(db_course)

    def get_course(self, course_id: int) -> CourseResponse:
        course = self.repository.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseResponse.model_validate(course)

    def get_all_courses(self) -> List[CourseResponse]:
        courses = self.repository.get_all()
        return [CourseResponse.model_validate(course) for course in courses]
