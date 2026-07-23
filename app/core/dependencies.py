import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import security, verify_token
from app.core.settings import settings


async def get_api_key(x_api_key: str = Header(default=None, alias=settings.API_KEY_HEADER)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required")

    if not secrets.compare_digest(x_api_key, settings.get_api_key()):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return x_api_key


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security)
    ]
):
    """
    Extracts the Bearer token from the Authorization header
    and returns the decoded JWT payload.
    """

    payload = verify_token(credentials)

    return payload


def require_role(required_role: str):

    def role_checker(
        current_user: Annotated[
            dict,
            Depends(get_current_user)
        ]
    ):

        if current_user["role"] != required_role:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return role_checker