from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.settings import settings


def create_access_token(data: dict[str, Any]) -> str:
    """Create a signed JWT access token for the supplied user identity."""

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_TTL_MINUTES)

    payload = {
        "sub": data["username"],
        "role": data["role"],
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.get_jwt_secret(),
        algorithm=settings.JWT_ALGORITHM,
    )