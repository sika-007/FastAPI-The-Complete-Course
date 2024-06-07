from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base
from app.main import app
from fastapi.testclient import TestClient
import pytest
from app.models import Todos, Users
from app.routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False}, poolclass=StaticPool)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close


def override_get_current_user():
    return {"username": "sika_007", "id": 1, "role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="sika_007",
        email="nsikakthomas102@gmail.com",
        first_name="Nsikak",
        last_name="Thomas",
        hashed_password=bcrypt_context.hash("test12345"),
        role="admin",
        phone_number="+234811111111"
    )

    db = TestSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
