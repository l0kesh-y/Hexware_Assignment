from sqlalchemy.orm import Session
from app.models.user import User

#class UserRepository:
    
#     @staticmethod
#     def create_user(db: Session, user_data: dict) -> User:
#         user = User(**user_data)
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return user

#     @staticmethod
#     def get_user_by_email(db: Session, email: str) -> User | None:
#         return db.query(User).filter(User.email == email).first()

#     @staticmethod
#     def get_user_by_id(db: Session, user_id: int) -> User | None:
#         return db.query(User).filter(User.id == user_id).first()

class UserRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    