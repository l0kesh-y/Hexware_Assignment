from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_date = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)
    condition_on_return = Column(String, nullable=True)
    
    # Relationships
    asset = relationship("Asset", back_populates="assignments")
    user = relationship("User", back_populates="asset_assignments")
