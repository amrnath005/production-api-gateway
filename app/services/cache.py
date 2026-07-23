import hashlib
import json
import os
import time
from typing import Any

from starlette.responses import Response

from app.core.settings import settings
from app.services.metrics import CACHE_HITS, CACHE_MISSES, CACHE_LATENCY, REDIS_CONNECTIONS, CACHED_RESPONSES


class CacheService:
    def __init__(self, client: Any | None = None) -> None:
        self._client = client
        self.is_connected = False

    async def connect(self) -> None:
        if self._client is None:
            try:
                import redis.asyncio as redis
            except ImportError:
                self.is_connected = False
                return

            self._client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                max_connections=settings.REDIS_POOL_SIZE,
            )

        if hasattr(self._client, "ping"):
            try:
                await self._client.ping()
                self.is_connected = True
                return
            except Exception:
                self.is_connected = False
                return

        self.is_connected = True

    async def health(self) -> dict[str, Any]:
        await self.connect()

        if self.is_connected:
            return {"status": "ready", "url": settings.REDIS_URL}

        return {"status": "unavailable", "url": settings.REDIS_URL}

    async def get(self, key: str) -> Any | None:
        start = time.perf_counter()
        try:
            await self.connect()
            if not self.is_connected:
                CACHE_MISSES.inc()
                return None

            value = await self._client.get(key)
            if value is None:
                CACHE_MISSES.inc()
                return None

            CACHE_HITS.inc()
            CACHE_LATENCY.observe(time.perf_counter() - start)
            return json.loads(value)
        except Exception:
            CACHE_MISSES.inc()
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> bool:
        try:
            await self.connect()
            if not self.is_connected:
                return False

            payload = json.dumps(value)
            if ttl_seconds is None:
                ttl_seconds = settings.CACHE_TTL_SECONDS
            if ttl_seconds <= 0:
                return True
            await self._client.set(key, payload, ex=ttl_seconds)
            CACHED_RESPONSES.inc()
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        try:
            await self.connect()
            if not self.is_connected:
                return False
            await self._client.delete(key)
            return True
        except Exception:
            return False

    async def delete_pattern(self, pattern: str) -> int:
        try:
            await self.connect()
            if not self.is_connected:
                return 0
            keys = [key async for key in self._client.scan_iter(pattern)]
            for key in keys:
                await self._client.delete(key)
            return len(keys)
        except Exception:
            return 0

    async def close(self) -> None:
        if self._client is not None:
            try:
                await self._client.close()
            except Exception:
                pass


cache_service = CacheService()


def build_cache_key(method: str, path: str, query: str, body: bytes | None = None) -> str:
    raw = f"{method}:{path}:{query}:{body or b''}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def cached_response(cache_service: CacheService, performance_service: Any | None = None, ttl_seconds: int | None = None, bypass: bool = False):
    def decorator(func):
        async def wrapper(request):
            if bypass:
                return await func(request)

            if request.method.upper() != "GET":
                return await func(request)

            cache_key = build_cache_key(
                method=request.method.upper(),
                path=request.url.path,
                query=str(request.query_params or ""),
            )
            cached_value = await cache_service.get(cache_key)
            if cached_value is not None:
                cached_body = cached_value.get("body") if isinstance(cached_value, dict) else None
                if isinstance(cached_value, dict) and cached_body is not None:
                    return Response(
                        content=cached_body.encode("utf-8"),
                        status_code=cached_value.get("status_code", 200),
                        media_type=cached_value.get("media_type", "application/json"),
                    )
                return cached_value

            response = await func(request)
            if hasattr(response, "body") and hasattr(response, "status_code"):
                await cache_service.set(cache_key, {"body": response.body.decode("utf-8"), "status_code": response.status_code, "media_type": response.media_type}, ttl_seconds=ttl_seconds)
                return response
            return response
        return wrapper
    return decorator
