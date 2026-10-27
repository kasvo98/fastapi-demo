from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listens_for
from .models import Base
from .settings import get_settings


def init_db(engine):
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


settings = get_settings()
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
init_db(engine)
