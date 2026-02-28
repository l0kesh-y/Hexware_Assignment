from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.leave_service import LeaveService
from app.services.user_service import UserService
from app.models.user import User

class ManagerController:
    @staticmethod
    def get_department_employees(current_user: User, db: Session = Depends(get_db)):
        if not current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager not assigned to any department"
            )
        service = UserService(db)
        return service.get_users_by_department(current_user.department_id)
    
    @staticmethod
    def get_department_leaves(current_user: User, db: Session = Depends(get_db)):
        if not current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager not assigned to any department"
            )
        service = LeaveService(db)
        return service.get_leaves_by_department(current_user.department_id)
    
    @staticmethod
    def approve_leave(leave_id: int, status: str, current_user: User, db: Session = Depends(get_db)):
        if not current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager not assigned to any department"
            )
        
        leave_service = LeaveService(db)
        leave = leave_service.get_leave_by_id(leave_id)
        
        # Verify leave belongs to manager's department
        user_service = UserService(db)
        employee = user_service.get_user_by_id(leave.employee_id)
        
        if employee.department_id != current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Leave request not in your department"
            )
        
        return leave_service.approve_leave(leave_id, current_user.id, status)
