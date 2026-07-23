from fastapi import APIRouter, HTTPException, Query, Request

from app.services.cache import cache_service

router = APIRouter(prefix="/api/v1/cache", tags=["Cache"])


@router.delete("/invalidate")
async def invalidate_cache(key: str | None = None, pattern: str | None = None) -> dict[str, object]:
    if key:
        deleted = await cache_service.delete(key)
        return {"status": "ok", "deleted": deleted}

    if pattern:
        deleted = await cache_service.delete_pattern(pattern)
        return {"status": "ok", "deleted": deleted}

    raise HTTPException(status_code=400, detail="Provide key or pattern")
