# Redis Caching & Rate Limiting Engine

Redis 7 powers response caching and sliding window rate limiting.

---

## 1. Sliding Window Rate Limiter
Tracks client IP requests using Redis key `rate_limit:{client_ip}` (TTL: 60s). Falls back to in-memory rate limiting when Redis is offline.

## 2. Response Caching
Caches GET payloads in Redis key `cache:{sha256_hash}` (TTL: 60s).

### Cache Invalidation API
`DELETE /api/v1/cache/invalidate?key=...` or `?pattern=cache:*` allows targeted or wild-card cache invalidation.
