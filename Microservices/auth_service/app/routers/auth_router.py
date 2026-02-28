from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.auth_schema import RegisterSchema, LoginSchema, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    user = AuthService.register(db, payload.email, payload.password, payload.role)
    return {"message": "User created", "id": user.id}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    token = AuthService.login(db, payload.email, payload.password)
    return {"access_token": token}