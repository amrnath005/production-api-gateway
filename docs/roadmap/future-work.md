# Future Work & System Roadmap

This document outlines planned enhancements for future platform releases:

---

## Planned Architecture Enhancements

1. **Kubernetes Metrics-Based HPA**: Configure HPA scaling triggers based on Prometheus custom metrics (`gateway_requests_total` rate) using Kube-Prometheus-Stack.
2. **Event-Driven Async Event Bus**: Integrate Apache Kafka / RabbitMQ for asynchronous event publishing and background job dispatching.
3. **Service Mesh Integration (Istio)**: Offload mTLS authentication and canary traffic splitting to an Istio sidecar proxy layer.
4. **OAuth2 / OIDC Single Sign-On**: Expand `/login` to support OAuth2 authorization code flow and OpenID Connect (OIDC) identity providers.
