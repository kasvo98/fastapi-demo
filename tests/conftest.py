import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import create_db_engine, get_db
from app.models import Base


@pytest.fixture
def client(tmp_path):
    database_path = tmp_path / "test.db"
    test_engine = create_db_engine(f"sqlite:///{database_path.as_posix()}", "SQLite")
    previous_overrides = dict(app.dependency_overrides)
    try:
        Base.metadata.create_all(bind=test_engine)
        TestingSession = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

        def override_get_db():
            db = TestingSession()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        test_engine.dispose()
        database_path.unlink(missing_ok=True)