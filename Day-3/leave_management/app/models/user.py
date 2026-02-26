from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN, MANAGER, EMPLOYEE
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Relationships
    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    leave_requests = relationship("LeaveRequest", foreign_keys="LeaveRequest.employee_id", back_populates="employee")
    approved_leaves = relationship("LeaveRequest", foreign_keys="LeaveRequest.approved_by", back_populates="approver")
    managed_department = relationship("Department", foreign_keys="Department.manager_id", back_populates="manager", uselist=False)
