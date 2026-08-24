# Testing — Index

> **13 files** — Testing fundamentals from Jest and React Testing Library to unit, integration, E2E, performance testing, chaos engineering, mocking, test patterns, frameworks comparison, and interview questions.

[![Files](https://img.shields.io/badge/files-13-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why testing:** Every senior engineer must own their test strategy. Test pyramid (unit/integration/E2E), coverage trade-offs, mocking patterns, and the ability to debug flaky tests. This section is the canonical reference.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Fundamentals](#fundamentals) | 1 | Test types, testing pyramid, TDD vs BDD, coverage |
| [Test Frameworks](#test-frameworks) | 3 | Jest, Vitest, RTL — the main tools |
| [Test Levels](#test-levels) | 3 | Unit, integration, E2E — the test pyramid |
| [Mocking & Patterns](#mocking--patterns) | 2 | Mocking, test patterns (Arrange-Act-Assert, factories) |
| [Advanced Testing](#advanced-testing) | 3 | Performance/load, chaos engineering, framework comparison |
| [Interview Prep](#interview-prep) | 1 | 40+ Qs |

---

## Fundamentals

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Testing Overview](50.1.01-testing-overview.md) | Test types, testing pyramid, TDD, BDD, coverage, strategies, when to write which test | 30 min |

---

## Test Frameworks

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 02 | [Jest](50.1.02-jest.md) | Configuration, matchers, snapshots, mocking, code coverage | Most React/Node projects | 30 min |
| 10 | [Vitest](50.1.10-vitest.md) | Native ESM, Vite integration, HMR, Jest-compatible, worker threads | Vite-based projects, faster than Jest | 30 min |
| 03 | [React Testing Library](50.1.03-react-testing-library.md) | Render, queries, events, async testing, accessibility (testing-library/jest-dom) | React component tests | 30 min |

---

## Test Levels

The test pyramid in practice.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 04 | [Unit Testing](50.1.04-unit-testing.md) | Isolated tests, boundaries, dependency injection, stubs | Pure functions, business logic | 25 min |
| 05 | [Integration Testing](50.1.05-integration-testing.md) | Component integration, API testing, database testing (Testcontainers) | Service-level, multiple modules | 25 min |
| 06 | [E2E Testing](50.1.06-e2e-testing.md) | Playwright, Cypress, user flows, visual regression | Critical user journeys | 30 min |

**Test pyramid:**

```text
       /\
      / \ E2E (slow, expensive, high confidence)
     /────\
    / \ Integration (medium speed, medium confidence)
   /────────\
  / \ Unit (fast, cheap, narrow confidence)
/────────────\
```

Aim for **lots of unit tests, some integration, few E2E.**

---

## Mocking & Patterns

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [Mocking](50.1.07-mocking.md) | Mock functions, spies, modules, network requests (MSW), time | 30 min |
| 08 | [Test Patterns](50.1.08-test-patterns.md) | Arrange-Act-Assert, factory methods, test fixtures, builders | 20 min |

---

## Advanced Testing

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 11 | [Performance & Load Testing](50.1.11-performance-load-testing.md) | k6, Artillery, Locust, p95/p99, ramp-up, stress/soak | Production-scale services | 30 min |
| 12 | [Chaos Engineering & Game Days](50.1.12-chaos-engineering.md) | Steady-state hypothesis, blast radius, Toxiproxy, Chaos Monkey, Gremlin, Litmus | Resilient distributed systems | 30 min |
| 13 | [Testing Frameworks Comparison](50.1.13-testing-frameworks-comparison.md) | Jest vs Vitest, Playwright E2E, Supertest API testing, choosing the right framework | Stack decisions | 20 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 09 | [Testing Interview Questions](50.1.09-interview-questions.md) | 40+ curated questions grouped by difficulty | 2-3 hrs |

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
