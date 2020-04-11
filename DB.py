from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base

engine = None
session = None
db_session = scoped_session(lambda: create_session(bind=engine))


Base = declarative_base()


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine


def init_session():
    global session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def init_db():
    from models import CaseDataEntry
    Base.metadata.create_all(bind=engine)