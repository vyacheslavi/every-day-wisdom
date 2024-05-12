from db.basemodel import Base
from db.database import engine


def create_db():
    Base.metadata.create_all(engine)


create_db()
