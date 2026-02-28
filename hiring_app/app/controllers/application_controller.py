from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.application_service import ApplicationService
from app.schemas.application_schema import ApplicationCreate, ApplicationResponse

router = APIRouter()

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.create_application(application)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_application(application_id)

@router.get("/users/{user_id}/applications", response_model=list[ApplicationResponse])
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_user_applications(user_id)

@router.patch("/{application_id}/status")
def update_application_status(application_id: int, status: str, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.update_status(application_id, status)
