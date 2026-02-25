from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)  # admin, loan_officer, customer
    hashed_password = Column(String, nullable=False)
    
    # Relationships
    loan_applications = relationship("LoanApplication", foreign_keys="LoanApplication.user_id", back_populates="customer")
    processed_applications = relationship("LoanApplication", foreign_keys="LoanApplication.processed_by", back_populates="loan_officer")
