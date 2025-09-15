from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.utils.config import Config

engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
