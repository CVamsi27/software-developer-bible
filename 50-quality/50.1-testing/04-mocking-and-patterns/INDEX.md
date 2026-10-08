# Mocking & Test Patterns

> **Study time:** ≈ 23 min of reading (3 files, ~8 min average).
> **3 files.** How to isolate code under test (mocks, spies, stubs, MSW) and how to structure tests that stay maintainable at scale (Arrange-Act-Assert, factories, fixtures, builders).

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Read the real logic against a controlled boundary

A dependency replacement makes selected inputs controllable but also removes the real dependency from observation. Test structure makes the resulting claim visible: which state was arranged, which action ran and which result was checked. Start with the boundary, then introduce helpers only where repetition obscures that contract.

## First pass: choose the replacement and its evidence boundary

Read [Mocking](50.1.4.01-mocking.md). Trace the receipt through the real consumer and a rejecting delivery interface. Then distinguish a received HTTP failure from a transport rejection, configured behavior from recorded calls, and wall-clock changes from timer advancement. A fake provider needs its own contract checks; a mock call alone cannot establish delivery.

## Second pass: make the scenario and ownership visible

Read [Test Patterns](50.1.4.02-test-patterns.md). Run the cart cases, then mutate the input and one builder result to explain the copy boundary. Distinguish a factory's fresh data from a fixture's environment and lifecycle. Compare named expected totals with a generated invariant: each detects different defects.

| Chapter | Main question | Read time |
| ------------------------------------------- | --------------------------------------------------------- | --------: |
| [Mocking](50.1.4.01-mocking.md) | What behavior does this replacement let the test observe? | 10 min |
| [Test Patterns](50.1.4.02-test-patterns.md) | Does reuse keep the contract and state ownership visible? | 48 min |

## Revision before interview practice

Complete the [section revision questions](REVISION.md) after both chapters. Change one condition in each example: a provider accepts a request before timing out, a builder stores a nested mutable object, or another worker shares the fixture namespace. Explain which assertion or isolation strategy must change. Continue to the [testing interview bank](../06-interview-prep/50.1.6.01-interview-questions.md) after the remaining testing categories.

## Cross-References

- [Frameworks](../02-frameworks/INDEX.md) — where jest.fn / vi.fn live.
- [Foundations](../01-foundations/INDEX.md) — why boundary mocking follows from test strategy.

---

## Navigation

[← Test Levels](../03-test-levels/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Advanced →](../05-advanced/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) supplies companion artifacts to inspect. Read the current source and its assertions before claiming that a test passed or that a personal project used the same design.

| Topic | Docita evidence |
| --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Clock mock | `apps/api/src/test-utils/fixed-clock.mock.ts` |
| Factories / builders | `apps/api/src/test-utils/factories.ts` |
| Time injection seam (mock at the port, not the call site) | `apps/api/src/shared/common/ports/clock.port.ts` ← `system-clock.service.ts` |
| Guard-level spec example | `apps/api/src/shared/modules/auth/auth/ws-jwt-auth.guard.spec.ts` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
