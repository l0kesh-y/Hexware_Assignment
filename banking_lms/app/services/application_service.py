from sqlalchemy.orm import Session
from app.repositories.application_repository import ApplicationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.application_schema import ApplicationCreate, ApplicationStatusUpdate
from app.exceptions.custom_exceptions import (
    UserNotFoundException, 
    ProductNotFoundException, 
    ApplicationNotFoundException,
    InvalidLoanAmountException,
    InvalidStatusTransitionException
)

class ApplicationService:
    def __init__(self, db: Session):
        self.repository = ApplicationRepository(db)
        self.user_repository = UserRepository(db)
        self.product_repository = ProductRepository(db)
        self.db = db
    
    def create_application(self, application: ApplicationCreate):
        user = self.user_repository.get_user(application.user_id)
        if not user:
            raise UserNotFoundException(f"User with id {application.user_id} not found")
        
        product = self.product_repository.get_product(application.product_id)
        if not product:
            raise ProductNotFoundException(f"Product with id {application.product_id} not found")
        
        if application.requested_amount > product.max_amount:
            raise InvalidLoanAmountException(
                f"Requested amount {application.requested_amount} exceeds max amount {product.max_amount}"
            )
        
        try:
            return self.repository.create_application(application)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_application(self, application_id: int):
        application = self.repository.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with id {application_id} not found")
        return application
    
    def get_all_applications(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_applications(skip, limit)
    
    def update_application_status(self, application_id: int, status_update: ApplicationStatusUpdate):
        application = self.repository.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with id {application_id} not found")
        
        # Business rule: Cannot disburse unless approved
        if status_update.status == "disbursed" and application.status != "approved":
            raise InvalidStatusTransitionException("Cannot disburse loan that is not approved")
        
        # Business rule: Approved amount cannot exceed product max
        if status_update.approved_amount:
            product = self.product_repository.get_product(application.product_id)
            if status_update.approved_amount > product.max_amount:
                raise InvalidLoanAmountException(
                    f"Approved amount {status_update.approved_amount} exceeds max amount {product.max_amount}"
                )
        
        try:
            return self.repository.update_application_status(
                application_id,
                status_update.status,
                status_update.approved_amount,
                status_update.processed_by
            )
        except Exception as e:
            self.db.rollback()
            raise e
