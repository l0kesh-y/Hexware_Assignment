from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token

class AuthController:
    @staticmethod
    def register(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
        service = AuthService(db)
        return service.register_user(user)
    
    @staticmethod
    def login(credentials: UserLogin, db: Session = Depends(get_db)) -> Token:
        service = AuthService(db)
        return service.login_user(credentials)
