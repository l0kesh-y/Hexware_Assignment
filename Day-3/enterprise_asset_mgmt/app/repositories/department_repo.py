from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_department(self, department: DepartmentCreate):
        db_department = Department(**department.model_dump())
        self.db.add(db_department)
        self.db.commit()
        self.db.refresh(db_department)
        return db_department
    
    def get_department_by_id(self, department_id: int):
        return self.db.query(Department).filter(Department.id == department_id).first()
    
    def get_all_departments(self, skip: int = 0, limit: int = 10):
        return self.db.query(Department).offset(skip).limit(limit).all()
    
    def update_department(self, department_id: int, department_data: DepartmentUpdate):
        db_department = self.get_department_by_id(department_id)
        if db_department:
            for key, value in department_data.model_dump(exclude_unset=True).items():
                setattr(db_department, key, value)
            self.db.commit()
            self.db.refresh(db_department)
        return db_department
