from sqlalchemy.orm import Session
from app.models.leave_request import LeaveRequest
from app.schemas.leave_schema import LeaveCreate
from datetime import date

class LeaveRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_leave(self, employee_id: int, leave: LeaveCreate):
        db_leave = LeaveRequest(
            employee_id=employee_id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            reason=leave.reason
        )
        self.db.add(db_leave)
        self.db.commit()
        self.db.refresh(db_leave)
        return db_leave
    
    def get_leave_by_id(self, leave_id: int):
        return self.db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    
    def get_all_leaves(self, skip: int = 0, limit: int = 10):
        return self.db.query(LeaveRequest).offset(skip).limit(limit).all()
    
    def get_leaves_by_employee(self, employee_id: int):
        return self.db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()
    
    def get_leaves_by_department(self, employee_ids: list):
        return self.db.query(LeaveRequest).filter(LeaveRequest.employee_id.in_(employee_ids)).all()
    
    def check_overlap(self, employee_id: int, start_date: date, end_date: date):
        return self.db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status != "REJECTED",
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date
        ).first()
    
    def update_leave_status(self, leave_id: int, status: str, approved_by: int = None):
        db_leave = self.get_leave_by_id(leave_id)
        if db_leave:
            db_leave.status = status
            if approved_by:
                db_leave.approved_by = approved_by
            self.db.commit()
            self.db.refresh(db_leave)
        return db_leave
