# API Key Authentication Manual

Administrative and user CRUD routes (`/api/v1/users`) require the `X-API-Key` HTTP header.

---

## Implementation Details
The security dependency ([app/core/dependencies.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/core/dependencies.py)) compares the incoming header against `settings.get_api_key()`:

```python
async def get_api_key(x_api_key: str = Header(default=None, alias=settings.API_KEY_HEADER)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required")

    if not secrets.compare_digest(x_api_key, settings.get_api_key()):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return x_api_key
```

Constant-time comparison via `secrets.compare_digest` prevents side-channel timing attacks.
