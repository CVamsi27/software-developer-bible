# Measurement

> **Study time:** ≈ 43 min of reading (6 files, ~7 min average).
> **6 files.** How performance is actually measured: browser Performance APIs, profiling tools, Lighthouse CI in the pipeline, real-user monitoring from production — and how the underlying protocol (HTTP/2 vs HTTP/3) changes what you should optimize.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Lab vs field

Laboratory runs control a workload before release; field collection observes sampled real visits. Performance APIs work in both environments. Neither is automatically complete: a lab may omit a route state, while field collection may miss unsupported browsers or consent-restricted visits.

When a lab score looks good but users report delays, verify the affected journey, collection coverage and comparable device/network populations. Trace a representative slow case and test the cause; do not treat a score or an unexamined field aggregate as unquestionable truth.

---

## The 5 files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Performance APIs](50.3.2.01-performance-apis.md) | `performance` API, Navigation Timing, Resource Timing, PerformanceObserver | Important | Important | 8 min |
| 02 | [Profiling Tools](50.3.2.02-profiling-tools.md) | Chrome DevTools, Lighthouse, WebPageTest, React Profiler, flame charts | Important | Important | 8 min |
| 03 | [Lighthouse CI](50.3.2.03-lighthouse-ci.md) | Automated audits, budgets, score tracking, CI/CD integration | Important | Important | 6 min |
| 04 | [Real User Monitoring](50.3.2.04-real-user-monitoring.md) | RUM, `web-vitals` library, `sendBeacon`, CrUX, segmentation | Important | Important | 10 min |
| 05 | [HTTP/2 & HTTP/3 Performance Effects](50.3.2.05-http2-http3-performance-effects.md) | Multiplexing, TCP head-of-line blocking, QUIC, 0-RTT, connection migration, sharding anti-patterns, CWV impact | Important | Important | 8 min |

---

## Suggested flow

1. **Performance APIs** — match each question to browser-owned or application-owned timing
2. **Profiling Tools** — connect one visible delay to CPU, rendering or network work
3. **Lighthouse CI** — make a repeatable laboratory regression fail before release
4. **Real User Monitoring** — test whether the issue affects comparable production populations
5. **HTTP/2 & HTTP/3 Effects** — interpret protocol observations without mistaking capability for a measured win
6. **[Revision](REVISION.md)** — trace measurement boundaries and changed conditions before interview practice.

---

## Cross-References

- [Core Metrics](../01-core-metrics/INDEX.md) — what you are measuring.
- [Observability pillars](../../../40-platform/40.4-observability/INDEX.md) — the backend-side counterpart.

---

## Navigation

[← Core Metrics](../01-core-metrics/INDEX.md) · [↑ Performance Home](../INDEX.md) · [Next: Optimization & Governance →](../03-optimization-and-governance/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — inspect these reading pointers in the current checkout before claiming verified production behavior.

| Topic | Docita evidence |
| ------------------------------------- | -------------------------------------------------------------------- |
| Server-side measurement endpoint | `apps/api/src/shared/modules/performance/performance.controller.ts` |
| Slow-query telemetry | `apps/api/src/shared/modules/database/slow-query-logging.service.ts` |
| Query-cost guard at the data layer | `apps/api/src/shared/common/extensions/query-budget.extension.ts` |
| Lab baseline tooling | `scripts/perf/perf-baseline.mjs` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
