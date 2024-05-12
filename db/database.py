from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.basemodel import Base

engine = create_engine("sqlite:///sqlite.db", echo=True)


sessionmaker = sessionmaker(bind=engine)


def get_session() -> Session:
    return sessionmaker()
