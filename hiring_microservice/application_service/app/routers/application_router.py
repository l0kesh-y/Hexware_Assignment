from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.application_service import ApplicationService
from app.schemas.application_schema import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from typing import List, Optional

router = APIRouter(prefix="/applications", tags=["Applications"])

def get_application_service(db: Session = Depends(get_db)):
    return ApplicationService(db)

@router.post("/", response_model=ApplicationResponse)
def create_application(
    payload: ApplicationCreate,
    application_service: ApplicationService = Depends(get_application_service)
):
    return application_service.create_application(payload)

@router.get("/", response_model=List[ApplicationResponse])
def get_all_applications(
    job_id: Optional[int] = Query(None),
    candidate_id: Optional[int] = Query(None),
    application_service: ApplicationService = Depends(get_application_service)
):
    if job_id:
        return application_service.get_applications_by_job(job_id)
    if candidate_id:
        return application_service.get_applications_by_candidate(candidate_id)
    return application_service.get_all_applications()

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    application_service: ApplicationService = Depends(get_application_service)
):
    return application_service.get_application_by_id(application_id)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    application_service: ApplicationService = Depends(get_application_service)
):
    return application_service.update_application(application_id, payload)

@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    application_service: ApplicationService = Depends(get_application_service)
):
    application_service.delete_application(application_id)
    return {"message": "Application deleted successfully"}
