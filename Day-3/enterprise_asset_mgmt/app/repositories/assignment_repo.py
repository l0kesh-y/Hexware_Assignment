from sqlalchemy.orm import Session
from app.models.asset_assignment import AssetAssignment
from app.schemas.assignment_schema import AssignmentCreate
from datetime import date

class AssignmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_assignment(self, assignment: AssignmentCreate):
        db_assignment = AssetAssignment(**assignment.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment
    
    def get_assignment_by_id(self, assignment_id: int):
        return self.db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id).first()
    
    def get_active_assignment_by_asset(self, asset_id: int):
        return self.db.query(AssetAssignment).filter(
            AssetAssignment.asset_id == asset_id,
            AssetAssignment.returned_date == None
        ).first()
    
    def get_assignments_by_user(self, user_id: int):
        return self.db.query(AssetAssignment).filter(AssetAssignment.user_id == user_id).all()
    
    def return_assignment(self, assignment_id: int, returned_date: date, condition: str):
        db_assignment = self.get_assignment_by_id(assignment_id)
        if db_assignment:
            db_assignment.returned_date = returned_date
            db_assignment.condition_on_return = condition
            self.db.commit()
            self.db.refresh(db_assignment)
        return db_assignment
