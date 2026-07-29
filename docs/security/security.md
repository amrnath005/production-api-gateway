# Security Architecture & Risk Mitigation

The Gateway enforces OWASP best practices across all entry points:

---

## Security Countermeasures
1. **Password Security**: Passwords hashed using PBKDF2-HMAC-SHA256 (100,000 iterations + 16-byte random salt).
2. **Timing Attack Resistance**: API key validation uses `secrets.compare_digest`.
3. **Secret Protection**: Production mode rejects weak/default keys via Pydantic `SecretStr` validators.
4. **Header Stripping**: Hop-by-hop headers (`Host`, `Connection`, etc.) stripped prior to proxying.
5. **Rate Limiting**: IP-based rate limiting blocks brute-force authentication attacks.
