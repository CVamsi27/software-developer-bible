# Measurement

> **4 files.** How performance is actually measured: browser Performance APIs, profiling tools, Lighthouse CI in the pipeline, and real-user monitoring from production.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
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

## The 4 files

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Performance APIs](50.3.2.01-performance-apis.md) | `performance` API, Navigation Timing, Resource Timing, PerformanceObserver | 25 min |
| 02 | [Profiling Tools](50.3.2.02-profiling-tools.md) | Chrome DevTools, Lighthouse, WebPageTest, React Profiler, flame charts | 30 min |
| 03 | [Lighthouse CI](50.3.2.03-lighthouse-ci.md) | Automated audits, budgets, score tracking, CI/CD integration | 25 min |
| 04 | [Real User Monitoring](50.3.2.04-real-user-monitoring.md) | RUM, `web-vitals` library, `sendBeacon`, CrUX, segmentation | 25 min |

---

## Planned additions

- **50.3.2.05 — HTTP/2 & HTTP/3 Performance Effects** *(upcoming)*: multiplexing, head-of-line blocking, QUIC, and what they change for perf strategy. Slot reserved; not yet written.

---

## Suggested flow

1. **Performance APIs** — where the numbers come from
2. **Profiling Tools** — how to turn a slow trace into a root cause
3. **Lighthouse CI** — gate regressions before deploy
4. **RUM** — verify reality after deploy

---

## Cross-References

- [Core Metrics](../01-core-metrics/INDEX.md) — what you are measuring.
- [Observability pillars](../../../40-platform/40.4-observability/INDEX.md) — the backend-side counterpart.

---

## Navigation

[← Core Metrics](../01-core-metrics/INDEX.md) · [↑ Performance Home](../INDEX.md) · [Next: Optimization & Governance →](../03-optimization-and-governance/INDEX.md)
