from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("loan_products.id"), nullable=False)
    requested_amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected, disbursed, closed
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    customer = relationship("User", foreign_keys=[user_id], back_populates="loan_applications")
    loan_officer = relationship("User", foreign_keys=[processed_by], back_populates="processed_applications")
    product = relationship("LoanProduct", back_populates="loan_applications")
    repayments = relationship("Repayment", back_populates="loan_application")
