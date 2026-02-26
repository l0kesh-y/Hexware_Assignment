from sqlalchemy.orm import Session
from app.repositories.department_repo import DepartmentRepository
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from fastapi import HTTPException, status

class DepartmentService:
    def __init__(self, db: Session):
        self.repository = DepartmentRepository(db)
        self.db = db
    
    def create_department(self, department: DepartmentCreate):
        try:
            return self.repository.create_department(department)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_department_by_id(self, department_id: int):
        department = self.repository.get_department_by_id(department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        return department
    
    def get_all_departments(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_departments(skip, limit)
    
    def update_department(self, department_id: int, department_data: DepartmentUpdate):
        department = self.repository.get_department_by_id(department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        try:
            return self.repository.update_department(department_id, department_data)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_department(self, department_id: int):
        department = self.repository.get_department_by_id(department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        return self.repository.delete_department(department_id)
