from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db
    
    def get_user_by_id(self, user_id: int):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def get_all_users(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all_users(skip, limit)
    
    def get_users_by_department(self, department_id: int):
        return self.repository.get_users_by_department(department_id)
    
    def update_user(self, user_id: int, user_data: dict):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            return self.repository.update_user(user_id, user_data)
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_user(self, user_id: int):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return self.repository.delete_user(user_id)
