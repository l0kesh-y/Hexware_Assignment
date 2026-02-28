from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.base import Base

class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False, index=True)
    candidate_id = Column(Integer, nullable=False, index=True)
    resume_url = Column(String)
    cover_letter = Column(Text)
    status = Column(String, default='pending')  # 'pending', 'reviewed', 'shortlisted', 'rejected', 'accepted'
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
