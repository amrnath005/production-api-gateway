from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["System"]
)


@router.get("/version")
def version():
    return {
        "service": "API Gateway",
        "version": "1.0.0",
        "python": "3.14",
        "framework": "FastAPI"
    }