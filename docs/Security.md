# Security Practices & Threat Model

## 1. Secrets Management
- All sensitive variables (`JWT_SECRET`, `API_KEY`, `DATABASE_URL`) are read via Pydantic `SecretStr`.
- Production environment checks mandate 16+ character secrets and non-default database connection strings.

## 2. Token Security
- JWTs are signed with HS256 algorithm and expire after `JWT_ACCESS_TOKEN_TTL_MINUTES`.
- Token expiration signatures (`exp`) are validated on every request.

## 3. Cryptographic Hardening
- Passwords stored in the database are hashed with PBKDF2-HMAC-SHA256 (100,000 iterations + 16-byte salt).
- API key verification uses `secrets.compare_digest` to prevent timing attacks.

## 4. Input & Network Security
- Request body and parameters validated via Pydantic models.
- Rate limiting protects against brute-force and DoS attacks.
- Hop-by-hop HTTP headers stripped before proxying to downstream backends.
