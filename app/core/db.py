from sqlmodel import Session, create_engine, SQLModel

from app.core.config import settings

engine = create_engine(str(settings.sqlalchemy_db_uri))


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    from app.models.agent import Agent

    SQLModel.metadata.create_all(engine)
