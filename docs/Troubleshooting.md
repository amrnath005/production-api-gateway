# Troubleshooting & Ops Playbook

## Common Issues & Solutions

### 1. HTTP 503 Service Unavailable (Circuit Breaker OPEN)
- **Cause**: Backend service reached failure threshold (5 consecutive connection errors).
- **Fix**: Check status of downstream service (`user-service` or `order-service`). Circuit automatically transitions to `HALF_OPEN` after 30 seconds.

### 2. HTTP 504 Gateway Timeout
- **Cause**: Backend service failed to respond within `REQUEST_TIMEOUT` (default: 5.0 seconds).
- **Fix**: Check backend CPU/memory usage or increase `REQUEST_TIMEOUT` in environment variables.

### 3. HTTP 401 Unauthorized / Invalid API Key
- **Cause**: Missing or incorrect `X-API-Key` or `Authorization: Bearer <token>` header.
- **Fix**: Re-authenticate via `/login` or verify `API_KEY` setting matches request header.

### 4. Database Connection Failures
- **Cause**: PostgreSQL unavailable or max connections reached.
- **Fix**: Verify DB container status (`docker-compose ps postgres`) and pool settings (`DATABASE_POOL_SIZE`).
