from fastapi import APIRouter, HTTPException, Request, Response
import httpx

from app.core.exceptions import GatewayException
from app.core.observability import build_correlation_headers
from app.core.routes import SERVICE_REGISTRY
from app.services.gateway import gateway_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Proxy"]
)


@router.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
@router.api_route(
    "/{service}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def proxy(
    service: str,
    request: Request,
    path: str = ""
):

    if service not in SERVICE_REGISTRY:

        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    headers = dict(request.headers)
    correlation_headers = build_correlation_headers(
        request_id=getattr(request.state, "request_id", "gateway-req"),
        correlation_id=request.headers.get("X-Correlation-ID") or getattr(request.state, "request_id", "gateway-req"),
    )
    headers.update(correlation_headers)

    params = dict(request.query_params)

    body = None

    if request.method in ["POST", "PUT", "PATCH"]:

        body = await request.body()

    try:

        response = await gateway_service.forward_request(
            service=service,
            method=request.method,
            path=path,
            headers=headers,
            params=params,
            body=body
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get(
                "content-type",
                "application/json"
            )
        )

    except GatewayException as e:

        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )

    except (httpx.ConnectError, httpx.NetworkError):

        raise HTTPException(
            status_code=502,
            detail="Backend Service Unavailable"
        )

    except httpx.TimeoutException:

        raise HTTPException(
            status_code=504,
            detail="Backend Service Timeout"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Internal Gateway Error: {str(e)}"
        )