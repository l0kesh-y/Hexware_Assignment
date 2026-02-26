from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True, nullable=False, index=True)
    asset_type = Column(String, nullable=False)  # Laptop, Monitor, License, Vehicle, etc.
    brand = Column(String)
    model = Column(String)
    purchase_date = Column(Date)
    status = Column(String, default="AVAILABLE")  # AVAILABLE, ASSIGNED, MAINTENANCE, RETIRED
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Relationships
    department = relationship("Department", back_populates="assets")
    assignments = relationship("AssetAssignment", back_populates="asset")
