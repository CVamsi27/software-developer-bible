---
section: Microservices
category: Architecture
tags: [concept]
---

# Service Mesh

## Definition

A **Service Mesh** is a dedicated infrastructure layer for handling service-to-service communication in microservices. It offloads traffic management, observability, and security from application code to a sidecar proxy (typically Envoy). **Istio** and **Linkerd** are the most popular implementations.

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

---

### See Also

- [API Gateway](../07-REST-API/09-API-Gateway.md)
- [Circuit Breaker](04-Circuit-Breaker.md)
- [Distributed Transactions](11-Distributed-Transactions.md)
- [gRPC](09-gRPC.md)
- [Interview Questions](08-Interview-Questions.md)

## References & Learn More

- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2.15/overview/)
- [Envoy Proxy](https://www.envoyproxy.io/)
