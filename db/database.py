from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.basemodel import Base
from config import settings

engine = create_engine(
    url=settings.db_url,
    echo=settings.db_echo,
)


sessionmaker = sessionmaker(bind=engine)


def get_session() -> Session:
    return sessionmaker()
