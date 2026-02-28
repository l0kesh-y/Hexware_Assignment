from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.company_repository import CompanyRepository
from app.schemas.company_schema import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
)
from typing import List


class CompanyService:

    def __init__(self, db: Session):
        self.db = db
        self.company_repo = CompanyRepository(db)

    def create_company(self, payload: CompanyCreate) -> CompanyResponse:
        existing_company = self.company_repo.get_company_by_email(payload.email)
        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company email already registered"
            )

        company_dict = payload.model_dump()
        company = self.company_repo.create_company(company_dict)

        return CompanyResponse.model_validate(company)

    def get_company_by_id(self, company_id: int) -> CompanyResponse:
        company = self.company_repo.get_company_by_id(company_id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        return CompanyResponse.model_validate(company)

    def get_all_companies(self) -> List[CompanyResponse]:
        companies = self.company_repo.get_all_companies()
        return [CompanyResponse.model_validate(company) for company in companies]

    def update_company(self, company_id: int, payload: CompanyUpdate) -> CompanyResponse:
        company = self.company_repo.get_company_by_id(company_id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        update_data = payload.model_dump(exclude_unset=True)
        updated_company = self.company_repo.update_company(company, update_data)

        return CompanyResponse.model_validate(updated_company)

    def delete_company(self, company_id: int):
        company = self.company_repo.get_company_by_id(company_id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        self.company_repo.delete_company(company)

        return {"message": "Company deleted successfully"}
