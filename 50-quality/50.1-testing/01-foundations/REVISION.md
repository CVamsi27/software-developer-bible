<!-- section: Testing | category: Reference | tags: revision, practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Testing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Testing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Testing Overview

Source: [Testing Overview](50.1.1.01-testing-overview.md)

**Q:** Why is a passing suite not proof that production behavior is correct?

**A:** Tests sample scenarios under specific environments and assertions. Missing cases, unrealistic doubles, and deployment differences can leave defects unobserved.

**Q:** What should determine the mix of unit, integration, and E2E tests?

**A:** The cost and failure risk of the behavior being verified. Fast units and real boundary tests complement a small set of critical browser journeys; a fixed percentage is not universal.

**Q:** What makes an assertion valuable when refactoring?

**A:** It checks the required observable outcome or contract while allowing valid internal changes. Mirroring implementation steps makes the test change with the code rather than detect a defect.

**Q:** A browser test intercepts the order API and returns a success fixture. Does it verify that a real order was committed?

**A:** It verifies the UI against the supplied response. To verify persistence, exercise the real handler and database, then assert the stored order and inventory invariant. State external substitutions separately.

**Q:** A price function executes every line during tests but returns 502 for two items at 500 cents. What is missing?

**A:** A useful oracle or assertion. Coverage shows execution, not correctness. An independently chosen expected result of 1,000 detects the defect.

## Test Data Management & Anonymization

Source: [Test Data Management & Anonymization](50.1.1.02-test-data-management-anonymization.md)

**Q:** Why is replacing names with repeatable tokens usually pseudonymization?

**A:** Stable tokens can preserve linkage, and a mapping/key may permit re-identification. Removing obvious identifiers does not prove the remaining data is anonymous.

**Q:** Why can a seeded data factory still be nondeterministic?

**A:** Uncontrolled clocks, randomness outside the seeded source, IDs, concurrency, and external data can vary. Control all inputs relevant to the assertion.

**Q:** Why does preserving customer/order joins with HMAC tokens not make an export anonymous?

**A:** The same input and key preserve stable linkage. A key holder can recompute tokens from candidate IDs, and other fields may identify someone without the key. The transformation also leaves dates and event histories untouched.

**Q:** What changes when a generator uses a fixed seed but generates dates relative to today?

**A:** Replaying on another day changes the date range. Fix the reference date as well as the seed, and pin the generator version and call order. Isolate concurrent generator state.

**Q:** What does a golden dataset checksum establish, and what does it leave unanswered?

**A:** Comparing against an independently recorded digest can detect changed bytes. It cannot establish that expected outputs express the correct business rule; review those outputs separately.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
