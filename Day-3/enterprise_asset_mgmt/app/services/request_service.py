from sqlalchemy.orm import Session
from app.repositories.request_repo import RequestRepository
from app.repositories.asset_repo import AssetRepository
from app.schemas.request_schema import RequestCreate, RequestApproval
from app.services.assignment_service import AssignmentService
from app.schemas.assignment_schema import AssignmentCreate
from fastapi import HTTPException, status
from datetime import date

class RequestService:
    def __init__(self, db: Session):
        self.repository = RequestRepository(db)
        self.asset_repository = AssetRepository(db)
        self.assignment_service = AssignmentService(db)
        self.db = db
    
    def create_request(self, employee_id: int, request: RequestCreate):
        try:
            return self.repository.create_request(employee_id, request)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_request(self, request_id: int):
        request = self.repository.get_request_by_id(request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found"
            )
        return request
    
    def get_all_requests(self, skip: int = 0, limit: int = 10, status: str = None):
        return self.repository.get_all_requests(skip, limit, status)
    
    def get_employee_requests(self, employee_id: int):
        return self.repository.get_requests_by_employee(employee_id)
    
    def approve_request(self, request_id: int, approval: RequestApproval):
        request = self.repository.get_request_by_id(request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found"
            )
        
        if request.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request is not pending"
            )
        
        try:
            # Update request status
            updated_request = self.repository.update_request_status(
                request_id,
                approval.status,
                approval.approved_by
            )
            
            # If approved, find available asset and assign
            if approval.status == "APPROVED":
                available_assets = self.asset_repository.get_all_assets(status="AVAILABLE")
                matching_asset = next(
                    (asset for asset in available_assets if asset.asset_type == request.asset_type),
                    None
                )
                
                if matching_asset:
                    assignment = AssignmentCreate(
                        asset_id=matching_asset.id,
                        user_id=request.employee_id,
                        assigned_date=date.today()
                    )
                    self.assignment_service.assign_asset(assignment)
            
            return updated_request
        except Exception as e:
            self.db.rollback()
            raise e
