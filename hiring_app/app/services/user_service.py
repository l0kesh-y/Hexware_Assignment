from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.exceptions.custom_exceptions import UserNotFoundException, DuplicateEmailException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db
    
    def create_user(self, user: UserCreate):
        if self.repository.get_user_by_email(user.email):
            raise DuplicateEmailException(f"Email {user.email} already exists")
        
        hashed_password = pwd_context.hash(user.password)
        try:
            return self.repository.create_user(user, hashed_password)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_user(self, user_id: int):
        user = self.repository.get_user(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return user
    
    def get_all_users(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_users(skip, limit)
    
    def update_user(self, user_id: int, user_data: dict):
        user = self.repository.get_user(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        
        try:
            return self.repository.update_user(user_id, user_data)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_user(self, user_id: int):
        user = self.repository.get_user(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return self.repository.delete_user(user_id)
