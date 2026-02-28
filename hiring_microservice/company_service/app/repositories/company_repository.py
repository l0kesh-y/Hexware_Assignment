from sqlalchemy.orm import Session
from app.models.company import Company
from typing import List

class CompanyRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def create_company(self, company_data: dict) -> Company:
        company = Company(**company_data)
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company
    
    def get_company_by_email(self, email: str) -> Company | None:
        return self.db.query(Company).filter(Company.email == email).first()
    
    def get_company_by_id(self, company_id: int) -> Company | None:
        return self.db.query(Company).filter(Company.id == company_id).first()

    def get_all_companies(self) -> List[Company]:
        return self.db.query(Company).all()

    def update_company(self, company: Company, update_data: dict) -> Company:
        for key, value in update_data.items():
            if value is not None:
                setattr(company, key, value)
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete_company(self, company: Company):
        self.db.delete(company)
        self.db.commit()
