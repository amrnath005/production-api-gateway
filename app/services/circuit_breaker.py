import time

from app.services.metrics import CIRCUIT_OPEN


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = {}

        self.last_failure_time = {}

        self.state = {}

    def before_request(self, backend: str):

        state = self.state.get(
            backend,
            "CLOSED"
        )

        if state == "OPEN":

            elapsed = (
                time.time()
                - self.last_failure_time[backend]
            )

            if elapsed >= self.recovery_timeout:

                self.state[backend] = "HALF_OPEN"

            else:

                raise RuntimeError(
                    f"Circuit OPEN for {backend}"
                )

    def record_success(self, backend: str):

        self.failure_count[backend] = 0

        self.state[backend] = "CLOSED"

    def record_failure(self, backend: str):

        failures = (
            self.failure_count.get(
                backend,
                0
            ) + 1
        )

        self.failure_count[backend] = failures

        self.last_failure_time[backend] = time.time()

        if failures >= self.failure_threshold:

            CIRCUIT_OPEN.inc()

            self.state[backend] = "OPEN"


circuit_breaker = CircuitBreaker()