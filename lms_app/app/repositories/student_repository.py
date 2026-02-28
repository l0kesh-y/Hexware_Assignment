from sqlalchemy.orm import Session
from app.models.student_model import Student
from app.schemas.student_schema import StudentCreate

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, student: StudentCreate) -> Student:
        db_student = Student(name=student.name, email=student.email)
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def get_by_id(self, student_id: int) -> Student:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_by_email(self, email: str) -> Student:
        return self.db.query(Student).filter(Student.email == email).first()
