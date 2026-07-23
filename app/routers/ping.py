from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Gateway"]
)


@router.get("/ping")
def ping():
    return {
        "message": "pong"
    }