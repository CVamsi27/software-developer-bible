# Quality Stack

> **Study time:** ≈ 5 h 33 m of reading (48 files, ~7 min average).
> **Testing, accessibility, performance monitoring, production engineering** — the "senior judgment" stack. Shared by both lanes.
>
> 48 files across 4 sub-stacks.

[![Files](https://img.shields.io/badge/files-48-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-4-green)](#the-4-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why these responsibilities belong together

A change can satisfy its unit tests while excluding keyboard users, slowing a critical journey or failing during recovery. These topics ask different questions about the same product: does the behavior satisfy its contract, can people use it, does it perform under its workload, and can the team operate it when a dependency fails?

## Use companion evidence carefully

[Docita](https://github.com/CVamsi27/docita) contains test specifications, performance-budget scripts and operational documents to inspect. Each sub-stack points to relevant artifacts. Their existence does not establish a current pass, complete implementation or personal authorship. Fault injection and other simulations need their own executed evidence.

## The 4 Sub-Stacks (in study order)

| Order | Sub-stack | Files | Topics |
| ----: | -------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------------------------------------- |
| 1 | [Testing](50.1-testing/INDEX.md) | 14 | Jest, RTL, unit, integration, E2E (Playwright), mocking, Vitest, test data management, load testing, chaos engineering |
| 2 | [Accessibility](50.2-accessibility/INDEX.md) | 9 | WCAG, ARIA, keyboard navigation, color contrast, forms & labels, charts, design systems |
| 3 | [Performance Monitoring](50.3-performance-monitoring/INDEX.md) | 9 | Core Web Vitals, profiling tools, Lighthouse CI, bundle analysis, RUM, HTTP/2 & HTTP/3, performance budgets |
| 4 | [Production Engineering](50.4-production-engineering/INDEX.md) | 6 | Incident response, SLI/SLO/error budgets, chaos engineering, production readiness reviews, on-call |

---

## Learning passes

1. **Testing:** state the behavior and expected result, then choose controlled and real boundaries. Complete each category's separate revision before its interview practice.
2. **Accessibility:** learn semantic structure, keyboard/focus behavior, perceivable content and error recovery. Combine automated findings with manual journeys through the actual interface.
3. **Performance monitoring:** distinguish laboratory observations from real-user populations, diagnose the contributing path and verify the result under comparable conditions.
4. **Production engineering:** connect user outcomes to objectives, bounded experiments, release evidence, incident response and sustainable response ownership.

The order supplies measurement and boundary reasoning before operational decisions. A role or project can change the depth of practice; accessibility and failure recovery still remain product responsibilities.

## Interview questions to expect

- "How do you decide what to test?"
- "Walk me through a Core Web Vitals issue you debugged."
- "Tell me about a production incident. What was the timeline? How did you resolve?"
- "What's the difference between SLI, SLO, and SLA? How do you set error budgets?"
- "How do you test accessibility? Walk me through a screen reader session."
- "What's your team's testing strategy? How do you balance speed vs coverage?"

---

## Cross-References

- [Frontend Stack](../10-frontend/INDEX.md) — testing React components (RTL)
- [Backend Stack](../20-backend/INDEX.md) — integration tests, load testing
- [Platform Stack — Observability](../40-platform/40.4-observability/INDEX.md) — production monitoring
- [System Design](../30-architecture/30.2-system-design/INDEX.md) — performance at scale

---

## Navigation

[← Previous: Platform](../40-platform/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Real-Time →](../60-realtime/INDEX.md)
