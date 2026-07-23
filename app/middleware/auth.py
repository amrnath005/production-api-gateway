from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.security import verify_token

PUBLIC_PATHS = {
    "/",
    "/health",
    "/version",
    "/ping",
    "/login",
    "/docs",
    "/openapi.json",
    "/redoc",
}


async def authenticate(request: Request, call_next):

    # Skip authentication for public routes
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    # Read Authorization header
    auth_header = request.headers.get("Authorization")

    # Header is missing
    if auth_header is None:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing"},
        )

    # Header must start with "Bearer "
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid Authorization header"},
        )

    # Extract token
    token = auth_header.split(" ", 1)[1]

    try:
        # Verify JWT
        payload = verify_token(token)

        # Store decoded user information
        request.state.user = payload

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or expired token"},
        )

    # Continue to the next middleware or route
    response = await call_next(request)

    return response