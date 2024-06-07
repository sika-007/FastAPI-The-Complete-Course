from utils import *
from app.routers.users import get_db, get_current_user
from starlette import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "sika_007"
    assert response.json().get("email") == "nsikakthomas102@gmail.com"
    assert response.json().get("first_name") == "Nsikak"
    assert response.json().get("last_name") == "Thomas"
    assert response.json().get("role") == "admin"
    assert response.json()["phone_number"] == "+234811111111"


def test_change_password_success(test_user):
    response = client.patch("/users/change_password",
                            json={"current_password": "test12345", "new_password": "test123456"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.patch("/users/change_password",
                            json={"current_password": "wrong_password", "new_password": "test123456"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "You provided a wrong password"}


def test_change_phone_number_success(test_user):
    response = client.put("/users/user/phone?phone_number=8167739545")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestSessionLocal()
    user = db.query(Users).filter(Users.id == 1).first()
    assert user.phone_number == "8167739545"
