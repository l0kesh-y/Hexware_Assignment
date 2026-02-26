from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.assignment_service import AssignmentService
from app.services.request_service import RequestService
from app.schemas.request_schema import RequestCreate
from app.models.user import User

class EmployeeController:
    @staticmethod
    def request_asset(request: RequestCreate, current_user: User, db: Session = Depends(get_db)):
        service = RequestService(db)
        return service.create_request(current_user.id, request)
    
    @staticmethod
    def get_my_requests(current_user: User, db: Session = Depends(get_db)):
        service = RequestService(db)
        return service.get_employee_requests(current_user.id)
    
    @staticmethod
    def get_my_assets(current_user: User, db: Session = Depends(get_db)):
        service = AssignmentService(db)
        return service.get_user_assignments(current_user.id)
