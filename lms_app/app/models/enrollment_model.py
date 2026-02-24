from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.core.db import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),
    )
