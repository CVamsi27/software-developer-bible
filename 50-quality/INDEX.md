# Quality Stack

> **Study time:** ≈ 9 h 38 m of reading (48 files, ~12 min average).
> **Testing, accessibility, performance monitoring, production engineering** — the "senior judgment" stack. Shared by both lanes.
>
> 48 files across 4 sub-stacks.

[![Files](https://img.shields.io/badge/files-48-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-4-green)](#the-4-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Docita Anchor

Everything in this stack is practiced — not just studied — in [docita](https://github.com/CVamsi27/docita), the companion production repo: 482 co-located spec files and Playwright E2E suites back the testing topics, `scripts/perf/` budget gates back performance governance, and `docs/runbooks/`, `docs/operations/playbooks/`, and 15 numbered ADRs back production engineering. Each sub-stack INDEX carries its own **Docita Anchor** table with verified file paths; chaos engineering is honestly flagged there as having no direct docita implementation yet.

---

## Why this stack matters

Quality is what separates a senior engineer from a mid-level one. Every senior interview (especially at FAANG) tests:
- **Testing** — unit, integration, E2E, mocking, test pyramid, coverage trade-offs
- **Performance** — Core Web Vitals, profiling, bundle analysis, performance budgets
- **Production Engineering** — incident response, SLI/SLO/error budgets, blameless postmortems
- **Accessibility** — WCAG, ARIA, keyboard navigation (often overlooked, cheap interview points)

This is the stack where you prove you can ship software that doesn't break.

---

## The 4 Sub-Stacks (in study order)

| Order | Sub-stack | Files | Topics |
| ----: | -------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------------------------------------- |
| 1 | [Testing](50.1-testing/INDEX.md) | 14 | Jest, RTL, unit, integration, E2E (Playwright), mocking, Vitest, test data management, load testing, chaos engineering |
| 2 | [Accessibility](50.2-accessibility/INDEX.md) | 9 | WCAG, ARIA, keyboard navigation, color contrast, forms & labels, charts, design systems |
| 3 | [Performance Monitoring](50.3-performance-monitoring/INDEX.md) | 9 | Core Web Vitals, profiling tools, Lighthouse CI, bundle analysis, RUM, HTTP/2 & HTTP/3, performance budgets |
| 4 | [Production Engineering](50.4-production-engineering/INDEX.md) | 5 | Incident response, SLI/SLO/error budgets, chaos engineering, production readiness reviews, on-call |

---

## Category Map

| Category | What it covers | When to read |
| -------------------------- | ---------------------------------------------------- | ----------------------------- |
| **Testing** | Unit, integration, E2E, mocking, load testing | First — asked in every loop |
| **Performance** | CWV, profiling, bundle analysis, performance budgets | Second — frontend-specific |
| **Production Engineering** | Incidents, SLO, error budgets, chaos engineering | Third — senior differentiator |
| **Accessibility** | WCAG, ARIA, keyboard, screen readers | Fourth — JD-dependent depth |

---

## Suggested Study Order

1. **Testing pyramid** → frameworks → E2E *(asked in every loop)*
2. **Performance**: CWV thresholds + profiling workflow
3. **Production engineering**: incident story + SLO vocabulary *(senior differentiator)*
4. **Accessibility**: WCAG basics *(cheap points; JD-dependent depth)*

---

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
- [System Design](../INDEX.md) — performance at scale

---

## Navigation

[← Previous: Platform](../40-platform/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Real-Time →](../60-realtime/INDEX.md)
