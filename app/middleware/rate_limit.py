import time

from fastapi import HTTPException, Request

from app.core.settings import settings

clients = {}


async def rate_limit(request: Request, call_next):

    client_ip = request.client.host

    current_time = time.time()

    if client_ip not in clients:

        clients[client_ip] = {
            "count": 1,
            "start": current_time
        }

    else:

        elapsed = current_time - clients[client_ip]["start"]

        if elapsed > settings.RATE_LIMIT_WINDOW:

            clients[client_ip] = {
                "count": 1,
                "start": current_time
            }

        else:

            clients[client_ip]["count"] += 1

            if clients[client_ip]["count"] > settings.RATE_LIMIT:

                raise HTTPException(
                    status_code=429,
                    detail="Too Many Requests"
                )

    response = await call_next(request)

    return response