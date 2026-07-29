# Authentication & Security Architecture

Authentication is implemented using JWT access tokens and constant-time API key verification.

---

## 1. Password Hashing
User passwords are stored as salted PBKDF2-HMAC-SHA256 hashes with 100,000 iterations:

```python
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"pbkdf2_sha256$100000${salt.hex()}${key.hex()}"
```

## 2. API Key Verification
Administrative user CRUD routes require the `X-API-Key` header verified with constant-time equality checks:

```python
async def get_api_key(x_api_key: str = Header(default=None, alias=settings.API_KEY_HEADER)):
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.get_api_key()):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
```

## 3. JWT Bearer Tokens
Signed with HS256 algorithm and configured expiration TTL (`JWT_ACCESS_TOKEN_TTL_MINUTES`).
