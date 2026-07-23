from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.middleware.logging import log_requests
from app.middleware.rate_limit import rate_limit

from app.routers.root import router as root_router
from app.routers.health import router as health_router
from app.routers.version import router as version_router
from app.routers.ping import router as ping_router
from app.routers.login import router as login_router
from app.routers.profile import router as profile_router
from app.routers.admin import router as admin_router

from app.routers import users
from app.routers import proxy
from app.routers.cache import router as cache_router
from app.routers.metrics import router as metrics_router

from app.core.observability import configure_logging, configure_tracing
from app.services.cache import cache_service
from app.services.health_monitor import health_monitor
from app.services.gateway import gateway_service
from app.db.lifespan import close_database_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once when the API Gateway starts.
    Starts the background health monitor.
    """

    monitor_task = asyncio.create_task(
        health_monitor.check_all_services()
    )

    await cache_service.connect()

    try:
        yield
    finally:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        await gateway_service.close()
        await cache_service.close()
        await close_database_pool()
configure_logging()

app = FastAPI(
    title="Production API Gateway",
    version="1.0.0",
    lifespan=lifespan
)

configure_tracing(app)

# -------------------------
# Middleware
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)
app.middleware("http")(rate_limit)

# -------------------------
# Public Routes
# -------------------------

app.include_router(root_router)
app.include_router(health_router)
app.include_router(version_router)
app.include_router(ping_router)
app.include_router(login_router)

# -------------------------
# Protected Routes
# -------------------------

app.include_router(profile_router)
app.include_router(admin_router)

# -------------------------
# Gateway & Domain Routes
# -------------------------

app.include_router(users.router)
app.include_router(metrics_router)
app.include_router(cache_router)
app.include_router(proxy.router)
