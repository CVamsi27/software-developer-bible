<!-- section: Testing | category: Reference | tags: revision, practi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Testing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Testing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Jest

Source: [Jest](50.1.2.01-jest.md)

**Q:** Why does a mock reset differ from clearing calls?

**A:** Clearing removes recorded calls/results; resetting also resets mock implementations according to the installed runner/version; restoring returns a spy/replaced property to its original implementation. Choose the needed isolation deliberately.

**Q:** Does `jest.mocked(fetch)` replace the global fetch implementation after mocking an unrelated API module?

**A:** No. It is a typing helper. Create a real mock or spy at the intended boundary; mocking a different module does not replace the global.

**Q:** Can isolated test files safely clear the same database in parallel?

**A:** No. The runtime sandbox does not isolate external data. Use separate databases/schemas or correctly scoped transactions and account for all workers.

## Vitest

Source: [Vitest](50.1.2.02-vitest.md)

**Q:** Why should a Jest-to-Vitest migration rerun behavior tests instead of only renaming globals?

**A:** Frameworks can differ in when they register mocks, how they locate imported modules, whether tests share state, how simulated timers and snapshots work, and which environment they use by default. Similar APIs do not guarantee that tests execute the same way.

**Q:** Does transforming a TypeScript test establish type safety?

**A:** No. Run a checker or supported type-test workflow separately; successful runtime tests do not validate every static type relationship.

**Q:** Why does an MSW handler that always returns success fail to establish the client's header contract?

**A:** Interception preserves the constructed request, but the handler or test must assert the expected header/body. Otherwise a malformed request can still receive the canned successful response.

**Q:** Can jsdom or happy-dom establish the same result as Vitest Browser Mode or a Next.js async Server Component E2E test?

**A:** No. DOM emulators implement a subset of browser behavior. Browser Mode supplies a configured real browser, while async Server Component routing/rendering needs the framework runtime; Next.js currently recommends E2E for that boundary.

## React Testing Library

Source: [React Testing Library](50.1.2.03-react-testing-library.md)

**Q:** Why prefer a role-and-name query to a CSS selector?

**A:** It checks the interface users and assistive technology can identify while reducing coupling to markup structure. It still cannot prove all accessibility requirements.

**Q:** Why does `waitFor(() => false)` not wait for the intended condition?

**A:** The callback retries when it throws. Returning false or running an empty callback can complete immediately. Put an assertion in the callback and keep user actions outside it.

**Q:** Why use `queryByRole` to assert an element is absent?

**A:** It returns null when there is no match. `getByRole` throws on absence before a negated matcher can evaluate.

## Testing Frameworks Comparison

Source: [Testing Frameworks Comparison](50.1.2.04-testing-frameworks-comparison.md)

**Q:** Why can one application reasonably use more than one testing tool?

**A:** Node unit tests, real dependency integration, and cross-browser interactions have different execution/observation requirements. Choose tools per boundary rather than making one framework cover everything.

**Q:** Does booking the same slot twice in sequence establish race safety?

**A:** No. It checks an existing-conflict path. Race safety needs overlapping operations against the real persistence constraint/transaction and an assertion on the durable invariant.

## Summary

Check which runtime, dependency and observation each test actually reaches. Reproduce the pending/error cases, then explain where integration or browser evidence is still required.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
