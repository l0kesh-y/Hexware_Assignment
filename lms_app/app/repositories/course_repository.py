from sqlalchemy.orm import Session
from app.models.course_model import Course
from app.schemas.course_schema import CourseCreate
from typing import List

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, course: CourseCreate) -> Course:
        db_course = Course(title=course.title, duration=course.duration)
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def get_by_id(self, course_id: int) -> Course:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_all(self) -> List[Course]:
        return self.db.query(Course).all()
