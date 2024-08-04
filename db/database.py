from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.basemodel import Base
from config import settings
from db.models import Quote

engine = create_engine(
    url=settings.db_url,
    echo=settings.db_echo,
)

sessionmaker = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return sessionmaker()
