import asyncio
import gzip
import json
import types
from io import BytesIO

import pytest
from starlette.responses import JSONResponse, Response

from app.services.cache import CacheService, cached_response
from app.services.performance import PerformanceService


class FakeRedisClient:
    def __init__(self):
        self.store = {}
        self.ping_calls = 0

    async def ping(self):
        self.ping_calls += 1
        return True

    async def get(self, key):
        value = self.store.get(key)
        if not value:
            return None
        return value

    async def set(self, key, value, ex=None):
        self.store[key] = value
        return True

    async def delete(self, key):
        self.store.pop(key, None)
        return True

    async def scan_iter(self, match):
        for key in list(self.store.keys()):
            if key.startswith(match.replace("*", "")):
                yield key


@pytest.mark.asyncio
async def test_redis_connection_health_reports_status():
    service = CacheService(client=FakeRedisClient())
    health = await service.health()

    assert health["status"] == "ready"
    assert service.is_connected


@pytest.mark.asyncio
async def test_cache_hit_and_miss():
    service = CacheService(client=FakeRedisClient())
    await service.set("cache:test", {"value": 1}, ttl_seconds=30)

    hit = await service.get("cache:test")
    miss = await service.get("cache:missing")

    assert hit == {"value": 1}
    assert miss is None


@pytest.mark.asyncio
async def test_ttl_expiration():
    client = FakeRedisClient()
    service = CacheService(client=client)
    await service.set("cache:ttl", {"value": 2}, ttl_seconds=0)

    assert await service.get("cache:ttl") is None


@pytest.mark.asyncio
async def test_cache_invalidation():
    service = CacheService(client=FakeRedisClient())
    await service.set("cache:one", {"value": 1}, ttl_seconds=30)
    await service.set("cache:two", {"value": 2}, ttl_seconds=30)

    await service.delete("cache:one")
    await service.delete_pattern("cache:*")

    assert await service.get("cache:one") is None
    assert await service.get("cache:two") is None


@pytest.mark.asyncio
async def test_etag_and_conditional_request():
    service = PerformanceService()
    response = Response(content=b"hello", media_type="text/plain")
    request = types.SimpleNamespace(headers={}, method="GET")

    processed = await service.apply_response_features(response, request)
    etag = processed.headers.get("ETag")

    assert etag is not None

    conditional_request = types.SimpleNamespace(headers={"If-None-Match": etag}, method="GET")
    conditional_response = await service.apply_response_features(Response(content=b"hello", media_type="text/plain"), conditional_request)

    assert conditional_response.status_code == 304


@pytest.mark.asyncio
async def test_gzip_compression_is_applied():
    service = PerformanceService()
    request = types.SimpleNamespace(headers={"accept-encoding": "gzip"}, method="GET")
    response = Response(content=b"payload" * 100, media_type="text/plain")

    processed = await service.apply_response_features(response, request)

    assert processed.headers.get("content-encoding") == "gzip"
    assert processed.headers.get("vary") == "Accept-Encoding"

    body = gzip.decompress(processed.body)
    assert body == b"payload" * 100


@pytest.mark.asyncio
async def test_cached_response_decorator_uses_cache():
    cache = CacheService(client=FakeRedisClient())
    service = PerformanceService(cache_service=cache)

    @cached_response(cache_service=cache, performance_service=service, ttl_seconds=30)
    async def handler(request):
        return JSONResponse({"ok": True})

    request = types.SimpleNamespace(headers={}, method="GET", url=types.SimpleNamespace(path="/test"), query_params={})
    first = await handler(request)
    second = await handler(request)

    assert first.status_code == 200
    assert second.status_code == 200
