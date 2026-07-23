import asyncio
import time

from app.core.routes import SERVICE_REGISTRY
from app.services.health_checker import health_checker
from app.services.metrics import (
    BACKEND_AVAILABILITY,
    HEALTHY_INSTANCES,
    HEALTH_CHECK_DURATION,
    LAST_HEALTH_CHECK,
    UNHEALTHY_INSTANCES,
)


class HealthMonitor:

    def __init__(self):
        self.health_status = {}
        self.last_check = None
        self.last_check_duration = 0.0

    async def update_health(self):
        start_time = time.perf_counter()

        for _, instances in SERVICE_REGISTRY.items():
            for instance in instances:
                healthy = await health_checker.is_healthy(instance)
                self.health_status[instance] = healthy
                BACKEND_AVAILABILITY.labels(backend=instance).set(1 if healthy else 0)

        healthy_count = sum(1 for value in self.health_status.values() if value)
        unhealthy_count = len(self.health_status) - healthy_count
        HEALTHY_INSTANCES.set(healthy_count)
        UNHEALTHY_INSTANCES.set(unhealthy_count)

        self.last_check = time.time()
        self.last_check_duration = time.perf_counter() - start_time
        LAST_HEALTH_CHECK.set(self.last_check)
        for instance in self.health_status:
            HEALTH_CHECK_DURATION.labels(backend=instance).observe(self.last_check_duration)

    async def check_all_services(self):
        await self.update_health()
        while True:
            await self.update_health()
            await asyncio.sleep(10)

    def is_healthy(self, instance: str) -> bool:
        return self.health_status.get(instance, False)


health_monitor = HealthMonitor()