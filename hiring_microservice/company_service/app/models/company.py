from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    location = Column(String)
    website = Column(String)
    industry = Column(String)
