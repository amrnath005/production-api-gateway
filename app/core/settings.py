import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "api-gateway")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
    ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8003")

    REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", 5))
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_POOL_SIZE = int(os.getenv("REDIS_POOL_SIZE", 10))
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 60))
    CACHE_BYPASS = os.getenv("CACHE_BYPASS", "false").lower() == "true"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://gateway:gateway_password@localhost:5432/api_gateway",
    )
    DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", 10))
    DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", 20))
    DATABASE_POOL_TIMEOUT = int(os.getenv("DATABASE_POOL_TIMEOUT", 30))
    DATABASE_POOL_RECYCLE_SECONDS = int(os.getenv("DATABASE_POOL_RECYCLE_SECONDS", 1800))
    DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"

    JWT_SECRET = os.getenv("JWT_SECRET", "my_super_secret_key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_TTL_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_TTL_MINUTES", 60))

    API_KEY = os.getenv("API_KEY", "my-secret-api-key")
    API_KEY_HEADER = os.getenv("API_KEY_HEADER", "X-API-Key")


settings = Settings()
