# Infra & Ops Patterns — Index

> **Study time:** ≈ 2 h 15 m of reading (22 files, ~6 min average).
> **22 files across 6 categories — operations-level patterns that sit *around* your services**: health checks and graceful shutdown, retries and idempotency, feature flags and kill switches, backups proven by restore drills, idempotency-retry deep dive, leader election, data-at-scale levers (including multi-tenant SaaS), zero-downtime deploys, technical debt management, cost engineering (FinOps), data retention/archival, and the interview bank that drills all of it.
>
> **Scope note:** the distributed-systems patterns (saga, circuit breaker deep-dives, bulkhead, API gateway, service discovery, strangler fig, event sourcing/CQRS, distributed transactions) live in [20.6-microservices](../../20-backend/20.6-microservices/INDEX.md) — this folder was deduplicated against it.

[![Files](https://img.shields.io/badge/files-22-blue)](../INDEX.md)
[![Categories](https://img.shields.io/badge/categories-6-green)](#categories)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Categories

| Category | Folder | Files | Why it matters |
| -------------------- | ---------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------------ |
| Liveness & Lifecycle | [01-liveness-lifecycle/](01-liveness-lifecycle/INDEX.md) | 1 | Health checks + graceful shutdown — the contract with your orchestrator |
| Failure & Recovery | [02-failure-and-recovery/](02-failure-and-recovery/INDEX.md) | 6 | Resilience overview, retry discipline, idempotency keys, feature flags & kill switches, backup strategy & restore drills |
| Coordination | [03-coordination/](03-coordination/INDEX.md) | 1 | Leader election & consensus — who runs the cron |
| Data at Scale | [04-data-at-scale/](04-data-at-scale/INDEX.md) | 4 | Database scaling, data pipelines, CDN architecture, multi-tenant SaaS |
| Shipping & Evolution | [05-shipping-and-evolution/](05-shipping-and-evolution/INDEX.md) | 4 | Zero-downtime deployments, technical debt strategy, cost engineering & FinOps, data retention & archival |
| Interview Prep | [06-interview-prep/](06-interview-prep/INDEX.md) | 1 | Senior-depth Q&A over the whole stack — contracts, drills, scaling levers, deploy safety |

---

## The Flow

```text
STAY ALIVE        SURVIVE FAILURE         SCALE DATA         SHIP SAFELY
01 health checks → 02 resilience      → 04 database      → 05 zero-downtime
   (graceful         02 retry patterns     scaling            deployments
    shutdown)        02 idempotency     04 data pipelines  05 technical debt
                      keys               04 CDN architecture 05 cost engineering
COORDINATE         02 feature flags                        05 data retention
03 leader election 02 backups & restore                    & archival
   & consensus        drills

RETRIEVE THEN DRILL
Each category REVISION follows its learning chapters
06 interview prep — the whole stack as Q&A
```

---

## File Index (reading order)

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Health Checks & Graceful Shutdown](01-liveness-lifecycle/30.3.1.01-health-checks-graceful-shutdown.md) | Liveness/readiness probes, SIGTERM draining, shutdown hooks | Essential | Important | 9 min |
| 02 | [Resilience Patterns — Overview](02-failure-and-recovery/30.3.2.01-resilience-patterns.md) | Timeout/bulkhead/circuit-breaker landscape; details in [20.6](../../20-backend/20.6-microservices/INDEX.md) | Important | Specialized | 6 min |
| 03 | [Retry Patterns](02-failure-and-recovery/30.3.2.02-retry-patterns.md) | Exponential backoff, jitter, retry budgets, retry storms | Essential | Important | 8 min |
| 04 | [Idempotency Keys](02-failure-and-recovery/30.3.2.03-idempotency-keys.md) | Stable operation identity, retry replay, and effect boundaries | Essential | Important | 7 min |
| 05 | [Feature Flags & Kill Switches](02-failure-and-recovery/30.3.2.04-feature-flags-kill-switches.md) | Flag types, targeting rules, kill-switch SLA, flag debt cleanup | Important | Specialized | 6 min |
| 06 | [Backup Strategy & Restore Drills](02-failure-and-recovery/30.3.2.05-backup-strategy-restore-drills.md) | Backup taxonomy, 3-2-1(-1-0), RPO/RTO math, restore game days, verification | Important | Specialized | 7 min |
| 07 | [Idempotency & Retry Deep Dive](02-failure-and-recovery/30.3.2.06-idempotency-retry-deep-dive.md) | Cross-authority commit, redelivery, ordering and replay boundaries | Essential | Important | 7 min |
| 08 | [Leader Election & Consensus](03-coordination/30.3.3.01-leader-election-consensus.md) | Fencing tokens, leases, cron coordination | Important | Specialized | 10 min |
| 09 | [Database Scaling](04-data-at-scale/30.3.4.01-database-scaling.md) | Read and write bottlenecks, partitioning, replication, pooling and query plans | Important | Specialized | 11 min |
| 10 | [Data Pipelines](04-data-at-scale/30.3.4.02-data-pipelines.md) | Checkpoints, replay, late events, backfills and data quality | Important | Specialized | 10 min |
| 11 | [CDN Architecture](04-data-at-scale/30.3.4.03-cdn-architecture.md) | Edge caching strategy (also: [40.10 CDN](../../40-platform/40.10-cdn/INDEX.md)) | Important | Specialized | 6 min |
| 12 | [Multi-Tenant SaaS Architecture](04-data-at-scale/30.3.4.04-multi-tenant-saas-architecture.md) | Verified request context, transaction-local RLS, caches/jobs and shared capacity | Important | Specialized | 6 min |
| 13 | [Zero-Downtime Deployments](05-shipping-and-evolution/30.3.5.01-zero-downtime-deployments.md) | Blue-green, canary, expand/contract migrations | Important | Specialized | 6 min |
| 14 | [Technical Debt](05-shipping-and-evolution/30.3.5.02-technical-debt.md) | Quadrants, remediation strategy | Important | Specialized | 6 min |
| 15 | [Cost Engineering & FinOps](05-shipping-and-evolution/30.3.5.03-cost-engineering-finops.md) | Rightsizing, spot strategy, unit economics, cost checks in CI | Important | Specialized | 6 min |
| 16 | [Data Retention & Archival](05-shipping-and-evolution/30.3.5.04-data-retention-archival.md) | Retention tiers, hot/warm/cold storage, legal hold, right-to-erasure | Important | Specialized | 7 min |
| 17 | [Infra & Ops Patterns Interview Questions](06-interview-prep/30.3.6.01-interview-questions.md) | Probe contracts, retry+idempotency, RPO/RTO & drills, fencing tokens, scaling levers, blue-green vs canary, scenario drills | Important | Specialized | 6 min |

---

## Category Completion

After each category, use its REVISION companion without reopening the chapters. Explain the guarantee, authority and one changed failure condition; then continue to the next category. The separate interview bank comes after all category retrieval checks.

## Where did the moved patterns go?

| Pattern (was here) | Now lives at | Role priority | General importance |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| Saga | [20.6 §Saga](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.01-saga-pattern.md) | Important | Important |
| Circuit breaker / resilience deep-dive | [20.6 §Circuit Breaker](../../20-backend/20.6-microservices/04-resilience/20.6.4.01-circuit-breaker.md) | Essential | Important |
| Bulkhead | [20.6 §Bulkhead](../../20-backend/20.6-microservices/04-resilience/20.6.4.02-bulkhead-pattern.md) | Important | Important |
| API gateway | [20.6 §API Gateway](../../20-backend/20.6-microservices/01-service-topology/20.6.1.02-api-gateway.md) | Important | Important |
| Service discovery | [20.6 §Service Discovery](../../20-backend/20.6-microservices/01-service-topology/20.6.1.01-service-discovery.md) | Important | Important |
| Strangler fig | [20.6 §Strangler Fig](../../20-backend/20.6-microservices/01-service-topology/20.6.1.04-strangler-fig.md) | Important | Important |
| Event sourcing / CQRS | [20.6 §Event Sourcing](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.03-event-sourcing.md) · [§CQRS](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.04-cqrs.md) | Important | Important |
| Distributed transactions | [20.6 §Distributed Transactions](../../20-backend/20.6-microservices/03-data-and-consistency/20.6.3.02-distributed-transactions.md) | Important | Important |

---

**Cross-references:** [Microservices stack](../../20-backend/20.6-microservices/INDEX.md) · [System design theory](../30.2-system-design/01-theory/INDEX.md) · [Platform stack](../../40-platform/INDEX.md)

---

## Navigation

[← Previous: System Design](../30.2-system-design/INDEX.md) · [ Back to Architecture Index](../INDEX.md)
