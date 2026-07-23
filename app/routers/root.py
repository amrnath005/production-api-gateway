from fastapi import APIRouter
from app.core.settings import settings

router = APIRouter(
    prefix="/api/v1",
    tags=["Gateway"]
)


@router.get("/")
def read_root():
  return {
    "service": settings.APP_NAME,
    "version": settings.APP_VERSION,
    "status": "running",
    "environment": settings.ENVIRONMENT
}