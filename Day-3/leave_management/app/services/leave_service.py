from sqlalchemy.orm import Session
from app.repositories.leave_repo import LeaveRepository
from app.repositories.user_repo import UserRepository
from app.schemas.leave_schema import LeaveCreate
from fastapi import HTTPException, status

class LeaveService:
    def __init__(self, db: Session):
        self.repository = LeaveRepository(db)
        self.user_repository = UserRepository(db)
        self.db = db
    
    def apply_leave(self, employee_id: int, leave: LeaveCreate):
        # Validate dates
        if leave.start_date > leave.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date"
            )
        
        # Check for overlapping leave
        overlap = self.repository.check_overlap(employee_id, leave.start_date, leave.end_date)
        if overlap:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Leave dates overlap with existing leave request"
            )
        
        try:
            return self.repository.create_leave(employee_id, leave)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_leave_by_id(self, leave_id: int):
        leave = self.repository.get_leave_by_id(leave_id)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        return leave
    
    def get_all_leaves(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_leaves(skip, limit)
    
    def get_leaves_by_employee(self, employee_id: int):
        return self.repository.get_leaves_by_employee(employee_id)
    
    def get_leaves_by_department(self, department_id: int):
        employees = self.user_repository.get_users_by_department(department_id)
        employee_ids = [emp.id for emp in employees]
        return self.repository.get_leaves_by_department(employee_ids)
    
    def approve_leave(self, leave_id: int, manager_id: int, status: str):
        leave = self.repository.get_leave_by_id(leave_id)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        if leave.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Leave request is not pending"
            )
        
        try:
            return self.repository.update_leave_status(leave_id, status, manager_id)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def admin_override(self, leave_id: int, status: str):
        leave = self.repository.get_leave_by_id(leave_id)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        try:
            return self.repository.update_leave_status(leave_id, status)
        except Exception as e:
            self.db.rollback()
            raise e
