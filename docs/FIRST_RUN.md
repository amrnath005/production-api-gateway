# Beginner's First Run Guide

Welcome to the **API Gateway Local Development Platform**. This guide takes you step-by-step through setting up, testing, and exploring the platform after running Docker Compose.

---

## Step 1: Start the Entire Stack

Open your terminal in the repository root directory and run:

```bash
docker compose up -d
```

Wait ~30–60 seconds for all containers to initialize and complete health checks.

To verify that all containers are healthy:
```bash
docker compose ps
```
You should see all services in an `Up` or `healthy` state.

---

## Step 2: Test the API Gateway (Open First)

### 1. Gateway Health Check
Open your web browser or run `curl`:
- **URL**: `http://localhost:8000/api/v1/health`
- **Expected Response**: `{"status": "healthy"}`

### 2. Swagger OpenAPI Documentation
- **URL**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **What it does**: Provides an interactive UI to test all Gateway routes.
- **How to test authentication**:
  1. Expand `POST /login`.
  2. Click **Try it out**.
  3. Enter Request body:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
  4. Click **Execute**. Copy the returned `access_token`.
  5. Click the **Authorize** button at the top right, paste the token, and click **Authorize**.
  6. Now try calling `GET /profile`!

---

## Step 3: Explore Monitoring & Observability Dashboards

### 1. Grafana Monitoring Dashboards
- **URL**: [http://localhost:3000](http://localhost:3000)
- **Login Credentials**: Auto-logs in automatically! (Or username: `admin`, password: `admin`).
- **What to explore**:
  - Click **Dashboards** in the left sidebar.
  - Open **Gateway Overview** to view real-time HTTP requests per second, p95 response latencies, and error rates.
  - Open **Redis Cache** to monitor hit/miss ratios.
  - Open **Circuit Breaker** to view circuit status and trips.

### 2. Distributed Tracing in Jaeger
- **URL**: [http://localhost:16686](http://localhost:16686)
- **No Login Required**.
- **What it does**: Visualizes trace spans for every request processed by the Gateway.
- **How to verify**:
  1. Select `api-gateway` under **Service**.
  2. Click **Find Traces**.
  3. Click any trace to view the exact lifecycle timing across Auth, Rate Limiter, Cache, and Microservices.

### 3. Prometheus Raw Metrics
- **URL**: [http://localhost:9090](http://localhost:9090)
- **What it does**: Scrapes raw metrics from `/api/v1/metrics`. Try querying `gateway_requests_total` in the Expression bar!

---

## Step 4: Inspect Database & Caching Tools

### 1. Database Management in pgAdmin
- **URL**: [http://localhost:5050](http://localhost:5050)
- **Login Credentials**: `admin@admin.com` / `admin`
- **Auto-Connected Server**: Click **Servers** in the left navigation tree. `API Gateway Postgres` is pre-configured and auto-connected!
- **How to view tables**: Expand `Servers` -> `API Gateway Postgres` -> `Databases` -> `api_gateway` -> `Schemas` -> `public` -> `Tables`. Right-click `users` and select **View/Edit Data**.

### 2. Cache Inspection in RedisInsight
- **URL**: [http://localhost:5540](http://localhost:5540)
- **No Login Required**.
- **Auto-Connected Redis**: `API Gateway Redis` is pre-added!
- **What to explore**: Click on the database connection to view live keys (e.g. `rate_limit:*`, `cache:*`), inspect TTL timers, and execute Redis commands.

---

## Verification Summary Checklist

| Action | URL | Expected Result | Verified? |
| :--- | :--- | :--- | :---: |
| Open Gateway Health | `http://localhost:8000/api/v1/health` | Returns `{"status":"healthy"}` | PASS |
| Test Login in Swagger | `http://localhost:8000/docs` | Returns Bearer access token | PASS |
| View Grafana Dashboards | `http://localhost:3000` | Auto-loads 10 pre-configured dashboards | PASS |
| Check Traces in Jaeger | `http://localhost:16686` | Displays visual trace waterfalls | PASS |
| Browse Tables in pgAdmin | `http://localhost:5050` | `API Gateway Postgres` auto-connected | PASS |
| Inspect Keys in RedisInsight | `http://localhost:5540` | `API Gateway Redis` auto-connected | PASS |
