# Performance Monitoring — Index

> **9 files across 4 categories.** Web performance monitoring from Core Web Vitals, performance APIs, profiling tools, Lighthouse CI, bundle analysis, real-user monitoring, HTTP/2 & HTTP/3 protocol effects, and performance budgets to interview questions.

[![Files](https://img.shields.io/badge/files-9-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why performance monitoring:** Core Web Vitals affect SEO, conversion, and user satisfaction. Senior frontend interviews test LCP/INP/CLS, profiling workflow, and performance budgets. Slow sites lose users — every 100ms costs ~1% of revenue.

---

## The 4 Categories (in study order)

| Category                                                                  | Files | Purpose                                                                        |
| ------------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------ |
| [01 — Core Metrics](01-core-metrics/INDEX.md)                             | 1     | LCP, INP, CLS — the three pillars and their thresholds                         |
| [02 — Measurement](02-measurement/INDEX.md)                               | 5     | Performance APIs, profiling tools, Lighthouse CI, RUM, HTTP/2 & HTTP/3 effects |
| [03 — Optimization & Governance](03-optimization-and-governance/INDEX.md) | 2     | Bundle analysis, performance budgets                                           |
| [04 — Interview Prep](04-interview-prep/INDEX.md)                         | 1     | 25+ Qs                                                                         |

---

## Core Metrics

The 3 Core Web Vitals — every senior frontend interview starts here.

| #   | File                                                            | Topics                                                                                      | Read time   |
| --: | ------                                                          | --------                                                                                    | ----------: |
| 01  | [Core Web Vitals](01-core-metrics/50.3.1.01-core-web-vitals.md) | LCP, INP, CLS — measurement, thresholds, optimization strategies. INP replaced FID in 2024. | 30 min      |

**The 3 metrics (memorize thresholds):**
- **LCP** (Largest Contentful Paint) — should be **≤ 2.5s**
- **INP** (Interaction to Next Paint) — should be **≤ 200ms**
- **CLS** (Cumulative Layout Shift) — should be **≤ 0.1**

---

## Measurement

Lab vs field: APIs, profilers, and Lighthouse are synthetic; RUM is truth from production.

| #   | File                                                                                               | Topics                                                                                             | Read time   |
| --: | ------                                                                                             | --------                                                                                           | ----------: |
| 01  | [Performance APIs](02-measurement/50.3.2.01-performance-apis.md)                                   | `performance` API, Navigation Timing, Resource Timing, observers (PerformanceObserver)             | 25 min      |
| 02  | [Profiling Tools](02-measurement/50.3.2.02-profiling-tools.md)                                     | Chrome DevTools, Lighthouse, WebPageTest, React Profiler, flame charts                             | 30 min      |
| 03  | [Lighthouse CI](02-measurement/50.3.2.03-lighthouse-ci.md)                                         | Automated audits, budgets, score tracking, CI/CD integration                                       | 25 min      |
| 04  | [Real User Monitoring](02-measurement/50.3.2.04-real-user-monitoring.md)                           | RUM, `web-vitals` library, `sendBeacon`, CrUX (Chrome User Experience Report), segmentation        | 25 min      |
| 05  | [HTTP/2 & HTTP/3 Performance Effects](02-measurement/50.3.2.05-http2-http3-performance-effects.md) | Multiplexing, TCP head-of-line blocking, QUIC, 0-RTT, connection migration, protocol-segmented RUM | 30 min      |

---

## Optimization & Governance

| #   | File                                                                                   | Topics                                                                       | Read time   |
| --: | ------                                                                                 | --------                                                                     | ----------: |
| 01  | [Bundle Analysis](03-optimization-and-governance/50.3.3.01-bundle-analysis.md)         | Bundle size, tree shaking, code splitting, bundlephobia, source-map-explorer | 25 min      |
| 02  | [Performance Budgets](03-optimization-and-governance/50.3.3.02-performance-budgets.md) | `size-limit`, per-chunk budgets, CI enforcement, budgeting tiers             | 20 min      |

---

## Interview Prep

| #   | File                                                                      | Contents                           | Time    |
| --: | ------                                                                    | ----------                         | ------  |
| 01  | [Interview Questions](04-interview-prep/50.3.4.01-interview-questions.md) | 25+ curated questions with answers | 1-2 hrs |

---

## Suggested Study Order

1. **Core Web Vitals** — must know (every frontend interview)
2. **Performance APIs + Profiling Tools** — must know
3. **Bundle Analysis** — for build pipeline discussions
4. **Lighthouse CI + RUM** — for production monitoring
5. **Performance Budgets** — for engineering culture discussions
6. **Interview Questions** — final review

---

## Common interview topics

- "What are Core Web Vitals? What are the thresholds?"
- "How do you measure LCP? How do you improve it?"
- "Your LCP is 4 seconds. Walk me through how you'd debug it."
- "How do you set performance budgets?"
- "Difference between lab and field data?"
- "INP vs FID — what changed?"

---

## Cross-References

- [Accessibility](../50.2-accessibility/INDEX.md) — Lighthouse a11y audits
- [Build Tools](../../40-platform/40.5-build-tools/INDEX.md) — bundle size from bundlers
- [Observability](../../40-platform/40.4-observability/INDEX.md) — backend observability
- [React Performance](../../10-frontend/10.3-react/INDEX.md) — React Profiler

---

## Navigation

[← Previous: Accessibility](../50.2-accessibility/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: WebSockets →](../../60-realtime/60.1-websockets/INDEX.md)
