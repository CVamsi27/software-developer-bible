# Failure & Recovery

> **Study time:** ≈ 1 h 16 m of reading (6 files, ~13 min average).
> **6 files.** Surviving transient failure without side effects, containing blast radius on purpose, and recovering state when prevention fails: the resilience pattern landscape, retry discipline, idempotency keys, feature flags with kill switches, backup strategy proven by restore drills, and the complete idempotency-retry chain. Distributed systems fail constantly; these patterns decide whether failure is an incident or a log line.

[![Files](https://img.shields.io/badge/files-6-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Resilience-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Networks partition, dependencies time out, deploys hiccup. Naive code turns each blip into user-facing errors or duplicate side effects (double charges, double emails). The fix is layered: circuit breakers to stop cascading failure, retries with backoff and jitter to ride out transients, and idempotency keys so a retried operation is safe to repeat. When a bad release or dependency is already burning, feature flags and kill switches turn it off faster than any rollback; and when state itself is lost, verified backups plus rehearsed restore drills are the difference between an RTO met and a company that isn't.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Resilience Patterns — Overview](30.3.2.01-resilience-patterns.md) | Timeout, bulkhead, circuit-breaker landscape; deep-dive implementations live in [20.6-microservices](../../../20-backend/20.6-microservices/INDEX.md) | 16 min |
| 02 | [Retry Patterns](30.3.2.02-retry-patterns.md) | Exponential backoff, jitter, retry budgets, retry storms, when NOT to retry | 11 min |
| 03 | [Idempotency Keys](30.3.2.03-idempotency-keys.md) | Exactly-once effects over at-least-once delivery, key design, dedupe windows, storage strategies | 12 min |
| 04 | [Feature Flags & Kill Switches](30.3.2.04-feature-flags-kill-switches.md) | Release/experiment/ops/permission flags, targeting rules, kill-switch SLA, flag debt cleanup, safe rollout recipe | 11 min |
| 05 | [Backup Strategy & Restore Drills](30.3.2.05-backup-strategy-restore-drills.md) | Full/incr/diff taxonomy, logical vs physical, 3-2-1(-1-0), RPO/RTO math, restore game days, automated verification, runbook template | 11 min |
| 06 | [Idempotency & Retry Deep Dive](30.3.2.06-idempotency-retry-deep-dive.md) | Complete reliability chain: API idempotency guard + outbox + consumer dedup + retry budgets + circuit breaker + DLQ | 15 min |

**Read order:** overview → retries → idempotency → flags/kill-switches → backups/drills → deep dive. Retries without idempotency are how you double-charge a customer; backups without restore drills are how you discover corruption mid-outage.

---

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

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — survives failure for real.

| Topic | Docita evidence |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Idempotency keys | Full module: `shared/modules/idempotency/*` (interceptor + service + repository + `@RequiresIdempotency` decorator); CI gate `check-job-idempotency.mjs` |
| Retries | `shared/common/interceptors/prisma-retry.interceptor.ts` |
| Circuit breaker | `shared/common/utils/circuit-breaker.registry.ts` + `circuit-breaker.ts` |
| DLQ & recovery | `queue/dlq-replay.scheduler.ts` + `dlq.controller.ts` behind the Postgres queue |
| Incident playbooks | `docs/operations/playbooks/*`: razorpay-outage, db-connection-exhaustion, openai-rate-limit, pdf-queue-backlog, cloudflare-upstream-timeout |
