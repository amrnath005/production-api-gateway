from typing import Any

from fastapi import APIRouter, Response, status

from app.services.cache import cache_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Health"]
)


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


async def _database_health() -> dict[str, Any]:
    try:
        from app.db.health import check_database_health
    except ImportError as exc:
        return {
            "status": "unavailable",
            "error": f"database dependencies are not installed: {exc.name}",
        }

    return await check_database_health()


@router.get("/health/db")
async def database_health_check(response: Response) -> dict[str, Any]:
    health = await _database_health()
    if health["status"] != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return health


@router.get("/ready")
async def readiness_check(response: Response) -> dict[str, Any]:
    database = await _database_health()
    cache = await cache_service.health()

    checks = {
        "database": database,
        "cache": cache,
    }
    ready = all(check["status"] == "ready" for check in checks.values())

    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ready" if ready else "degraded",
        "checks": checks,
    }
