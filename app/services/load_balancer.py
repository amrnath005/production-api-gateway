from collections import defaultdict

from app.services.health_monitor import health_monitor


class RoundRobinLoadBalancer:

    def __init__(self):
        self.current_index = defaultdict(int)

    async def get_next_instance(
        self,
        service_name: str,
        instances: list[str]
    ) -> str:

        if not instances:
            raise ValueError(
                f"No backend instances configured for '{service_name}'"
            )

        total = len(instances)

        # Try each backend once
        for _ in range(total):

            index = self.current_index[service_name]

            backend = instances[index]

            # Move to next backend for the next request
            self.current_index[service_name] = (
                index + 1
            ) % total

            # Read cached health status
            if health_monitor.is_healthy(backend):
                return backend

        raise RuntimeError(
            f"All backend instances for '{service_name}' are unavailable."
        )


load_balancer = RoundRobinLoadBalancer()