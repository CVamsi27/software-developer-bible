# Testing — Index

> **Study time:** ≈ 2 h 30 m of reading (19 files, ~8 min average).
> **19 files across six categories.** Learn testing fundamentals, framework behavior, unit/integration/E2E boundaries, test data, mocking, reusable patterns, load and fault experiments, then practice the interview bank.

[![Files](https://img.shields.io/badge/files-19-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

## Read from behavior to release evidence

A test observes selected behavior under a controlled arrangement. Start with the expected result and boundary, then learn how a runner executes it, how real integrations change the evidence, and how load or fault experiments test different conditions. Tool names and coverage percentages are useful only after that claim is clear.

## Six categories in study order

| Category | Files | Purpose |
| ----------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------ |
| [01 — Foundations](01-foundations/INDEX.md) | 2 | Test types, testing pyramid, TDD vs BDD, coverage, test data management — contract, observation and data ownership |
| [02 — Frameworks](02-frameworks/INDEX.md) | 4 | Jest, Vitest, RTL, comparison — execution, module behavior and awaited UI observations |
| [03 — Test Levels](03-test-levels/INDEX.md) | 3 | Unit, integration, E2E — scope and real-boundary evidence |
| [04 — Mocking & Patterns](04-mocking-and-patterns/INDEX.md) | 2 | Controlled collaborators, visible scenarios and resource ownership |
| [05 — Advanced](05-advanced/INDEX.md) | 2 | Workload models, semantic thresholds and bounded fault experiments |
| [06 — Interview Prep](06-interview-prep/INDEX.md) | 1 | Forty questions with changed-condition probes |

---

## Foundations

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Testing Overview](01-foundations/50.1.1.01-testing-overview.md) | Test types, testing pyramid, TDD, BDD, coverage, strategies, when to write which test | Essential | Foundational | 11 min |
| 02 | [Test Data Management & Anonymization](01-foundations/50.1.1.02-test-data-management-anonymization.md) | Synthetic ownership, deterministic generation, anonymization/pseudonymization and golden oracles | Essential | Foundational | 11 min |

---

## Frameworks

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Jest](02-frameworks/50.1.2.01-jest.md) | Configuration, matchers, snapshots, mocking, code coverage | Most React/Node projects | Essential | Foundational | 10 min |
| 02 | [Vitest](02-frameworks/50.1.2.02-vitest.md) | Runtime/configuration, transforms, mocking and migration boundaries | Choose from compatibility and measured suite behavior | Essential | Foundational | 9 min |
| 03 | [React Testing Library](02-frameworks/50.1.2.03-react-testing-library.md) | Render, queries, events, async testing, accessibility (testing-library/jest-dom) | React component tests | Essential | Foundational | 11 min |
| 04 | [Testing Frameworks Comparison](02-frameworks/50.1.2.04-testing-frameworks-comparison.md) | Jest vs Vitest, Playwright E2E, Supertest API testing, choosing the right framework | Stack decisions | Essential | Foundational | 5 min |

---

## Test Levels

Choose the smallest boundary that observes the relevant failure. Broader scope adds real seams and also setup, cost and diagnosis sources; it does not automatically make every assertion stronger. The pyramid is a feedback-cost model, not a universal test-count ratio.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Unit Testing](03-test-levels/50.1.3.01-unit-testing.md) | Isolated tests, boundaries, dependency injection, stubs | Pure functions, business logic | Essential | Foundational | 10 min |
| 02 | [Integration Testing](03-test-levels/50.1.3.02-integration-testing.md) | Component integration, API testing, database testing (Testcontainers) | Service-level, multiple modules | Essential | Foundational | 10 min |
| 03 | [E2E Testing](03-test-levels/50.1.3.03-e2e-testing.md) | Playwright, Cypress, user flows, visual regression | Critical user journeys | Essential | Foundational | 11 min |

---

## Mocking & Patterns

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Mocking](04-mocking-and-patterns/50.1.4.01-mocking.md) | Mock functions, spies, modules, network requests (MSW), time | Essential | Foundational | 10 min |
| 02 | [Test Patterns](04-mocking-and-patterns/50.1.4.02-test-patterns.md) | Arrange-Act-Assert, factory methods, test fixtures, builders | Essential | Foundational | 11 min |

---

## Advanced

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Performance & Load Testing](05-advanced/50.1.5.01-performance-load-testing.md) | k6, Artillery, Locust, p95/p99, ramp-up, stress/soak | Production-scale services | Important | Specialized | 10 min |
| 02 | [Chaos Engineering & Game Days](05-advanced/50.1.5.02-chaos-engineering.md) | Steady-state hypothesis, blast radius, Toxiproxy, Chaos Monkey, Gremlin, Litmus | Resilient distributed systems | Important | Specialized | 10 min |

---

## Interview Prep

| # | File | Contents | Time | Role priority | General importance |
| --: | ------ | ---------- | ------ | --- | --- |
| 01 | [Testing Interview Questions](06-interview-prep/50.1.6.01-interview-questions.md) | 40 questions across fundamentals, async behavior, application boundaries, strategy and experience | Practice in several sessions | Essential | Foundational |

---

## Learning passes and revision

1. **State the contract:** foundations and data management explain outcomes, assertions, observed code and resource ownership. Finish the [foundations revision](01-foundations/REVISION.md).
2. **Run and observe:** choose the compatible runner, then learn awaited component observations and its evidence boundary. Finish the [framework revision](02-frameworks/REVISION.md).
3. **Choose scope:** unit, integration and complete journeys establish different claims. Finish the [test-level revision](03-test-levels/REVISION.md).
4. **Control and reuse deliberately:** mocking and patterns preserve consumer behavior, scenario visibility and cleanup. Finish the [mocking/pattern revision](04-mocking-and-patterns/REVISION.md).
5. **Vary operating conditions:** workload and fault experiments separate the offered input, observed response and recovery. Finish the [advanced revision](05-advanced/REVISION.md).
6. **Practice decisions:** answer the [interview bank](06-interview-prep/INDEX.md), including its changed-condition probes and supported experience questions.

## Cross-References

- [React](../../10-frontend/10.3-react/INDEX.md) — RTL for component tests
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — NestJS testing module
- [CI/CD](../../40-platform/40.3-ci-cd/INDEX.md) — running tests in CI
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — testing algorithm solutions

---

## Navigation

[← Previous: Twelve-Factor App](../../40-platform/40.9-twelve-factor/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Accessibility →](../50.2-accessibility/INDEX.md)
