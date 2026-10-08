# Advanced Testing

> **Study time:** ≈ 22 min of reading (3 files, ~7 min average).
> **3 files.** Testing beyond correctness: performance/load testing (k6, Artillery, Locust) and chaos engineering — measuring behavior under stated load and failure conditions.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Pass 1 — Relate incoming work to capacity

Read [Performance & Load Testing](50.1.5.01-performance-load-testing.md). Start with the operation and workload, distinguish closed users from independent arrivals, then trace the local catalog test from request to business check to exit status. Practice identifying generator limits and the service bottleneck before making a capacity claim.

## Pass 2 — Change one failure condition

Read [Chaos Engineering & Game Days](50.1.5.02-chaos-engineering.md). Define the hypothesis and fault boundary, run the local downstream-delay fixture and explain what it establishes. Add an application contract before claiming deadline, retry or circuit-breaker resilience.

## Revision, then operational practice

Complete [REVISION](REVISION.md) with the chapters closed. Return to a source example when you cannot trace its denominator, fault or decision boundary. For production permission, response roles and recovery ownership, continue with [operational chaos engineering](../../50.4-production-engineering/50.4.03-chaos-engineering.md).

## Related learning

- [Production Engineering](../../50.4-production-engineering/INDEX.md) — reliability targets, readiness and response capacity
- [Observability](../../../40-platform/40.4-observability/INDEX.md) — instruments and measurement coverage

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) provides companion artifacts. Performance-budget scripts check selected limits; they are not proof of a load-tested production capacity or a deployed chaos program. Verify the artifact and result before citing it as your experience.

| Topic | Docita evidence |
| ---------------------------- | ----------------------------------------------------------------------- |
| Performance budgets as gates | `scripts/perf/check-perf-budget.mjs` + `scripts/perf/perf-baseline.mjs` |
| Web Vitals field checks | `scripts/perf/check-web-vitals.mjs` + `check-web-vitals-budget.mjs` |
| Route-level budgets | `scripts/perf/route-budgets.config.mjs` + `check-route-budgets.mjs` |
| Chaos engineering | _No direct docita implementation yet._ |

## Navigation

[← Mocking & Patterns](../04-mocking-and-patterns/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Interview Prep →](../06-interview-prep/INDEX.md)
