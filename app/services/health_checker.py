import httpx


class HealthChecker:

    async def is_healthy(self, instance: str) -> bool:
        """Check whether an instance responds to its health endpoint."""

        base_url = instance.rstrip("/")
        health_url = f"{base_url}/health"

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(health_url)
                return response.status_code < 500
        except (
            httpx.ConnectError,
            httpx.TimeoutException,
            httpx.NetworkError,
        ):
            return False


health_checker = HealthChecker()