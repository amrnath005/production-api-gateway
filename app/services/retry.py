import asyncio
import httpx

from app.services.metrics import RETRY_COUNT


class RetryService:

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 0.1
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay

    async def execute(self, request_function):

        delay = self.initial_delay

        last_exception = None

        for attempt in range(self.max_retries):

            try:

                return await request_function()

            except (
                httpx.ConnectError,
                httpx.TimeoutException,
                httpx.NetworkError,
            ) as e:

                last_exception = e

                RETRY_COUNT.inc()

                if attempt < self.max_retries - 1:

                    await asyncio.sleep(delay)

                    delay *= 2

        raise last_exception


retry_service = RetryService()