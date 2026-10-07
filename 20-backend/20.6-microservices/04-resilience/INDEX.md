# Resilience - Microservices

> **Study time:** ≈ 46 min of reading (3 files, ~15 min average).
> **3 files.** Surviving partial failure: the circuit-breaker state machine that short-circuits failing dependencies, and bulkhead resource partitioning so one failure cannot exhaust everything.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Resilience-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Circuit Breaker](20.6.4.01-circuit-breaker.md) | Closed/open/half-open states, threshold tuning, fallbacks, integration with retries/timeouts | Essential | Important | 24 min |
| 02 | [Bulkhead Pattern](20.6.4.02-bulkhead-pattern.md) | Thread pool/semaphore/connection partitioning, tenant isolation, pool sizing | Important | Important | 20 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Circuit breaker | `apps/api/src/shared/common/utils/circuit-breaker.ts` - CLOSED/OPEN/HALF_OPEN state machine with Prometheus metrics, shared via a registry |
| Request deadlines | `apps/api/src/shared/common/interceptors/timeout.interceptor.ts` - config-driven per-request timeout |
| Outbound timeouts | `apps/api/src/shared/common/http/fetch-with-timeout.ts` - abortable fetch wrapper for provider calls |
| Bulkhead by deployment | `apps/worker/src/main.ts` - job load isolated in its own process so spikes cannot starve the API |

---

[← Previous: Data & Consistency](../03-data-and-consistency/INDEX.md) · [Next: Interview Drills →](../05-interview-drills/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
