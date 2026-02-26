from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.user_service import UserService
from app.services.department_service import DepartmentService
from app.services.leave_service import LeaveService
from app.schemas.user_schema import UserResponse
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.leave_schema import LeaveResponse

class AdminController:
    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        service = UserService(db)
        return service.get_all_users(skip, limit)
    
    @staticmethod
    def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
        service = DepartmentService(db)
        return service.create_department(department)
    
    @staticmethod
    def get_all_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        service = DepartmentService(db)
        return service.get_all_departments(skip, limit)
    
    @staticmethod
    def update_department(department_id: int, department_data: DepartmentUpdate, db: Session = Depends(get_db)):
        service = DepartmentService(db)
        return service.update_department(department_id, department_data)
    
    @staticmethod
    def delete_department(department_id: int, db: Session = Depends(get_db)):
        service = DepartmentService(db)
        return service.delete_department(department_id)
    
    @staticmethod
    def get_all_leaves(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        service = LeaveService(db)
        return service.get_all_leaves(skip, limit)
    
    @staticmethod
    def override_leave_status(leave_id: int, status: str, db: Session = Depends(get_db)):
        service = LeaveService(db)
        return service.admin_override(leave_id, status)
