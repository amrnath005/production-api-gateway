import time
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.settings import settings
from app.services.cache import cache_service

clients: dict[str, dict[str, float | int]] = {}


def get_client_ip(request: Request) -> str:
    """Extract real client IP address from proxy headers or request client."""

    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return "127.0.0.1"


def cleanup_expired_clients(current_time: float) -> None:
    """Evict expired client tracking entries to prevent memory leaks."""

    if len(clients) > 10000:
        expired_ips = [
            ip for ip, data in clients.items()
            if current_time - float(data["start"]) > settings.RATE_LIMIT_WINDOW
        ]
        for ip in expired_ips:
            clients.pop(ip, None)


async def is_rate_limited_redis(client_ip: str) -> bool:
    """Perform sliding window rate limiting using Redis if connected."""

    if not cache_service.is_connected or not cache_service._client:
        return False

    key = f"rate_limit:{client_ip}"
    try:
        current_count = await cache_service._client.incr(key)
        if current_count == 1:
            await cache_service._client.expire(key, settings.RATE_LIMIT_WINDOW)

        return current_count > settings.RATE_LIMIT
    except Exception:
        return False


async def rate_limit(request: Request, call_next):
    client_ip = get_client_ip(request)
    current_time = time.time()

    # Try Redis rate limit first if available
    if cache_service.is_connected:
        if await is_rate_limited_redis(client_ip):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests"},
            )
    else:
        # Fallback to in-memory window rate limiting
        cleanup_expired_clients(current_time)

        client_data = clients.get(client_ip)
        if not client_data or (current_time - float(client_data["start"])) > settings.RATE_LIMIT_WINDOW:
            clients[client_ip] = {
                "count": 1,
                "start": current_time,
            }
        else:
            clients[client_ip]["count"] = int(client_data["count"]) + 1
            if int(clients[client_ip]["count"]) > settings.RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too Many Requests"},
                )

    response = await call_next(request)
    return response