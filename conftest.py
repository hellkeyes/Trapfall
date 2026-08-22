# onfig for test files

import os
from pathlib import Path
from dotenv import load_dotenv

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.models.user import User
from backend.app.auth.dependencies import get_current_user

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db   # a dictionary that fastapi check before resolving depends and override our get_db with get_test_db

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db_session):   # getting db session for a particular test
    with TestClient(app) as c:
        yield c

def get_test_current_user():
    return User(id=1, username="testuser", email="test@example.com")

app.dependency_overrides[get_current_user] = get_test_current_user

@pytest.fixture(autouse=True)
def reset_current_user_override():
    yield
    app.dependency_overrides[get_current_user] = get_test_current_user
