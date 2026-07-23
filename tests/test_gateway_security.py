import pytest

from app.core.security import hash_password, verify_password, verify_token
from app.services.auth import create_access_token


def test_password_hashing_and_verification():
    raw_password = "SuperSecretPassword123!"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert "$" in hashed
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation_and_verification():
    data = {"username": "testuser", "role": "admin"}
    token = create_access_token(data)

    payload = verify_token(token)

    assert payload["sub"] == "testuser"
    assert payload["role"] == "admin"
    assert "exp" in payload
