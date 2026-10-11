# Resilience - Microservices

> **Study time:** ≈ 14 min of reading (3 files, ~5 min average).
> **3 files.** Surviving partial failure: use a circuit breaker to limit new calls to a failing dependency and partition resources to bound what one workload can consume.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Resilience-blue)](../INDEX.md)

---

## Learning flow

First follow breaker admission through counted failures and a controlled recovery probe. Then separate resource occupancy from health decisions with a bulkhead, including queueing, actual task lifetime and fleet capacity. Use [revision](REVISION.md) before [interview practice](../05-interview-drills/20.6.5.01-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Circuit Breaker](20.6.4.01-circuit-breaker.md) | Closed/open/half-open states, threshold tuning, fallbacks, integration with retries/timeouts | Essential | Important | 6 min |
| 02 | [Bulkhead Pattern](20.6.4.02-bulkhead-pattern.md) | Thread pool/semaphore/connection partitioning, tenant isolation, pool sizing | Important | Important | 6 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) source paths illustrate local controls; inspect their actual state, cancellation and resource boundaries:

| Topic | Docita evidence |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Circuit breaker | `apps/api/src/shared/common/utils/circuit-breaker.ts` - CLOSED/OPEN/HALF_OPEN state machine with Prometheus metrics, shared via a registry |
| Request deadlines | `apps/api/src/shared/common/interceptors/timeout.interceptor.ts` - config-driven per-request timeout |
| Outbound timeouts | `apps/api/src/shared/common/http/fetch-with-timeout.ts` - abortable fetch wrapper for provider calls |
| Bulkhead by deployment | `apps/worker/src/main.ts` - separate worker process; shared host/database capacity still needs isolation evidence |

---

[← Previous: Data & Consistency](../03-data-and-consistency/INDEX.md) · [Next: Interview Drills →](../05-interview-drills/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
