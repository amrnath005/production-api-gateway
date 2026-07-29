# Redis Caching & RedisInsight Developer Guide

## Redis Operations
- **Connection**: `redis://redis:6379/0`
- **Keyspace Structure**:
  - `rate_limit:{client_ip}` (TTL: 60s)
  - `cache:{sha256_hash}` (TTL: 60s)

## RedisInsight Dashboard
Access RedisInsight UI at `http://localhost:5540` to view live key TTLs, memory consumption, and run Redis commands.
