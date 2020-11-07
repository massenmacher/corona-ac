from sqlalchemy import Column, Integer, String, TIMESTAMP
from .Base import db

class CaseDataEntry(db.Model):
    __tablename__ = 'cases_ac'

    id = Column(Integer, primary_key=True)
    cases_region = Column(Integer)
    cases_city = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    timestamp = Column(TIMESTAMP, unique=True)
    alsdorf = Column(Integer)
    baesweiler = Column(Integer)
    eschweiler = Column(Integer)
    herzogenrath = Column(Integer)
    monschau = Column(Integer)
    roetgen = Column(Integer)
    simmerath = Column(Integer)
    stolberg = Column(Integer)
    wuerselen = Column(Integer)
    not_associated = Column(Integer)