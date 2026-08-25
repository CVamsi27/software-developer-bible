# Infra & Ops Patterns — Index

> **10 files — operations-level patterns that sit *around* your services**: retries, idempotency, health checks, graceful shutdown, leader election, zero-downtime deploys, data pipelines, technical debt management.
>
> **Scope note:** the distributed-systems patterns (saga, circuit breaker, bulkhead, API gateway, service discovery, strangler fig, event sourcing/CQRS, distributed transactions) live in [20.6-microservices](../../20-backend/20.6-microservices/INDEX.md) — this folder was deduplicated against it.

[![Files](https://img.shields.io/badge/files-10-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 10 files classify into 5 conceptual categories — the "GoF classification" of infra/ops patterns.

| Category | Files | Why it matters |
|----------|------:|----------------|
| **Liveness & Lifecycle** | 1 | Health checks + graceful shutdown — the contract between your app and the orchestrator |
| **Failure Recovery** | 2 | Retry patterns, idempotency keys — surviving transient failure without side effects |
| **Coordination** | 1 | Leader election & consensus — who runs the cron, fencing tokens |
| **Shipping & Evolution** | 2 | Zero-downtime deployments, technical debt management — change without breakage |
| **Data at Scale** | 4 | Database scaling, data pipelines, CDN architecture, resilience overview |

---

## The Flow

```text
KEEP ALIVE RECOVER SHIP SAFELY RUN CLEAN
03 health checks → 02 resilience → 05 zero-downtime → 06 data pipelines
   (graceful shutdown) overview + deployments 04 technical debt
                        pointers 01 database scaling
RETRY & DEDUPE COORDINATE 07 CDN architecture
14 idempotency keys 13 retry patterns 16 leader election &
                                             consensus
```

| # | File | Topics |
|---|------|--------|
| 01 | [Database Scaling](04-data-at-scale/30.3.4.01-database-scaling.md) | Read replicas, partitioning, scaling levers |
| 02 | [Resilience Patterns — Overview](02-failure-and-recovery/30.3.2.01-resilience-patterns.md) | Timeout/bulkhead/circuit-breaker landscape; details in [20.6](../../20-backend/20.6-microservices/INDEX.md) |
| 03 | [Leader Election & Consensus](03-coordination/30.3.3.01-leader-election-consensus.md) | Fencing tokens, leases, cron coordination |
| 04 | [Technical Debt](05-shipping-and-evolution/30.3.5.02-technical-debt.md) | Quadrants, remediation strategy |
| 05 | [Zero-Downtime Deployments](05-shipping-and-evolution/30.3.5.01-zero-downtime-deployments.md) | Blue-green, canary, expand/contract migrations |
| 06 | [Data Pipelines](04-data-at-scale/30.3.4.02-data-pipelines.md) | ETL vs streaming, Bronze/Silver/Gold framing |
| 07 | [CDN Architecture](04-data-at-scale/30.3.4.03-cdn-architecture.md) | Edge caching strategy (also: [40.10 CDN](../../40-platform/40.10-cdn/INDEX.md)) |
| 08 | [Health Checks & Graceful Shutdown](01-liveness-lifecycle/30.3.1.01-health-checks-graceful-shutdown.md) | Liveness/readiness, SIGTERM draining |
| 09 | [Retry Patterns](02-failure-and-recovery/30.3.2.02-retry-patterns.md) | Exponential backoff, jitter, retry budgets |
| 10 | [Idempotency Keys](02-failure-and-recovery/30.3.2.03-idempotency-keys.md) | Exactly-once effects over at-least-once delivery |

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

**Cross-references:** [Microservices stack](../../20-backend/20.6-microservices/INDEX.md) · [System design theory](../30.2-system-design/01-theory/INDEX.md)

---

## Navigation

[← Previous: System Design](../30.2-system-design/INDEX.md) · [ Back to Index](../INDEX.md)
