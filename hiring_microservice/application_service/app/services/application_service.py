from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.application_repository import ApplicationRepository
from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
)
from typing import List


class ApplicationService:

    def __init__(self, db: Session):
        self.db = db
        self.application_repo = ApplicationRepository(db)

    def create_application(self, payload: ApplicationCreate) -> ApplicationResponse:
        application_dict = payload.model_dump()
        application = self.application_repo.create_application(application_dict)
        return ApplicationResponse.model_validate(application)

    def get_application_by_id(self, application_id: int) -> ApplicationResponse:
        application = self.application_repo.get_application_by_id(application_id)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )

        return ApplicationResponse.model_validate(application)

    def get_all_applications(self) -> List[ApplicationResponse]:
        applications = self.application_repo.get_all_applications()
        return [ApplicationResponse.model_validate(app) for app in applications]

    def get_applications_by_job(self, job_id: int) -> List[ApplicationResponse]:
        applications = self.application_repo.get_applications_by_job(job_id)
        return [ApplicationResponse.model_validate(app) for app in applications]

    def get_applications_by_candidate(self, candidate_id: int) -> List[ApplicationResponse]:
        applications = self.application_repo.get_applications_by_candidate(candidate_id)
        return [ApplicationResponse.model_validate(app) for app in applications]

    def update_application(self, application_id: int, payload: ApplicationUpdate) -> ApplicationResponse:
        application = self.application_repo.get_application_by_id(application_id)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )

        update_data = payload.model_dump(exclude_unset=True)
        updated_application = self.application_repo.update_application(application, update_data)

        return ApplicationResponse.model_validate(updated_application)

    def delete_application(self, application_id: int):
        application = self.application_repo.get_application_by_id(application_id)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )

        self.application_repo.delete_application(application)

        return {"message": "Application deleted successfully"}
