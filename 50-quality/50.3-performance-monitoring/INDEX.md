# Performance Monitoring — Index

> **Study time:** ≈ 1 h 21 m of reading (12 files, ~7 min average).
> **12 files across 4 categories.** Web performance monitoring from Core Web Vitals, performance APIs, profiling tools, Lighthouse CI, bundle analysis, real-user monitoring, HTTP/2 & HTTP/3 protocol effects, and performance budgets to interview questions.

[![Files](https://img.shields.io/badge/files-12-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why performance monitoring:** Performance monitoring connects loading, interaction and visual stability to decisions about a real user journey. It also helps assess search and business outcomes, which need their own scope and evidence. Senior interviews test LCP/INP/CLS, profiling and enforced budgets.

---

## The 4 Categories (in study order)

| Category | Files | Purpose |
| ------------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------ |
| [01 — Core Metrics](01-core-metrics/INDEX.md) | 1 | LCP, INP, CLS — the three pillars and their thresholds |
| [02 — Measurement](02-measurement/INDEX.md) | 5 | Performance APIs, profiling tools, Lighthouse CI, RUM, HTTP/2 & HTTP/3 effects |
| [03 — Optimization & Governance](03-optimization-and-governance/INDEX.md) | 2 | Bundle analysis, performance budgets |
| [04 — Interview Prep](04-interview-prep/INDEX.md) | 1 | 30 questions |

---

## Core Metrics

Learn the three metrics and their distinct observation boundaries before choosing an optimization.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Core Web Vitals](01-core-metrics/50.3.1.01-core-web-vitals.md) | LCP, INP, CLS — measurement, thresholds, optimization strategies. INP replaced FID in 2024. | Important | Important | 8 min |

**Good thresholds (evaluate eligible observations at p75):**
- **LCP** (Largest Contentful Paint) — should be **≤ 2.5s**
- **INP** (Interaction to Next Paint) — should be **≤ 200ms**
- **CLS** (Cumulative Layout Shift) — should be **≤ 0.1**

---

## Measurement

Laboratory tests control a workload; field collection samples real visits. Performance APIs can serve both. Check coverage and population before comparing results.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Performance APIs](02-measurement/50.3.2.01-performance-apis.md) | `performance` API, Navigation Timing, Resource Timing, observers (PerformanceObserver) | Important | Important | 8 min |
| 02 | [Profiling Tools](02-measurement/50.3.2.02-profiling-tools.md) | Chrome DevTools, Lighthouse, WebPageTest, React Profiler, flame charts | Important | Important | 9 min |
| 03 | [Lighthouse CI](02-measurement/50.3.2.03-lighthouse-ci.md) | Automated audits, budgets, score tracking, CI/CD integration | Important | Important | 7 min |
| 04 | [Real User Monitoring](02-measurement/50.3.2.04-real-user-monitoring.md) | RUM, `web-vitals` library, `sendBeacon`, CrUX (Chrome User Experience Report), segmentation | Important | Important | 11 min |
| 05 | [HTTP/2 & HTTP/3 Performance Effects](02-measurement/50.3.2.05-http2-http3-performance-effects.md) | Multiplexing, TCP head-of-line blocking, QUIC, 0-RTT, connection migration, protocol-segmented RUM | Important | Important | 8 min |

---

## Optimization & Governance

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Bundle Analysis](03-optimization-and-governance/50.3.3.01-bundle-analysis.md) | Bundle size, tree shaking, code splitting, bundlephobia, source-map-explorer | Important | Important | 8 min |
| 02 | [Performance Budgets](03-optimization-and-governance/50.3.3.02-performance-budgets.md) | artifact and route budgets, CI enforcement, explicit units and exception ownership | Important | Important | 8 min |

---

## Interview Prep

| # | File | Contents | Time | Role priority | General importance |
| --: | ------ | ---------- | ------ | --- | --- |
| 01 | [Interview Questions](04-interview-prep/50.3.4.01-interview-questions.md) | 30 questions with answers and changed-condition probes | 1-2 hrs | Important | Important |

---

## Suggested Study Order

1. **Core Web Vitals** — trace the metric and identify its observation boundary
2. **Performance APIs, then Profiling Tools** — choose a timing boundary, then attribute the delay
3. **Bundle Analysis** — trace shipped assets to imports and route requests
4. **Lighthouse CI** — make a repeatable lab regression fail visibly in the pipeline
5. **RUM, then HTTP/2 & HTTP/3** — understand the observed population and the connection behavior behind it
6. **Performance Budgets** — turn selected measurements into owned release decisions
7. **Category revision companions**, then **Interview Questions** — derive answers before changing a condition

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
