# Testing Foundations

> **Study time:** ≈ 24 min of reading (3 files, ~8 min average).
> **3 files.** The mental model before any tool: the testing pyramid, test types, TDD vs BDD, coverage trade-offs — and the data that feeds every suite. Everything else in the testing stack assumes this vocabulary.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why foundations first

Tool questions ("Jest or Vitest?") are cheap. Strategy questions ("what do you test, and why?") are what interviews and incidents actually probe. This category builds the strategy layer:

- The **testing pyramid** — a cost-and-feedback starting model, not a required test ratio.
- **Test types** — unit, integration, E2E, and where contract/smoke tests fit.
- **TDD and BDD** — a short test/implementation/refactor cycle and collaborative discovery of concrete behavior; they are not mutually exclusive alternatives.
- **Coverage** — what execution metrics reveal and why they cannot replace a useful test oracle.
- **Test data** — factories, faker generators, anonymization versus pseudonymization, golden datasets.

---

## The files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Testing Overview](50.1.1.01-testing-overview.md) | Test types, testing pyramid, TDD, BDD, coverage, strategies, when to write which test | Essential | Foundational | 11 min |
| 02 | [Test Data Management & Anonymization](50.1.1.02-test-data-management-anonymization.md) | Explicit fixtures, seeded variety, join-preserving pseudonyms, identification risk, golden oracles, refresh validation | Essential | Foundational | 11 min |

---

## Key takeaways

- The pyramid guides cost and feedback; choose the actual mix from the defect risks and boundaries you need to examine.
- Coverage records execution, not correctness. Use uncovered critical paths to find missing scenarios, and inspect assertions for meaningful checks.
- Assert the observable contract at the boundary that can expose the defect; test a collaborator interaction directly when that interaction is itself required behavior.

---

## Cross-References

- [Frameworks](../02-frameworks/INDEX.md) — the tools that implement this model.
- [Test Levels](../03-test-levels/INDEX.md) — each pyramid layer in depth.

---

## Navigation

[↑ Testing Home](../INDEX.md) · [Next: Frameworks →](../02-frameworks/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Testing strategy doc | `docs/testing/TESTING.md` |
| Co-located unit tests | `*.spec.ts` files beside their source across `apps/api/src` |
| Deterministic time (injected clock port) | `apps/api/src/shared/common/ports/clock.port.ts` + `apps/api/src/shared/modules/time/system-clock.service.ts` |
| Test data factories | `apps/api/src/test-utils/factories.ts` |
| E2E layer with Playwright | `apps/app/e2e/` + `apps/app/playwright.config.ts` (also `apps/internal`, `apps/landing`) |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
