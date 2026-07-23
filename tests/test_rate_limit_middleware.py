import unittest
from starlette.requests import Request
from starlette.responses import Response

from app.middleware.rate_limit import rate_limit


class RateLimitMiddlewareTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_the_response_for_allowed_requests(self):
        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [],
            "query_string": b"",
            "client": ("127.0.0.1", 12345),
            "server": ("testserver", 80),
        }

        request = Request(scope, receive)
        expected_response = Response(status_code=200)

        async def call_next(_request):
            return expected_response

        result = await rate_limit(request, call_next)

        self.assertIs(result, expected_response)


if __name__ == "__main__":
    unittest.main()
