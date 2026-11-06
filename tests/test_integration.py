
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models import User
from app.security import verify_password
from app.users import get_engine


def test_create_user_and_uniqueness():
    client = TestClient(app)

    username = "user_" + uuid4().hex[:12]
    email = username + "@example.com"

    user_data = {
        "username": username,
        "email": email,
        "password": "Password123!"
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    result = response.json()
    assert result["username"] == username
    assert "password_hash" not in result
    assert "password" not in result

    user_id = result["id"]

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == email

    duplicate = client.post("/users", json=user_data)
    assert duplicate.status_code == 409

    duplicate_email = client.post(
        "/users",
        json={
            "username": "other_" + uuid4().hex[:12],
            "email": email,
            "password": "Password123!"
        }
    )
    assert duplicate_email.status_code == 409

    with Session(get_engine()) as session:
        saved_user = session.get(User, user_id)
        assert saved_user is not None
        assert saved_user.password_hash != "Password123!"
        assert verify_password(
            "Password123!", saved_user.password_hash
        )
        session.delete(saved_user)
        session.commit()


def test_invalid_user_email():
    client = TestClient(app)

    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "Password123!"
        }
    )

    assert response.status_code == 422


def test_user_not_found():
    client = TestClient(app)

    response = client.get("/users/999999999")
    assert response.status_code == 404
