import gzip
import hashlib
import time
from typing import Any

from starlette.responses import Response

from app.services.metrics import CACHE_HIT_RATIO, COMPRESSION_USAGE


class PerformanceService:
    def __init__(self, cache_service: Any | None = None) -> None:
        self.cache_service = cache_service

    async def apply_response_features(self, response: Response, request: Any) -> Response:
        headers = dict(response.headers)

        if request.method.upper() == "GET" and response.status_code == 200:
            body = response.body or b""
            etag_value = hashlib.sha256(body).hexdigest()
            headers["ETag"] = f'"{etag_value}"'

            if request.headers.get("If-None-Match") == headers["ETag"]:
                return Response(status_code=304, headers=headers, media_type=response.media_type)

            response.headers["ETag"] = headers["ETag"]
            accept_encoding = (request.headers.get("accept-encoding") or "").lower()
            if "gzip" in accept_encoding and len(body) > 100:
                compressed = gzip.compress(body)
                if len(compressed) < len(body):
                    headers["Content-Encoding"] = "gzip"
                    headers["Vary"] = "Accept-Encoding"
                    response = Response(content=compressed, status_code=response.status_code, headers=headers, media_type=response.media_type)
                    COMPRESSION_USAGE.inc()
                    return response

        return response
