from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Repayment(Base):
    __tablename__ = "repayments"
    
    id = Column(Integer, primary_key=True, index=True)
    loan_application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_status = Column(String, default="completed")  # completed, pending
    
    # Relationships
    loan_application = relationship("LoanApplication", back_populates="repayments")
