# Automated Testing Suite & Strategy

All application modules are tested using `pytest` and `pytest-asyncio`.

---

## Test Execution
Run the full test suite:

```bash
pytest
```

### Test Coverage Summary (29 Tests Passing)
- **`tests/test_auth.py`**: Tests API key verification, invalid key rejection, and token validation.
- **`tests/test_caching_performance.py`**: Tests Redis caching, TTL expiration, invalidation, ETags, and Gzip compression.
- **`tests/test_gateway_exceptions.py`**: Tests custom domain exception mapping (CircuitOpen, Timeout, ServiceUnavailable).
- **`tests/test_gateway_security.py`**: Tests PBKDF2 password hashing and token payload claims.
- **`tests/test_observability.py`**: Tests logging context variables and trace header formatting.
- **`tests/test_persistence.py`**: Tests UserRepository CRUD operations and async session scoping.
- **`tests/test_rate_limit_middleware.py`**: Tests sliding window rate limiting and 429 response emission.
- **`tests/test_settings.py`**: Tests environment variable validation and SecretStr extraction.
