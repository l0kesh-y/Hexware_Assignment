from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    # ---------------------------------------------------
    # CREATE USER
    # ---------------------------------------------------
    def create_user(self, payload: UserCreate) -> UserResponse:
        existing_user = self.user_repo.get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_dict = payload.model_dump()
        user_dict["password"] = hash_password(user_dict["password"])

        user = self.user_repo.create_user(user_dict)

        return UserResponse.model_validate(user)


    # ---------------------------------------------------
    # LOGIN USER (RETURN ACCESS TOKEN)
    # ---------------------------------------------------
    def login_user(self, email: str, password: str) -> str:
        user = self.user_repo.get_user_by_email(email)

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "id": user.id,
                "role": user.role
            }
        )

        return access_token


    # ---------------------------------------------------
    # GET USER BY ID
    # ---------------------------------------------------
    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse.model_validate(user)


    # ---------------------------------------------------
    # GET USER BY EMAIL
    # ---------------------------------------------------
    def get_user_by_email(self, email: str) -> UserResponse:
        user = self.user_repo.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse.model_validate(user)


    # ---------------------------------------------------
    # UPDATE USER (BY ID)
    # ---------------------------------------------------
    def update_user(self, user_id: int, payload: UserUpdate) -> UserResponse:
        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        update_data = payload.model_dump(exclude_unset=True)

        # Hash password if being updated
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        updated_user = self.user_repo.update_user(user, update_data)

        return UserResponse.model_validate(updated_user)


    # ---------------------------------------------------
    # DELETE USER (BY ID)
    # ---------------------------------------------------
    def delete_user(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        self.user_repo.delete_user(user)

        return {"message": "User deleted successfully"}