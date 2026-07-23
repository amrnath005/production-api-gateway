from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.models.user import UserCreate, UserResponse, UserUpdate
from app.core.dependencies import get_api_key

router = APIRouter(
    prefix="/api/v1",
    tags=["Users"]
)


def _is_integrity_error(exc: Exception) -> bool:
    return exc.__class__.__name__ == "IntegrityError"


from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.users import UserRepository


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserCreate,
    repository: Annotated[Any, Depends(get_user_repository)],
    api_key: str = Depends(get_api_key),
):
    try:
        return await repository.create(user)
    except Exception as exc:
        if _is_integrity_error(exc):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this username or email already exists",
            ) from exc
        raise


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    repository: Annotated[Any, Depends(get_user_repository)],
    api_key: str = Depends(get_api_key),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await repository.list(limit=limit, offset=offset)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    repository: Annotated[Any, Depends(get_user_repository)],
    api_key: str = Depends(get_api_key),
):
    user = await repository.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    repository: Annotated[Any, Depends(get_user_repository)],
    api_key: str = Depends(get_api_key),
):
    try:
        user = await repository.update(user_id, user_update)
    except Exception as exc:
        if _is_integrity_error(exc):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this username or email already exists",
            ) from exc
        raise

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    repository: Annotated[Any, Depends(get_user_repository)],
    api_key: str = Depends(get_api_key),
):
    deleted = await repository.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
