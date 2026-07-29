# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this repository, please do **NOT** open a public issue.

Instead, please report the vulnerability directly to the project security maintainers by emailing security@gateway-project.local or opening a private security advisory on GitHub.

### Security Best Practices Implemented
- **Secrets Validation**: Sensitive configurations use Pydantic `SecretStr` enforcing minimum secret length in production.
- **Timing Attack Prevention**: API key checks use `secrets.compare_digest`.
- **Password Security**: Passwords are stored as salted `PBKDF2-HMAC-SHA256` hashes (100,000 iterations).
- **Network Boundary Protection**: Hop-by-hop HTTP headers are stripped prior to microservice proxy forwarding.
