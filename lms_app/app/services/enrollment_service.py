from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.course_repository import CourseRepository
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse, StudentEnrollmentResponse
from fastapi import HTTPException
from typing import List

class EnrollmentService:
    def __init__(
        self,
        enrollment_repo: EnrollmentRepository,
        student_repo: StudentRepository,
        course_repo: CourseRepository
    ):
        self.enrollment_repo = enrollment_repo
        self.student_repo = student_repo
        self.course_repo = course_repo

    def enroll_student(self, enrollment: EnrollmentCreate) -> EnrollmentResponse:
        # Validate student exists
        student = self.student_repo.get_by_id(enrollment.student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Validate course exists
        course = self.course_repo.get_by_id(enrollment.course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Check duplicate enrollment
        if self.enrollment_repo.exists(enrollment.student_id, enrollment.course_id):
            raise HTTPException(status_code=400, detail="Already enrolled")

        db_enrollment = self.enrollment_repo.create(enrollment)
        return EnrollmentResponse.model_validate(db_enrollment)

    def get_all_enrollments(self) -> List[EnrollmentResponse]:
        enrollments = self.enrollment_repo.get_all()
        return [EnrollmentResponse.model_validate(e) for e in enrollments]

    def get_student_enrollments(self, student_id: int) -> List[StudentEnrollmentResponse]:
        # Validate student exists
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        enrollments = self.enrollment_repo.get_by_student(student_id)
        return [
            StudentEnrollmentResponse(
                course_id=enrollment.course_id,
                course_title=course.title
            )
            for enrollment, course in enrollments
        ]
