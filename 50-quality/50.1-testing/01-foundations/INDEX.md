# Testing Foundations

> **2 files.** The mental model before any tool: the testing pyramid, test types, TDD vs BDD, coverage trade-offs — and the data that feeds every suite. Everything else in the testing stack assumes this vocabulary.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why foundations first

Tool questions ("Jest or Vitest?") are cheap. Strategy questions ("what do you test, and why?") are what interviews and incidents actually probe. This category builds the strategy layer:

- The **testing pyramid** — many unit tests, fewer integration tests, few E2E tests.
- **Test types** — unit, integration, E2E, and where contract/smoke tests fit.
- **TDD vs BDD** — red-green-refactor vs behavior specs as shared language.
- **Coverage** — what it measures, what it hides, why 100% is not the goal.
- **Test data** — factories, faker generators, anonymization, golden datasets.

---

## The files

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Testing Overview](50.1.1.01-testing-overview.md) | Test types, testing pyramid, TDD, BDD, coverage, strategies, when to write which test | 30 min |
| 02 | [Test Data Management & Anonymization](50.1.1.02-test-data-management-anonymization.md) | Test data pyramid, factories/builders, faker, PII risks, GDPR-safe staging seeding, golden datasets, refresh pipelines | 30 min |

---

## Key takeaways

- The pyramid is a cost/confidence trade-off, not dogma — but you must justify deviations (e.g., testing trophies) explicitly.
- Coverage is a **negative** signal: low coverage means untested code; high coverage proves nothing about assertion quality.
- Write tests for behavior at boundaries, not implementation details.

---

## Cross-References

- [Frameworks](../02-frameworks/INDEX.md) — the tools that implement this model.
- [Test Levels](../03-test-levels/INDEX.md) — each pyramid layer in depth.

---

## Navigation

[↑ Testing Home](../INDEX.md) · [Next: Frameworks →](../02-frameworks/INDEX.md)
