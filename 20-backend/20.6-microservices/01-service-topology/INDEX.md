# Service Topology - Microservices

> **Study time:** ≈ 22 min of reading (5 files, ~4 min average).
> **5 files.** How services find each other and evolve safely: discovery registries, the edge gateway, managed service-hop policy, and the strangler-fig migration path off a monolith.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Service%20Topology-blue)](../INDEX.md)

---

## Learning flow

First resolve changing endpoints, then separate external routing from downstream authority. Read the mesh to understand managed service-hop policy, and finally use those boundaries for incremental migration. Follow the chapters with [revision](REVISION.md) and then the [interview bank](../05-interview-drills/20.6.5.01-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Service Discovery](20.6.1.01-service-discovery.md) | Client vs server-side discovery, Consul, Eureka, DNS-based, registry HA, Kubernetes | Important | Important | 5 min |
| 02 | [API Gateway](20.6.1.02-api-gateway.md) | Routing, aggregation, auth, rate limiting at the edge; cross-cutting concerns and BFF | Important | Important | 5 min |
| 03 | [Service Mesh](20.6.1.03-service-mesh.md) | Istio, Linkerd, sidecar proxies, mTLS, retries, traffic shifting, observability without app changes | Important | Important | 4 min |
| 04 | [Strangler Fig](20.6.1.04-strangler-fig.md) | Legacy migration, facade/router design, parallel run, dual-write consistency, feature-flag cutover | Important | Important | 6 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) source paths illustrate a modular monolith; inspect current source rather than treating a study pattern as deployed evidence:

Docita is a **modular monolith**: one API deployable plus one worker deployable — no discovery registry, mesh, or gateway product.

| Topic | Docita evidence |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Modular monolith topology | `apps/api/src/app.module.ts` - ~20 bounded-context modules in a single deployable |
| Worker as separate deployable | `apps/worker/src/main.ts` - own Fly.io process (`apps/worker/fly.toml`) for crons and jobs |
| Incremental cutover lever | `apps/api/src/shared/modules/feature-flags/feature-flags.service.ts` - per-clinic flags enable strangler-style rollout |

Consul/Eureka, Istio/Linkerd, and API-gateway products not used; adding another deployable does not require those products. Choose discovery/routing and communication policy from actual requirements and operational capacity.
---

[Next: Communication & Messaging →](../02-communication-and-messaging/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
