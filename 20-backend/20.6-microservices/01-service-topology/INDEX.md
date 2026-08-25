# Service Topology - Microservices

> **4 files.** How services find each other and evolve safely: discovery registries, the edge gateway, the sidecar service mesh, and the strangler-fig migration path off a monolith.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Service%20Topology-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Service Discovery](20.6.1.01-service-discovery.md) | Client vs server-side discovery, Consul, Eureka, DNS-based, registry HA, Kubernetes | 15 min |
| 02 | [API Gateway](20.6.1.02-api-gateway.md) | Routing, aggregation, auth, rate limiting at the edge; cross-cutting concerns and BFF | 15 min |
| 03 | [Service Mesh](20.6.1.03-service-mesh.md) | Istio, Linkerd, sidecar proxies, mTLS, retries, traffic shifting, observability without app changes | 10 min |
| 04 | [Strangler Fig](20.6.1.04-strangler-fig.md) | Legacy migration, facade/router design, parallel run, dual-write consistency, feature-flag cutover | 20 min |

---

[← Back to Microservices](../INDEX.md)
