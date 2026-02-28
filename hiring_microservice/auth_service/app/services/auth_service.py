from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    
    def __init__(self, db: Session):
        self.db = db         #This service will use the DB session
        self.user_repo = UserRepository(db) #This service will delegate the database operations to the UserRepository
        

    def register_user(self, user_data: dict) -> User:
        existing_user = self.user_repo.get_user_by_email(user_data['email'])
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        user_data['password'] = hash_password(user_data['password'])
        return self.user_repo.create_user(user_data)

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.email})
        return access_token

