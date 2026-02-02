from typing import Any, Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.models.base import BaseModel  # this should be SQLModel-based
from backend.apis.deps import get_db
from backend.apis.main import api_router


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


# Use SQLModel's engine
SQL_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQL_DATABASE_URL, connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh DB for each test
    """
    SQLModel.metadata.create_all(engine)
    _app = start_application()
    yield _app
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    """
    Creates session with BEGIN/ROLLBACK wrapping each test function
    """
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Overrides get_db to use test session
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as c:
        yield c

import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def auth_headers(client: TestClient):
    # Register user
    register_data = {
        "full_name": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing"
    }
    res = client.post("/api/v1/users", json=register_data)
    assert res.status_code == 201

    # Login for token
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }
    res = client.post("/api/v1/token", data=login_data)
    assert res.status_code == 200

    token = res.json()["access_token"]
    assert token is not None

    return {"Authorization": f"Bearer {token}"}
