from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db
    
    def register_user(self, user: UserCreate):
        if self.repository.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = hash_password(user.password)
        try:
            return self.repository.create_user(user, hashed_password)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def login_user(self, credentials: UserLogin):
        user = self.repository.get_user_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}
