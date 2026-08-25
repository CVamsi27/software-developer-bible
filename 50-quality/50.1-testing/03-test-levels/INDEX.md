# Test Levels

> **3 files.** The test pyramid in practice: unit, integration, and E2E — what to test at each level, which tools, and how much confidence each layer buys.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The pyramid

```text
       /\
      / \ E2E (slow, expensive, high confidence)
     /----\
    /      \ Integration (medium speed, medium confidence)
   /----------\
  /            \ Unit (fast, cheap, narrow confidence)
/----------------\
```

Aim for **lots of unit tests, some integration, few E2E.**

---

## The 3 levels

| # | File | Level | Topics | When to use | Read time |
|--:|------|-------|--------|-------------|----------:|
| 01 | [Unit Testing](50.1.3.01-unit-testing.md) | Base | Isolated tests, boundaries, dependency injection, stubs | Pure functions, business logic | 25 min |
| 02 | [Integration Testing](50.1.3.02-integration-testing.md) | Middle | Component integration, API testing, database testing (Testcontainers) | Service-level, multiple modules | 25 min |
| 03 | [E2E Testing](50.1.3.03-e2e-testing.md) | Top | Playwright, Cypress, user flows, visual regression | Critical user journeys | 30 min |

---

## How the layers divide responsibility

- **Unit** — logic branches, edge cases, error paths. Milliseconds each; run on every save.
- **Integration** — module seams: HTTP handlers with real routing, DB access against containers, queue consumers. Catches wiring bugs unit tests cannot see.
- **E2E** — money paths only (signup, checkout, core workflow). Slow and flaky-prone; budget them like production infra.

Interview trap: "Why not just write E2E tests for everything?" — feedback loop time, flakiness, cost, and blast-radius-free failure diagnosis.

---

## Cross-References

- [Frameworks](../02-frameworks/INDEX.md) — runners and component libraries per level.
- [Advanced](../05-advanced/INDEX.md) — load and chaos testing operate above the pyramid.

---

## Navigation

[← Frameworks](../02-frameworks/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Mocking & Patterns →](../04-mocking-and-patterns/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
|-------|-----------------|
| Unit/integration level | co-located `*.spec.ts` files throughout `apps/api/src` (482 total) |
| Component level | `*.test.tsx` files under `packages/ui` |
| E2E critical flows | `apps/app/e2e/critical-flows.spec.ts` plus per-feature specs (`auth`, `appointments`, `invoices`, …) |
| Multi-app E2E suites | `apps/app/e2e/`, `apps/internal/e2e/`, `apps/landing/e2e/` |
