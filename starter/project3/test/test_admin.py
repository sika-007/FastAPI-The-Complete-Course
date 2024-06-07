from utils import *
from starlette import status
from app.routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete": False, "title": "Learn to code!",
                                "description": "Need to learn everyday", "id": 1, "priority": 5, "owner_id": 1}]


def test_admin_delete_todos_authenticated(test_todo):
    response = client.delete("/admin/todos/1")
    assert response.status_code == 204
    db = TestSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None


def test_admin_delete_todos_not_found(test_todo):
    response = client.delete("/admin/todos/999")
    assert response.status_code == 404
