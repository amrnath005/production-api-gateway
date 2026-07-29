# Jaeger Distributed Tracing Guide

## Tracing Architecture
Jaeger acts as the OTLP collector endpoint at `http://jaeger:14268/api/traces`.

## Viewing Spans
Navigate to `http://localhost:16686`, select service `api-gateway`, and click **Find Traces** to view full span hierarchy.
