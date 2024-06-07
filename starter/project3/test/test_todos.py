from starlette import status
from app.db.get_db import get_db
from app.routers.auth import get_current_user
from app.models import Todos
import pytest
from utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "complete": False,
        "title": "Learn to code!",
        "description": "Need to learn everyday",
        "id": 1,
        "priority": 5,
        "owner_id": 1,
    }]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False,
        "title": "Learn to code!",
        "description": "Need to learn everyday",
        "id": 1,
        "priority": 5,
        "owner_id": 1,
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': "Not Found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "New todo",
        "description": "New todo description",
        "priority": 5,
        "complete": False
    }
    response = client.post("/todos/todo/", json=request_data)
    assert response.status_code == 201
    db = TestSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 2).first()
    assert todo.title == request_data.get("title")  # type: ignore
    assert todo.description == request_data.get("description")  # type: ignore
    assert todo.priority == request_data.get(
        "priority")  # type: ignore # type: ignore
    assert todo.complete == request_data.get("complete")  # type: ignore


def test_update_todo(test_todo):
    request_data = {
        "title": "A change made to the title",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == 204
    db = TestSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo.title == request_data.get("title")  # type: ignore
    assert todo.description == request_data.get("description")  # type: ignore
    assert todo.priority == request_data.get(
        "priority")  # type: ignore # type: ignore
    assert todo.complete == request_data.get("complete")  # type: ignore


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "A change made to the title",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 204
    db = TestSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo == None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
