from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("")
async def profile(
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    return {
        "message": "Authenticated Successfully",
        "username": current_user["sub"],
        "role": current_user["role"],
        "token_payload": current_user
    }