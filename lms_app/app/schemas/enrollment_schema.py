from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True

class StudentEnrollmentResponse(BaseModel):
    course_id: int
    course_title: str

    class Config:
        from_attributes = True
