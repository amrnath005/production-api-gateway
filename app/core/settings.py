from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Values that must never be used when ENVIRONMENT=production.
_INSECURE_JWT_SECRETS = frozenset(
    {
        "",
        "change-me-in-production",
        "my_super_secret_key",
        "dev-only-jwt-secret-change-me",
        "ci-jwt-secret",
    }
)
_INSECURE_API_KEYS = frozenset(
    {
        "",
        "change-me-in-production",
        "my-secret-api-key",
        "dev-only-api-key-change-me",
        "ci-api-key",
    }
)

_DEV_DEFAULT_DATABASE_URL = (
    "postgresql+asyncpg://gateway:gateway_password@localhost:5432/api_gateway"
)
_MIN_SECRET_LENGTH = 16


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "api-gateway"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "staging", "production", "test"] = "development"

    USER_SERVICE_URL: str = "http://localhost:8002"
    ORDER_SERVICE_URL: str = "http://localhost:8003"

    REQUEST_TIMEOUT: float = Field(default=5.0, gt=0)
    RATE_LIMIT: int = Field(default=5, ge=1)
    RATE_LIMIT_WINDOW: int = Field(default=60, ge=1)

    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_POOL_SIZE: int = Field(default=10, ge=1)
    CACHE_TTL_SECONDS: int = Field(default=60, ge=0)
    CACHE_BYPASS: bool = False

    DATABASE_URL: SecretStr = Field(
        default=SecretStr(_DEV_DEFAULT_DATABASE_URL),
        description="Async SQLAlchemy database URL.",
    )
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0)
    DATABASE_POOL_TIMEOUT: int = Field(default=30, ge=1)
    DATABASE_POOL_RECYCLE_SECONDS: int = Field(default=1800, ge=0)
    DATABASE_ECHO: bool = False

    JWT_SECRET: SecretStr = Field(
        default=SecretStr("dev-only-jwt-secret-change-me"),
        description="Signing key for JWT access tokens.",
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_TTL_MINUTES: int = Field(default=60, ge=1)

    API_KEY: SecretStr = Field(
        default=SecretStr("dev-only-api-key-change-me"),
        description="Shared API key for protected gateway routes.",
    )
    API_KEY_HEADER: str = "X-API-Key"

    @field_validator("JWT_ALGORITHM")
    @classmethod
    def validate_jwt_algorithm(cls, value: str) -> str:
        if not value:
            raise ValueError("JWT_ALGORITHM must not be empty.")
        return value

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.ENVIRONMENT != "production":
            return self

        jwt_secret = self.JWT_SECRET.get_secret_value()
        if jwt_secret in _INSECURE_JWT_SECRETS:
            raise ValueError(
                "JWT_SECRET uses an insecure or placeholder value in production."
            )
        if len(jwt_secret) < _MIN_SECRET_LENGTH:
            raise ValueError(
                f"JWT_SECRET must be at least {_MIN_SECRET_LENGTH} characters in production."
            )

        api_key = self.API_KEY.get_secret_value()
        if api_key in _INSECURE_API_KEYS:
            raise ValueError(
                "API_KEY uses an insecure or placeholder value in production."
            )
        if len(api_key) < _MIN_SECRET_LENGTH:
            raise ValueError(
                f"API_KEY must be at least {_MIN_SECRET_LENGTH} characters in production."
            )

        database_url = self.DATABASE_URL.get_secret_value()
        if database_url == _DEV_DEFAULT_DATABASE_URL:
            raise ValueError(
                "DATABASE_URL must be explicitly configured for production deployments."
            )
        if not database_url:
            raise ValueError("DATABASE_URL must not be empty in production.")

        return self

    def get_database_url(self) -> str:
        """Return the configured database URL as a plain string."""

        return self.DATABASE_URL.get_secret_value()

    def get_jwt_secret(self) -> str:
        """Return the JWT signing secret as a plain string."""

        return self.JWT_SECRET.get_secret_value()

    def get_api_key(self) -> str:
        """Return the configured API key as a plain string."""

        return self.API_KEY.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()


settings = get_settings()
