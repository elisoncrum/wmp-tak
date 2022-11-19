from . import config
from sqlmodel import SQLModel, create_engine

settings = config.Settings()
engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)