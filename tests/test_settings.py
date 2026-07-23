import pytest
from pydantic import SecretStr, ValidationError

from app.core.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_development_allows_placeholder_secrets():
    settings = Settings(
        ENVIRONMENT="development",
        JWT_SECRET=SecretStr("change-me-in-production"),
        API_KEY=SecretStr("change-me-in-production"),
    )

    assert settings.get_jwt_secret() == "change-me-in-production"
    assert settings.get_api_key() == "change-me-in-production"


def test_production_rejects_placeholder_jwt_secret():
    with pytest.raises(ValidationError, match="JWT_SECRET uses an insecure"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET=SecretStr("change-me-in-production"),
            API_KEY=SecretStr("production-api-key-value-123"),
            DATABASE_URL=SecretStr(
                "postgresql+asyncpg://gateway:strong_password@postgres:5432/api_gateway"
            ),
        )


def test_production_rejects_short_jwt_secret():
    with pytest.raises(ValidationError, match="JWT_SECRET must be at least"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET=SecretStr("short-secret"),
            API_KEY=SecretStr("production-api-key-value-123"),
            DATABASE_URL=SecretStr(
                "postgresql+asyncpg://gateway:strong_password@postgres:5432/api_gateway"
            ),
        )


def test_production_rejects_placeholder_api_key():
    with pytest.raises(ValidationError, match="API_KEY uses an insecure"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET=SecretStr("production-jwt-secret-value-123"),
            API_KEY=SecretStr("change-me-in-production"),
            DATABASE_URL=SecretStr(
                "postgresql+asyncpg://gateway:strong_password@postgres:5432/api_gateway"
            ),
        )


def test_production_rejects_short_api_key():
    with pytest.raises(ValidationError, match="API_KEY must be at least"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET=SecretStr("production-jwt-secret-value-123"),
            API_KEY=SecretStr("short-key"),
            DATABASE_URL=SecretStr(
                "postgresql+asyncpg://gateway:strong_password@postgres:5432/api_gateway"
            ),
        )


def test_production_rejects_dev_default_database_url():
    with pytest.raises(ValidationError, match="DATABASE_URL must be explicitly configured"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET=SecretStr("production-jwt-secret-value-123"),
            API_KEY=SecretStr("production-api-key-value-123"),
            DATABASE_URL=SecretStr(
                "postgresql+asyncpg://gateway:gateway_password@localhost:5432/api_gateway"
            ),
        )


def test_production_accepts_explicitly_configured_secrets():
    settings = Settings(
        ENVIRONMENT="production",
        JWT_SECRET=SecretStr("production-jwt-secret-value-123"),
        API_KEY=SecretStr("production-api-key-value-123"),
        DATABASE_URL=SecretStr(
            "postgresql+asyncpg://gateway:strong_password@postgres:5432/api_gateway"
        ),
    )

    assert settings.get_jwt_secret() == "production-jwt-secret-value-123"
    assert settings.get_api_key() == "production-api-key-value-123"
    assert "postgres:5432" in settings.get_database_url()


def test_secret_str_is_redacted_in_repr():
    settings = Settings(
        ENVIRONMENT="development",
        JWT_SECRET=SecretStr("super-secret-value"),
        API_KEY=SecretStr("super-api-key-value"),
    )

    rendered = repr(settings)

    assert "super-secret-value" not in rendered
    assert "super-api-key-value" not in rendered


def test_settings_loads_cache_bypass_from_env(monkeypatch):
    monkeypatch.setenv("CACHE_BYPASS", "true")

    settings = Settings()

    assert settings.CACHE_BYPASS is True


def test_get_settings_returns_cached_instance():
    first = get_settings()
    second = get_settings()

    assert first is second
