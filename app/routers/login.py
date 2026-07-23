from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.db.session import get_session
from app.repositories.users import UserRepository
from app.services.auth import create_access_token

router = APIRouter(
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_username(data.username)

    if user and user.hashed_password:
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        role = getattr(user, "role", "user") or "user"
        token = create_access_token({"username": user.username, "role": role})
        return {"access_token": token, "token_type": "bearer"}

    # Development fallback
    if data.username == "admin" and data.password == "admin123":
        token = create_access_token({"username": data.username, "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )