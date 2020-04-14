from sqlalchemy import Column, Integer, String, TIMESTAMP
from .Base import Base

class CaseDataEntry(Base):
    __tablename__ = 'cases_ac'

    id = Column(Integer, primary_key=True)
    cases_region = Column(Integer)
    cases_city = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    timestamp = Column(TIMESTAMP, unique=True)
