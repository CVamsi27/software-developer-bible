# Measurement

> **Study time:** ≈ 1 h 4 m of reading (6 files, ~11 min average).
> **6 files.** How performance is actually measured: browser Performance APIs, profiling tools, Lighthouse CI in the pipeline, real-user monitoring from production — and how the underlying protocol (HTTP/2 vs HTTP/3) changes what you should optimize.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Lab vs field

The organizing idea of this category:

```text
LAB (synthetic)                    FIELD (real users)
performance-apis                   real-user-monitoring
profiling-tools                    CrUX data
lighthouse-ci                      sendBeacon beacons
"Reproducible, pre-deploy"         "Truth, post-deploy"
```

Senior interviews probe exactly this split: "Your lab Lighthouse score is 95 but users complain it's slow — what do you do?" (Answer: trust field data, segment by device/network, find the p75 outliers.)

---

## The 5 files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Performance APIs](50.3.2.01-performance-apis.md) | `performance` API, Navigation Timing, Resource Timing, PerformanceObserver | Important | Important | 8 min |
| 02 | [Profiling Tools](50.3.2.02-profiling-tools.md) | Chrome DevTools, Lighthouse, WebPageTest, React Profiler, flame charts | Important | Important | 19 min |
| 03 | [Lighthouse CI](50.3.2.03-lighthouse-ci.md) | Automated audits, budgets, score tracking, CI/CD integration | Important | Important | 9 min |
| 04 | [Real User Monitoring](50.3.2.04-real-user-monitoring.md) | RUM, `web-vitals` library, `sendBeacon`, CrUX, segmentation | Important | Important | 13 min |
| 05 | [HTTP/2 & HTTP/3 Performance Effects](50.3.2.05-http2-http3-performance-effects.md) | Multiplexing, TCP head-of-line blocking, QUIC, 0-RTT, connection migration, sharding anti-patterns, CWV impact | Important | Important | 13 min |

---

## Suggested flow

1. **Performance APIs** — where the numbers come from
2. **Profiling Tools** — how to turn a slow trace into a root cause
3. **Lighthouse CI** — gate regressions before deploy
4. **RUM** — verify reality after deploy
5. **HTTP/2 & HTTP/3 Effects** — interpret field data through the protocol lens

---

## Cross-References

- [Core Metrics](../01-core-metrics/INDEX.md) — what you are measuring.
- [Observability pillars](../../../40-platform/40.4-observability/INDEX.md) — the backend-side counterpart.

---

## Navigation

[← Core Metrics](../01-core-metrics/INDEX.md) · [↑ Performance Home](../INDEX.md) · [Next: Optimization & Governance →](../03-optimization-and-governance/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| ------------------------------------- | -------------------------------------------------------------------- |
| Server-side measurement endpoint | `apps/api/src/shared/modules/performance/performance.controller.ts` |
| Slow-query telemetry (RUM for the DB) | `apps/api/src/shared/modules/database/slow-query-logging.service.ts` |
| Query-cost guard at the data layer | `apps/api/src/shared/common/extensions/query-budget.extension.ts` |
| Lab baseline tooling | `scripts/perf/perf-baseline.mjs` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
