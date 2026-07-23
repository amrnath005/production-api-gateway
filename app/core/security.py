import hashlib
import os
import secrets
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.settings import settings

# Creates the "Authorize" button in Swagger UI
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a plain text password using PBKDF2-HMAC-SHA256 with a random salt."""

    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored PBKDF2-HMAC-SHA256 hash."""

    if not hashed_password or "$" not in hashed_password:
        return False
    salt_hex, key_hex = hashed_password.split("$", 1)
    salt = bytes.fromhex(salt_hex)
    key = bytes.fromhex(key_hex)
    new_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100000)
    return secrets.compare_digest(key, new_key)


def verify_token(token_or_credentials: str | HTTPAuthorizationCredentials) -> dict:
    """Verify JWT access token and return decoded payload claims."""

    if isinstance(token_or_credentials, HTTPAuthorizationCredentials):
        token = token_or_credentials.credentials
    else:
        token = token_or_credentials

    try:
        payload = jwt.decode(
            token,
            settings.get_jwt_secret(),
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )