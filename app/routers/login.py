from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.auth import create_access_token

router = APIRouter(
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(data: LoginRequest):

    if (
        data.username != "admin"
        or
        data.password != "admin123"
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "username": data.username,
            "role": "admin"
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }