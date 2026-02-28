from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.leave_service import LeaveService
from app.schemas.leave_schema import LeaveCreate, LeaveResponse
from app.models.user import User

class EmployeeController:
    @staticmethod
    def apply_leave(leave: LeaveCreate, current_user: User, db: Session = Depends(get_db)):
        service = LeaveService(db)
        return service.apply_leave(current_user.id, leave)
    
    @staticmethod
    def get_my_leaves(current_user: User, db: Session = Depends(get_db)):
        service = LeaveService(db)
        return service.get_leaves_by_employee(current_user.id)
    
    @staticmethod
    def get_leave_by_id(leave_id: int, current_user: User, db: Session = Depends(get_db)):
        service = LeaveService(db)
        leave = service.get_leave_by_id(leave_id)
        if leave.employee_id != current_user.id:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return leave
