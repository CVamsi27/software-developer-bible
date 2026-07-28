# Service Mesh

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

e-to-service communication in microservices. It offloads traffic management, observability, and security from application code to a sidecar proxy (typically Envoy). **Istio** and **Linkerd** are the most popular implementations.

## Why Do We Need It?

1. **Traffic management**: Canary deployments, blue-green, circuit breaking, retries, timeouts
2. **Observability**: mTLS, distributed tracing, metrics (golden signals), access logs
3. **Security**: Automatic mTLS encryption, service identity, authorization policies
4. **Resilience**: Timeouts, retries, circuit breaking, fault injection for testing

## Core Components (Istio)

```text
┌─────────────────────────────────────────────────────────────┐
│                      SERVICE MESH (ISTIO)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Control Plane (istiod)                                      │
│  ├── Pilot: Service discovery, traffic config               │
│  ├── Citadel: Certificate management, mTLS                  │
│  └── Galley: Config validation                              │
│                                                              │
│  Data Plane (Envoy sidecars)                                 │
│  ├── Pod A: Service → Envoy proxy → mTLS →                 │
│  ├── Pod B: Envoy proxy → Service                          │
│  └── Metrics, tracing, logs sent to backend                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Summary

- Service mesh abstracts service-to-service communication into a dedicated infrastructure layer
- Sidecar proxies (Envoy) handle traffic management, observability, and security transparently
- Istio and Linkerd are the leading service mesh implementations for Kubernetes
- Provides mTLS encryption, circuit breaking, traffic splitting, and distributed tracing out of the box
- Operational overhead of sidecar injection and resource consumption are key trade-offs to evaluate

---

## Cheat Sheet
```text
SERVICE MESH CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  ┌─────────────────────────────────────────────────────────────┐
  │                      SERVICE MESH (ISTIO)                     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                              │
  │  Control Plane (istiod)                                      │
  │  ├── Pilot: Service discovery, traffic config               │
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [API Gateway](../07-REST-API/09-API-Gateway.md)
- [CQRS](13-CQRS.md)

## References & Learn More

- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2.15/overview/)
- [Envoy Proxy](https://www.envoyproxy.io/)
