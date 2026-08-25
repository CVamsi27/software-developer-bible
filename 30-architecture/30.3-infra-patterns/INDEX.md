# Infra & Ops Patterns — Index

> **10 files across 5 categories — operations-level patterns that sit *around* your services**: health checks and graceful shutdown, retries and idempotency, leader election, data-at-scale levers, zero-downtime deploys, and technical debt management.
>
> **Scope note:** the distributed-systems patterns (saga, circuit breaker deep-dives, bulkhead, API gateway, service discovery, strangler fig, event sourcing/CQRS, distributed transactions) live in [20.6-microservices](../../20-backend/20.6-microservices/INDEX.md) — this folder was deduplicated against it.

[![Files](https://img.shields.io/badge/files-10-blue)](../INDEX.md)
[![Categories](https://img.shields.io/badge/categories-5-green)](#categories)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Categories

| Category | Folder | Files | Why it matters |
|----------|--------|------:|----------------|
| Liveness & Lifecycle | [01-liveness-lifecycle/](01-liveness-lifecycle/INDEX.md) | 1 | Health checks + graceful shutdown — the contract with your orchestrator |
| Failure & Recovery | [02-failure-and-recovery/](02-failure-and-recovery/INDEX.md) | 3 | Resilience overview, retry discipline, idempotency keys |
| Coordination | [03-coordination/](03-coordination/INDEX.md) | 1 | Leader election & consensus — who runs the cron |
| Data at Scale | [04-data-at-scale/](04-data-at-scale/INDEX.md) | 3 | Database scaling, data pipelines, CDN architecture |
| Shipping & Evolution | [05-shipping-and-evolution/](05-shipping-and-evolution/INDEX.md) | 2 | Zero-downtime deployments, technical debt strategy |

---

## The Flow

```text
STAY ALIVE        SURVIVE FAILURE       SCALE DATA         SHIP SAFELY
01 health checks → 02 resilience      → 04 database      → 05 zero-downtime
   (graceful         02 retry patterns     scaling            deployments
    shutdown)        02 idempotency     04 data pipelines  05 technical debt
                     keys               04 CDN architecture
COORDINATE
03 leader election & consensus
```

---

## File Index (reading order)

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Health Checks & Graceful Shutdown](01-liveness-lifecycle/30.3.1.01-health-checks-graceful-shutdown.md) | Liveness/readiness probes, SIGTERM draining, shutdown hooks | 25 min |
| 02 | [Resilience Patterns — Overview](02-failure-and-recovery/30.3.2.01-resilience-patterns.md) | Timeout/bulkhead/circuit-breaker landscape; details in [20.6](../../20-backend/20.6-microservices/INDEX.md) | 25 min |
| 03 | [Retry Patterns](02-failure-and-recovery/30.3.2.02-retry-patterns.md) | Exponential backoff, jitter, retry budgets, retry storms | 25 min |
| 04 | [Idempotency Keys](02-failure-and-recovery/30.3.2.03-idempotency-keys.md) | Exactly-once effects over at-least-once delivery | 20 min |
| 05 | [Leader Election & Consensus](03-coordination/30.3.3.01-leader-election-consensus.md) | Fencing tokens, leases, cron coordination | 30 min |
| 06 | [Database Scaling](04-data-at-scale/30.3.4.01-database-scaling.md) | Read replicas, partitioning, scaling levers in order | 35 min |
| 07 | [Data Pipelines](04-data-at-scale/30.3.4.02-data-pipelines.md) | ETL vs streaming, Bronze/Silver/Gold framing | 30 min |
| 08 | [CDN Architecture](04-data-at-scale/30.3.4.03-cdn-architecture.md) | Edge caching strategy (also: [40.10 CDN](../../40-platform/40.10-cdn/INDEX.md)) | 30 min |
| 09 | [Zero-Downtime Deployments](05-shipping-and-evolution/30.3.5.01-zero-downtime-deployments.md) | Blue-green, canary, expand/contract migrations | 30 min |
| 10 | [Technical Debt](05-shipping-and-evolution/30.3.5.02-technical-debt.md) | Quadrants, remediation strategy | 20 min |

---

## Where did the moved patterns go?

| Pattern (was here) | Now lives at |
|--------------------|--------------|
| Saga | [20.6 §Saga](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.01-saga-pattern.md) |
| Circuit breaker / resilience deep-dive | [20.6 §Circuit Breaker](../../20-backend/20.6-microservices/04-resilience/20.6.4.01-circuit-breaker.md) |
| Bulkhead | [20.6 §Bulkhead](../../20-backend/20.6-microservices/04-resilience/20.6.4.02-bulkhead-pattern.md) |
| API gateway | [20.6 §API Gateway](../../20-backend/20.6-microservices/01-service-topology/20.6.1.02-api-gateway.md) |
| Service discovery | [20.6 §Service Discovery](../../20-backend/20.6-microservices/01-service-topology/20.6.1.01-service-discovery.md) |
| Strangler fig | [20.6 §Strangler Fig](../../20-backend/20.6-microservices/01-service-topology/20.6.1.04-strangler-fig.md) |
| Event sourcing / CQRS | [20.6 §Event Sourcing](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.03-event-sourcing.md) · [§CQRS](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.04-cqrs.md) |
| Distributed transactions | [20.6 §Distributed Transactions](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.02-distributed-transactions.md) |

---

**Cross-references:** [Microservices stack](../../20-backend/20.6-microservices/INDEX.md) · [System design theory](../30.2-system-design/01-theory/INDEX.md) · [Platform stack](../../40-platform/INDEX.md)

---

## Navigation

[← Previous: System Design](../30.2-system-design/INDEX.md) · [ Back to Architecture Index](../INDEX.md)
