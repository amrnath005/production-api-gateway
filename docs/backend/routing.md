# Dynamic Proxy Routing & Header Handling

The proxy router ([app/routers/proxy.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/routers/proxy.py)) dynamically intercepts and proxies requests matching `/api/v1/{service}/{path:path}`.

---

## Service Registry Lookup
Microservices are registered in `SERVICE_REGISTRY` ([app/core/routes.py](file:///c:/Users/salte/OneDrive/Desktop/api-gateway-project/app/core/routes.py)):

```python
SERVICE_REGISTRY = {
    "users": [
        "http://user-service:8002",
    ],
    "orders": [
        "http://order-service:8003",
    ]
}
```

## Hop-by-Hop Header Sanitization
Before forwarding requests downstream, `GatewayService` strips connection-specific headers:

- `Host`
- `Connection`
- `Keep-Alive`
- `Proxy-Authenticate`
- `Proxy-Authorization`
- `TE`
- `Trailers`
- `Transfer-Encoding`
- `Upgrade`
- `Content-Length`
