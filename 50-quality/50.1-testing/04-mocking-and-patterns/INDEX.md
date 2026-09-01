# Mocking & Test Patterns

> **2 files.** How to isolate code under test (mocks, spies, stubs, MSW) and how to structure tests that stay maintainable at scale (Arrange-Act-Assert, factories, fixtures, builders).

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why these belong together

Isolation without structure produces brittle suites; structure without isolation produces slow ones. Senior-level testing is the combination: replace the *right* boundaries with doubles, and keep every test readable as three sentences.

---

## The 2 files

| #   | File                                        | Topics                                                              | Read time   |
| --: | ------                                      | --------                                                            | ----------: |
| 01  | [Mocking](50.1.4.01-mocking.md)             | Mock functions, spies, modules, network requests (MSW), fake timers | 30 min      |
| 02  | [Test Patterns](50.1.4.02-test-patterns.md) | Arrange-Act-Assert, factory methods, test fixtures, builders        | 20 min      |

---

## What to mock (and what not to)

```text
Mock:            HTTP edges (MSW), clocks/timers, queues, third-party SDKs
Do NOT mock:     the unit under test's own logic, plain value objects,
                 everything (over-mocking = testing your mocks)
```

Interview trap: "Your test mocks half the system — what are you actually verifying?" Over-mocking is the most common senior-level criticism of test suites.

---

## Patterns that keep suites alive

- **Arrange-Act-Assert** — one behavior per test; the Act section should be one line.
- **Object mother / fixture** — canonical valid entities for shared setup.
- **Test data builder** — `buildUser({ role: "admin" })`; defaults in one place, overrides explicit.
- **Naming** — `subject_condition_expectation` ("cancel_unpaidInvoice_throws").

---

## Cross-References

- [Frameworks](../02-frameworks/INDEX.md) — where jest.fn / vi.fn live.
- [Foundations](../01-foundations/INDEX.md) — why boundary mocking follows from test strategy.

---

## Navigation

[← Test Levels](../03-test-levels/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Advanced →](../05-advanced/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic                                                     | Docita evidence                                                              |
| --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Clock mock                                                | `apps/api/src/test-utils/fixed-clock.mock.ts`                                |
| Factories / builders                                      | `apps/api/src/test-utils/factories.ts`                                       |
| Time injection seam (mock at the port, not the call site) | `apps/api/src/shared/common/ports/clock.port.ts` ← `system-clock.service.ts` |
| Guard-level spec example                                  | `apps/api/src/shared/modules/auth/auth/ws-jwt-auth.guard.spec.ts`            |
