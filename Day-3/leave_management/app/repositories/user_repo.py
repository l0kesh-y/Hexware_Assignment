from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserCreate, hashed_password: str):
        db_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            role=user.role,
            department_id=user.department_id
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_users_by_department(self, department_id: int):
        return self.db.query(User).filter(User.department_id == department_id).all()
    
    def update_user(self, user_id: int, user_data: dict):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            for key, value in user_data.items():
                if value is not None:
                    setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
