
import pytest
from pydantic import ValidationError

from app.schemas import UserCreate
from app.security import hash_password, verify_password


def test_password_hashing():
    password = "TestPassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_wrong_password():
    hashed = hash_password("CorrectPassword123!")

    assert not verify_password("WrongPassword123!", hashed)


def test_valid_user():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="Password123!"
    )

    assert user.username == "testuser"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="not-an-email",
            password="Password123!"
        )


def test_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            password="123"
        )
