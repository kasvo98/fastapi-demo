from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listens_for
from .models import Base
from .settings import get_settings



def create_db_engine(url, dbms):
    configured_engine = create_engine(url, connect_args={"check_same_thread": False})

    if dbms == "SQLite":
        @listens_for(configured_engine, "connect")
        def enable_foreign_keys(connection, connection_record):
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return configured_engine


def init_db(engine):
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


settings = get_settings()
engine = create_db_engine(settings.database_url, settings.dbms)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
init_db(engine)
