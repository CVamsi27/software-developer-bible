# Failure & Recovery

> **3 files.** Surviving transient failure without side effects: the resilience pattern landscape, retry discipline, and idempotency keys. Distributed systems fail constantly; these patterns decide whether failure is an incident or a log line.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Resilience-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Networks partition, dependencies time out, deploys hiccup. Naive code turns each blip into user-facing errors or duplicate side effects (double charges, double emails). The fix is layered: circuit breakers to stop cascading failure, retries with backoff and jitter to ride out transients, and idempotency keys so a retried operation is safe to repeat.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Resilience Patterns — Overview](30.3.2.01-resilience-patterns.md) | Timeout, bulkhead, circuit-breaker landscape; deep-dive implementations live in [20.6-microservices](../../../20-backend/20.6-microservices/INDEX.md) | 25 min |
| 02 | [Retry Patterns](30.3.2.02-retry-patterns.md) | Exponential backoff, jitter, retry budgets, retry storms, when NOT to retry | 25 min |
| 03 | [Idempotency Keys](30.3.2.03-idempotency-keys.md) | Exactly-once effects over at-least-once delivery, key design, dedupe windows, storage strategies | 20 min |

**Read order:** overview → retries → idempotency. Retries without idempotency are how you double-charge a customer.

---

## Cross-References

- [Liveness & Lifecycle](../01-liveness-lifecycle/INDEX.md) — detecting failure before recovering from it
- [Microservices Resilience](../../../20-backend/20.6-microservices/04-resilience/INDEX.md) — circuit breaker and bulkhead deep-dives
- [System Design: Resilience Deep-Dive](../../30.2-system-design/01-theory/INDEX.md) — hedging, load shedding, coalescing

---

## Navigation

[← Liveness & Lifecycle](../01-liveness-lifecycle/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Coordination →](../03-coordination/INDEX.md)
