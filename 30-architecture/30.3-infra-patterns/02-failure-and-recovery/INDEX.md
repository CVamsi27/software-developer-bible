# Failure & Recovery

> **Study time:** ≈ 44 min of reading (7 files, ~6 min average).
> **7 files.** Surviving transient failure without side effects, containing blast radius on purpose, and recovering state when prevention fails: the resilience pattern landscape, retry discipline, idempotency keys, feature flags with kill switches, backup strategy proven by restore drills, and the complete idempotency-retry chain. The useful answer is a bounded failure and a recoverable outcome, supported by the chosen authority and capacity contracts.

[![Files](https://img.shields.io/badge/files-7-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Resilience-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Networks partition, dependencies time out, deploys hiccup. Naive code turns each blip into user-facing errors or duplicate side effects (double charges, double emails). The fix is layered: circuit breakers to stop cascading failure, retries with backoff and jitter to ride out transients, and idempotency keys so a retried operation is safe to repeat. When a bad release or dependency is already burning, feature flags and kill switches turn it off faster than any rollback; and when state itself is lost, verified backups plus rehearsed restore drills are the difference between an RTO met and a company that isn't.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Resilience Patterns — Overview](30.3.2.01-resilience-patterns.md) | Timeout, bulkhead, circuit-breaker landscape; deep-dive implementations live in [20.6-microservices](../../../20-backend/20.6-microservices/INDEX.md) | Important | Specialized | 6 min |
| 02 | [Retry Patterns](30.3.2.02-retry-patterns.md) | Exponential backoff, jitter, retry budgets, retry storms, when NOT to retry | Essential | Important | 8 min |
| 03 | [Idempotency Keys](30.3.2.03-idempotency-keys.md) | Stable operation identity, atomic local effects, retry replay, remote deduplication limits | Essential | Important | 7 min |
| 04 | [Feature Flags & Kill Switches](30.3.2.04-feature-flags-kill-switches.md) | Release and experiment flags, operational controls, trusted targeting, propagation and cleanup | Important | Specialized | 6 min |
| 05 | [Backup Strategy & Restore Drills](30.3.2.05-backup-strategy-restore-drills.md) | Full, incremental and differential backups; logical and physical formats; RPO/RTO; verified recovery and runbooks | Important | Specialized | 7 min |
| 06 | [Idempotency & Retry Deep Dive](30.3.2.06-idempotency-retry-deep-dive.md) | Cross-service failure trace: atomic API claim, outbox, inbox, receiver identity, retry budget and replay limits | Essential | Important | 7 min |

**Read order:** overview → retries → idempotency → flags/kill-switches → backups/drills → deep dive. Retries without idempotency are how you double-charge a customer; backups without restore drills are how you discover corruption mid-outage.

---

## Reading Path and Completion Check

Start with the resilience overview, then retries and idempotency. Add flags for controlled release and backups for data recovery; use the deep dive to connect the boundaries.

Trace one uncertain mutation and one full restore; explain the retry identity, durable evidence and bounded recovery time. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [Liveness & Lifecycle](../01-liveness-lifecycle/INDEX.md) — detecting failure before recovering from it
- [Microservices Resilience](../../../20-backend/20.6-microservices/04-resilience/INDEX.md) — circuit breaker and bulkhead deep-dives
- [System Design: Resilience Deep-Dive](../../30.2-system-design/01-theory/INDEX.md) — hedging, load shedding, coalescing
- [Data Retention & Archival](../05-shipping-and-evolution/30.3.5.04-data-retention-archival.md) — retention policy for the backup artifacts themselves

---

## Navigation

[← Liveness & Lifecycle](../01-liveness-lifecycle/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Coordination →](../03-coordination/INDEX.md)

---

## Docita Anchor

Candidate implementation locations in [Docita](https://github.com/CVamsi27/docita), the hospital-management SaaS. Read the checked-out revision and its tests before presenting a path as evidence of concurrency, cancellation, recovery or provider guarantees.

| Topic | Docita evidence |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Idempotency keys | Full module: `shared/modules/idempotency/*` (interceptor + service + repository + `@RequiresIdempotency` decorator); CI gate `check-job-idempotency.mjs` |
| Retries | `shared/common/interceptors/prisma-retry.interceptor.ts` |
| Circuit breaker | `shared/common/utils/circuit-breaker.registry.ts` + `circuit-breaker.ts` |
| DLQ & recovery | `apps/api/src/shared/modules/queue/dlq-replay.scheduler.ts` + `dlq.controller.ts` behind the Postgres queue |
| Incident playbooks | `docs/operations/playbooks/*`: razorpay-outage, db-connection-exhaustion, openai-rate-limit, pdf-queue-backlog, cloudflare-upstream-timeout |
