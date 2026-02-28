from sqlalchemy.orm import Session
from app.models.asset_request import AssetRequest
from app.schemas.request_schema import RequestCreate

class RequestRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_request(self, employee_id: int, request: RequestCreate):
        db_request = AssetRequest(
            employee_id=employee_id,
            asset_type=request.asset_type,
            reason=request.reason
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        return db_request
    
    def get_request_by_id(self, request_id: int):
        return self.db.query(AssetRequest).filter(AssetRequest.id == request_id).first()
    
    def get_all_requests(self, skip: int = 0, limit: int = 10, status: str = None):
        query = self.db.query(AssetRequest)
        if status:
            query = query.filter(AssetRequest.status == status)
        return query.offset(skip).limit(limit).all()
    
    def get_requests_by_employee(self, employee_id: int):
        return self.db.query(AssetRequest).filter(AssetRequest.employee_id == employee_id).all()
    
    def update_request_status(self, request_id: int, status: str, approved_by: int = None):
        db_request = self.get_request_by_id(request_id)
        if db_request:
            db_request.status = status
            if approved_by:
                db_request.approved_by = approved_by
            self.db.commit()
            self.db.refresh(db_request)
        return db_request
