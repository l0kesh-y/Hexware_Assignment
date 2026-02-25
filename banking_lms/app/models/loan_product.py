from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class LoanProduct(Base):
    __tablename__ = "loan_products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    max_amount = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    description = Column(String)
    
    # Relationships
    loan_applications = relationship("LoanApplication", back_populates="product")
