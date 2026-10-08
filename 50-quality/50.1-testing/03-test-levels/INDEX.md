# Test Levels

> **Study time:** ≈ 33 min of reading (4 files, ~8 min average).
> **4 files.** The test pyramid in practice: unit, integration, and E2E — what to test at each level, which tools, and how much confidence each layer buys.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Start With a Booking That Must Survive Reloading

A booking can fail inside a calculation, at the database boundary, or while the browser carries an authenticated request. Use the three chapters to decide which observation locates each failure. Test shape follows the risk and feedback cost; a fixed percentage of each level cannot establish coverage.

## Pass 1 — Make the Rule Deterministic

[Unit Testing](50.1.3.01-unit-testing.md) isolates the behavior you own. Learn to control external boundaries while asserting inputs, outputs and failure effects. Keep internal helper-call details out of the contract unless that interaction is itself required.

## Pass 2 — Exercise the Connection That Can Break

[Integration Testing](50.1.3.02-integration-testing.md) checks selected connections between components: HTTP routing, conversion of values into request or response formats (serialization), database constraints or provider protocols. State which components are real. A mocked payment response cannot verify a provider; an API test transaction cannot roll back writes made through an unrelated connection.

## Pass 3 — Observe the User's Consequence

[E2E Testing](50.1.3.03-e2e-testing.md) follows a browser action through the declared application boundary. Trace a write and subsequent reload/read, then force an error to verify recovery. Learn why browser-context isolation does not reset server data and why traces/auth files need restricted handling.

## Compare the Observation Before Choosing a Tool

| Risk | Useful observation | Why another layer may miss it |
| ------------------------------------------ | -------------------------------------------- | ------------------------------------------------ |
| Incorrect conflict calculation | Deterministic business-rule result | A browser journey may never hit that branch |
| Two concurrent bookings claim one slot | Real database constraint/transaction outcome | Separate mocked calls do not exercise the race |
| Cookie or route breaks the booking journey | Authorized browser write and subsequent read | A direct handler test can bypass the broken path |

Runner and component-library choices are explained in [Frameworks](../02-frameworks/INDEX.md). Load and failure experiments extend these checks in [Advanced](../05-advanced/INDEX.md); they are separate dimensions rather than a higher confidence tier.

## Finish With Revision, Then Interview Practice

Close the chapters and work through [section revision questions](REVISION.md). Return to the mechanism that you could not explain, then use the separate [testing interview bank](../06-interview-prep/50.1.6.01-interview-questions.md).

## Apply the Flow to a Real Repository

Locate one pure rule, one real database/API seam, and one browser journey in the application you work on. Inspect their setup, isolation, failure assertions and current run evidence. File names or a historical suite count do not establish what the tests verify.

## Navigation

[← Frameworks](../02-frameworks/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Mocking & Patterns →](../04-mocking-and-patterns/INDEX.md)
