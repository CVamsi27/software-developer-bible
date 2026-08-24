# Performance Monitoring — Index

> **8 files** — Web performance monitoring from Core Web Vitals, performance APIs, profiling tools, Lighthouse CI, bundle analysis, real-user monitoring, and performance budgets to interview questions.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why performance monitoring:** Core Web Vitals affect SEO, conversion, and user satisfaction. Senior frontend interviews test LCP/INP/CLS, profiling workflow, and performance budgets. Slow sites lose users — every 100ms costs ~1% of revenue.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Core Metrics](#core-metrics) | 1 | LCP, INP, CLS — the three pillars |
| [Measurement](#measurement) | 2 | Performance APIs, profiling tools |
| [Lab Testing](#lab-testing) | 1 | Lighthouse CI — automated audits |
| [Real-User Monitoring](#real-user-monitoring) | 1 | RUM, CrUX — what users actually see |
| [Optimization](#optimization) | 2 | Bundle analysis, performance budgets |
| [Interview Prep](#interview-prep) | 1 | 25+ Qs |

---

## Core Metrics

The 3 Core Web Vitals — every senior frontend interview starts here.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Core Web Vitals](50.3.01-core-web-vitals.md) | LCP, INP, CLS — measurement, thresholds, optimization strategies. INP replaced FID in 2024. | 30 min |

**The 3 metrics (memorize thresholds):**
- **LCP** (Largest Contentful Paint) — should be **≤ 2.5s**
- **INP** (Interaction to Next Paint) — should be **≤ 200ms**
- **CLS** (Cumulative Layout Shift) — should be **≤ 0.1**

---

## Measurement

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [Performance APIs](50.3.02-performance-apis.md) | `performance` API, Navigation Timing, Resource Timing, observers (PerformanceObserver) | 25 min |
| 03 | [Profiling Tools](50.3.03-profiling-tools.md) | Chrome DevTools, Lighthouse, WebPageTest, React Profiler, flame charts | 30 min |

---

## Lab Testing

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 05 | [Lighthouse CI](50.3.05-lighthouse-ci.md) | Automated audits, budgets, score tracking, CI/CD integration | 25 min |

---

## Real-User Monitoring

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [Real User Monitoring](50.3.07-real-user-monitoring.md) | RUM, `web-vitals` library, `sendBeacon`, CrUX (Chrome User Experience Report), segmentation | 25 min |

---

## Optimization

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Bundle Analysis](50.3.06-bundle-analysis.md) | Bundle size, tree shaking, code splitting, bundlephobia, source-map-explorer | 25 min |
| 08 | [Performance Budgets](50.3.08-performance-budgets.md) | `size-limit`, per-chunk budgets, CI enforcement, budgeting tiers | 20 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Interview Questions](50.3.04-interview-questions.md) | 25+ curated questions with answers | 1-2 hrs |

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
