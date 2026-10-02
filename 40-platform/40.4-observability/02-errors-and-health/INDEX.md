# Errors & Health

> **Study time:** ≈ 41 min of reading (3 files, ~14 min average).
> **3 files.** Runtime quality signals: aggregated error tracking (Sentry-style) and health checks that let orchestrators and load balancers trust your process.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Errors%20%26%20Health-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Pillars tell you what the system did; errors and health tell you whether what it did was correct and whether it can keep doing it. Error tracking groups thousands of stack traces into actionable issues tied to releases; health endpoints turn internal state into machine-readable signals that Kubernetes probes and load balancers act on. Together they close the loop between "it broke" and "something restarted it".

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Error Tracking](40.4.2.01-error-tracking.md) | Error aggregation (Sentry), source maps, grouping/dedup, release tracking, alerting on new issues | 20 min |
| 02 | [Health Checks](40.4.2.02-health-checks.md) | Liveness/readiness semantics, health endpoint design, dependency checks, graceful degradation | 19 min |

---

## Cross-References

- [The 3 Pillars](../01-pillars/INDEX.md) — logs and metrics feed error triage
- [Kubernetes Health Checks](../../../40-platform/40.2-kubernetes/04-production-hardening/INDEX.md) — probe configuration on the platform side
- [Infra: Health Checks & Graceful Shutdown](../../../30-architecture/30.3-infra-patterns/01-liveness-lifecycle/INDEX.md) — architecture-level contract

---

## Navigation

[← The 3 Pillars](../01-pillars/INDEX.md) · [↑ Observability Home](../INDEX.md) · [Next: SRE Targets →](../03-sre-targets/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — tracks errors and health for real.

| Topic | Docita evidence |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Error tracking (Sentry) | `instrument.ts` bootstrap with `createSentryBeforeSend` scrubbing (`error-handling/sentry.utils.ts`); optional profiling behind `SENTRY_PROFILING` |
| Error service layer | `monitoring/services/error-tracking.service.ts` wraps reporting for the app |
| Ops alerts | `ops-alert.service.ts` + `listeners/ops-alert.listener.ts` react to domain events |
| Health checks | `health-check.controller.ts`, `monitoring/health/prisma.health.ts`, `health-check.service.ts`; Fly probes `/api/health/live` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
