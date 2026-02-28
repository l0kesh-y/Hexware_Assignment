from sqlalchemy import Column, Integer, String, Text, Float
from app.database.base import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    company_id = Column(Integer, nullable=False)
    location = Column(String)
    salary_min = Column(Float)
    salary_max = Column(Float)
    job_type = Column(String)  # 'full-time', 'part-time', 'contract', 'internship'
    experience_level = Column(String)  # 'entry', 'mid', 'senior'
    status = Column(String, default='active')  # 'active', 'closed', 'draft'
