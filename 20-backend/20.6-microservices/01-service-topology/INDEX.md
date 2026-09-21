# Service Topology - Microservices

> **Study time:** ≈ 1 h 6 m of reading (4 files, ~16 min average).
> **4 files.** How services find each other and evolve safely: discovery registries, the edge gateway, the sidecar service mesh, and the strangler-fig migration path off a monolith.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Service%20Topology-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Service Discovery](20.6.1.01-service-discovery.md) | Client vs server-side discovery, Consul, Eureka, DNS-based, registry HA, Kubernetes | 14 min |
| 02 | [API Gateway](20.6.1.02-api-gateway.md) | Routing, aggregation, auth, rate limiting at the edge; cross-cutting concerns and BFF | 21 min |
| 03 | [Service Mesh](20.6.1.03-service-mesh.md) | Istio, Linkerd, sidecar proxies, mTLS, retries, traffic shifting, observability without app changes | 7 min |
| 04 | [Strangler Fig](20.6.1.04-strangler-fig.md) | Legacy migration, facade/router design, parallel run, dual-write consistency, feature-flag cutover | 24 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

Docita is a **modular monolith**: one API deployable plus one worker deployable — no discovery registry, mesh, or gateway product.

| Topic | Docita evidence |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Modular monolith topology | `apps/api/src/app.module.ts` - ~20 bounded-context modules in a single deployable |
| Worker as separate deployable | `apps/worker/src/main.ts` - own Fly.io process (`apps/worker/fly.toml`) for crons and jobs |
| Incremental cutover lever | `apps/api/src/shared/modules/feature-flags/feature-flags.service.ts` - per-clinic flags enable strangler-style rollout |

Consul/Eureka, Istio/Linkerd, and API-gateway products not used; they would arrive with the second independently deployed service — DNS plus a gateway first, a mesh only when mTLS/traffic-shifting pain is real.
---

[Next: Communication & Messaging →](../02-communication-and-messaging/INDEX.md)
