from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.asset_service import AssetService
from app.services.assignment_service import AssignmentService
from app.services.request_service import RequestService
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn
from app.schemas.request_schema import RequestApproval

class ITAdminController:
    @staticmethod
    def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
        service = AssetService(db)
        return service.create_asset(asset)
    
    @staticmethod
    def get_all_assets(skip: int = 0, limit: int = 10, status: str = None, db: Session = Depends(get_db)):
        service = AssetService(db)
        return service.get_all_assets(skip, limit, status)
    
    @staticmethod
    def assign_asset(assignment: AssignmentCreate, db: Session = Depends(get_db)):
        service = AssignmentService(db)
        return service.assign_asset(assignment)
    
    @staticmethod
    def return_asset(assignment_id: int, return_data: AssignmentReturn, db: Session = Depends(get_db)):
        service = AssignmentService(db)
        return service.return_asset(assignment_id, return_data)
    
    @staticmethod
    def get_all_requests(skip: int = 0, limit: int = 10, status: str = None, db: Session = Depends(get_db)):
        service = RequestService(db)
        return service.get_all_requests(skip, limit, status)
    
    @staticmethod
    def approve_request(request_id: int, approval: RequestApproval, db: Session = Depends(get_db)):
        service = RequestService(db)
        return service.approve_request(request_id, approval)
