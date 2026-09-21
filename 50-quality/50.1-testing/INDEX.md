# Testing — Index

> **Study time:** ≈ 8 h 5 m of reading (14 files, ~35 min average).
> **14 files across 6 categories.** Testing fundamentals from Jest and React Testing Library to unit, integration, E2E, performance testing, chaos engineering, mocking, test patterns, frameworks comparison, test data management, and interview questions.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why testing:** Every senior engineer must own their test strategy. Test pyramid (unit/integration/E2E), coverage trade-offs, mocking patterns, and the ability to debug flaky tests. This section is the canonical reference.

---

## The 6 Categories (in study order)

| Category | Files | Purpose |
| ----------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------- |
| [01 — Foundations](01-foundations/INDEX.md) | 2 | Test types, testing pyramid, TDD vs BDD, coverage, test data management — the vocabulary |
| [02 — Frameworks](02-frameworks/INDEX.md) | 4 | Jest, Vitest, RTL, comparison — the tools |
| [03 — Test Levels](03-test-levels/INDEX.md) | 3 | Unit, integration, E2E — the pyramid in practice |
| [04 — Mocking & Patterns](04-mocking-and-patterns/INDEX.md) | 2 | Mocking mechanics + AAA/factories/builders |
| [05 — Advanced](05-advanced/INDEX.md) | 2 | Performance/load testing, chaos engineering |
| [06 — Interview Prep](06-interview-prep/INDEX.md) | 1 | 40+ Qs |

---

## Foundations

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Testing Overview](01-foundations/50.1.1.01-testing-overview.md) | Test types, testing pyramid, TDD, BDD, coverage, strategies, when to write which test | 29 min |
| 02 | [Test Data Management & Anonymization](01-foundations/50.1.1.02-test-data-management-anonymization.md) | Test data pyramid, factories, faker, anonymization/pseudonymization, GDPR-safe seeding, golden datasets | 15 min |

---

## Frameworks

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 01 | [Jest](02-frameworks/50.1.2.01-jest.md) | Configuration, matchers, snapshots, mocking, code coverage | Most React/Node projects | 44 min |
| 02 | [Vitest](02-frameworks/50.1.2.02-vitest.md) | Native ESM, Vite integration, HMR, Jest-compatible, worker threads | Vite-based projects, faster than Jest | 15 min |
| 03 | [React Testing Library](02-frameworks/50.1.2.03-react-testing-library.md) | Render, queries, events, async testing, accessibility (testing-library/jest-dom) | React component tests | 49 min |
| 04 | [Testing Frameworks Comparison](02-frameworks/50.1.2.04-testing-frameworks-comparison.md) | Jest vs Vitest, Playwright E2E, Supertest API testing, choosing the right framework | Stack decisions | 11 min |

---

## Test Levels

The test pyramid in practice.

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

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 01 | [Unit Testing](03-test-levels/50.1.3.01-unit-testing.md) | Isolated tests, boundaries, dependency injection, stubs | Pure functions, business logic | 50 min |
| 02 | [Integration Testing](03-test-levels/50.1.3.02-integration-testing.md) | Component integration, API testing, database testing (Testcontainers) | Service-level, multiple modules | 48 min |
| 03 | [E2E Testing](03-test-levels/50.1.3.03-e2e-testing.md) | Playwright, Cypress, user flows, visual regression | Critical user journeys | 41 min |

---

## Mocking & Patterns

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Mocking](04-mocking-and-patterns/50.1.4.01-mocking.md) | Mock functions, spies, modules, network requests (MSW), time | 47 min |
| 02 | [Test Patterns](04-mocking-and-patterns/50.1.4.02-test-patterns.md) | Arrange-Act-Assert, factory methods, test fixtures, builders | 49 min |

---

## Advanced

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 01 | [Performance & Load Testing](05-advanced/50.1.5.01-performance-load-testing.md) | k6, Artillery, Locust, p95/p99, ramp-up, stress/soak | Production-scale services | 19 min |
| 02 | [Chaos Engineering & Game Days](05-advanced/50.1.5.02-chaos-engineering.md) | Steady-state hypothesis, blast radius, Toxiproxy, Chaos Monkey, Gremlin, Litmus | Resilient distributed systems | 20 min |

---

## Interview Prep

| # | File | Contents | Time |
| --: | ------ | ---------- | ------ |
| 01 | [Testing Interview Questions](06-interview-prep/50.1.6.01-interview-questions.md) | 40+ curated questions grouped by difficulty | 2-3 hrs |

---

## Suggested Study Order

1. **Testing Overview** — must know the pyramid
2. **Jest or Vitest** — the framework your team uses
3. **React Testing Library** — if React focus
4. **Unit Testing** — must know
5. **Integration + E2E** — for senior roles
6. **Mocking + Test Patterns** — the senior-level
7. **Performance + Chaos** — for staff/SRE roles
8. **Interview Questions** — final review

---

## Common interview topics

- "What's your testing strategy? Why?"
- "Unit vs integration vs E2E — when to use which?"
- "How do you test async code?"
- "How do you test React components?"
- "How do you mock network requests?"
- "What does good test coverage look like? Is 100% the goal?"

---

## Cross-References

- [React](../../10-frontend/10.3-react/INDEX.md) — RTL for component tests
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — NestJS testing module
- [CI/CD](../../40-platform/40.3-ci-cd/INDEX.md) — running tests in CI
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — testing algorithm solutions

---

## Navigation

[← Previous: Twelve-Factor App](../../40-platform/40.9-twelve-factor/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Accessibility →](../50.2-accessibility/INDEX.md)
