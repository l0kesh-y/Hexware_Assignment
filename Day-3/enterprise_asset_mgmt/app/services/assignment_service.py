from sqlalchemy.orm import Session
from app.repositories.assignment_repo import AssignmentRepository
from app.repositories.asset_repo import AssetRepository
from app.repositories.user_repo import UserRepository
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn
from fastapi import HTTPException, status
from datetime import date

class AssignmentService:
    def __init__(self, db: Session):
        self.repository = AssignmentRepository(db)
        self.asset_repository = AssetRepository(db)
        self.user_repository = UserRepository(db)
        self.db = db
    
    def assign_asset(self, assignment: AssignmentCreate):
        # Check if asset exists
        asset = self.asset_repository.get_asset_by_id(assignment.asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        # Check if asset is available
        if asset.status != "AVAILABLE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset is not available. Current status: {asset.status}"
            )
        
        # Check if user exists
        user = self.user_repository.get_user_by_id(assignment.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check for active assignment
        active_assignment = self.repository.get_active_assignment_by_asset(assignment.asset_id)
        if active_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset is already assigned to another user"
            )
        
        try:
            # Create assignment
            new_assignment = self.repository.create_assignment(assignment)
            # Update asset status
            self.asset_repository.update_asset_status(assignment.asset_id, "ASSIGNED")
            return new_assignment
        except Exception as e:
            self.db.rollback()
            raise e
    
    def return_asset(self, assignment_id: int, return_data: AssignmentReturn):
        assignment = self.repository.get_assignment_by_id(assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        if assignment.returned_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset already returned"
            )
        
        try:
            # Update assignment
            updated_assignment = self.repository.return_assignment(
                assignment_id,
                return_data.returned_date,
                return_data.condition_on_return
            )
            # Update asset status
            self.asset_repository.update_asset_status(assignment.asset_id, "AVAILABLE")
            return updated_assignment
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_user_assignments(self, user_id: int):
        return self.repository.get_assignments_by_user(user_id)
