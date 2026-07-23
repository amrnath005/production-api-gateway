from app.core.settings import settings

SERVICE_REGISTRY = {
    "users": [
        settings.USER_SERVICE_URL,
        "http://localhost:8002",
        "http://localhost:8003",
    ],
    "orders": [
        settings.ORDER_SERVICE_URL,
    ],
}