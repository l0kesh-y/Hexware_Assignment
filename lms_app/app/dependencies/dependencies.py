from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.student_repository import StudentRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from fastapi import Depends

def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    repository = StudentRepository(db)
    return StudentService(repository)

def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    repository = CourseRepository(db)
    return CourseService(repository)

def get_enrollment_service(db: Session = Depends(get_db)) -> EnrollmentService:
    enrollment_repo = EnrollmentRepository(db)
    student_repo = StudentRepository(db)
    course_repo = CourseRepository(db)
    return EnrollmentService(enrollment_repo, student_repo, course_repo)
