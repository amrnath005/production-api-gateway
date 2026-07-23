from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import require_role

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("")
async def admin_dashboard(
    current_user: Annotated[
        dict,
        Depends(require_role("admin"))
    ]
):
    return {
        "message": "Welcome Admin",
        "username": current_user["sub"],
        "role": current_user["role"]
    }