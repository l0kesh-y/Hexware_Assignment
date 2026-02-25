from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.application_service import ApplicationService
from app.schemas.application_schema import ApplicationCreate, ApplicationStatusUpdate, ApplicationResponse

router = APIRouter()

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.create_application(application)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_application(application_id)

@router.get("/", response_model=list[ApplicationResponse])
def get_all_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_all_applications(skip, limit)

@router.put("/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(application_id: int, status_update: ApplicationStatusUpdate, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.update_application_status(application_id, status_update)
