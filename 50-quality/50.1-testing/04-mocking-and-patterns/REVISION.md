<!-- section: Testing | category: Reference | tags: revision, practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Testing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Testing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Mocking

Source: [Mocking](50.1.4.01-mocking.md)

**Q:** Why does a network-level mock often provide more confidence than mocking a fetch wrapper?

**A:** The application still converts data into the request format, constructs requests, handles responses, and runs its error paths. The real external service remains outside that test's scope.

**Q:** Why can a permissive mock hide a broken request?

**A:** It may answer even when the method, URL, payload, or headers are wrong. Match the contract and make unexpected requests fail clearly.

**Q:** Why can clearing a mock's call history still leave a test-order dependency?

**A:** It preserves configured behavior. A previous return/rejection or mutable fake state can still affect the next test; reset the intended behavior or construct a fresh double and reset separate data.

**Q:** In current Vitest, does restoring all spied methods also erase the calls retained on a spy variable?

**A:** No. `vi.restoreAllMocks()` restores the original methods but retains that spy's history and mock implementation. Individual `mockRestore()` has a different contract. Choose explicit clearing or fresh doubles when history isolation is required.

**Q:** How do an HTTP 500 and HttpResponse.error exercise different client paths?

**A:** A 500 is a received response whose status the client must inspect; HttpResponse.error causes a transport rejection handled through the promise error path. One cannot stand in for both.

**Q:** Why is checking a password starts with hashed_ insufficient?

**A:** A fake string prefix can satisfy the assertion without a supported hash. Verify the stored value using the real password verifier and assert that plaintext was not stored.

**Q:** Does setting a fake wall clock run a delayed callback?

**A:** No. Wall-clock control and timer advancement are separate operations. Advance the supported timer clock to trigger callbacks, and await promise work as required.

## Test Patterns

Source: [Test Patterns](50.1.4.02-test-patterns.md)

**Q:** How does a factory improve a test's reading flow?

**A:** It creates fresh data with explicit defaults while the test overrides facts relevant to the scenario. Defaults must stay visible when they affect the result; rejection tests may deliberately create invalid input. The assertion can then focus on behavior without a large setup block.

**Q:** When does a shared fixture become a liability?

**A:** When unrelated tests depend on its evolving mutable state or hidden setup. Use explicit scenario inputs and fresh data; for external resources, also give each test an isolated namespace and a cleanup owner.

**Q:** Why name a parameterized case rather than only listing input values?

**A:** The name states the invariant or edge condition being tested, making a failure understandable without reverse-engineering the dataset.

**Q:** Why does the cart builder copy both when adding a line and when building a result?

**A:** The first copy prevents a caller's later mutation from changing the stored line. The second prevents a returned result from changing future results. That contract holds here because all fields are primitives; nested mutable fields need a separate ownership or copying rule.

**Q:** Can the cart's reordering property establish that every total is correctly priced?

**A:** No. An implementation that always returns zero also preserves totals under reordering. Independent expected-value cases check the pricing rule; generated cases search the stated input domain for violations of a relationship.

**Q:** Why does a shared fixture need more than an afterEach cleanup hook?

**A:** Concurrent tests can see or delete each other's state before cleanup. Namespace resources by ownership, await setup and cleanup, and account for a runner that dies before hooks execute.

**Q:** When can two assertions still describe one behavior?

**A:** A rejected action can have both a required error and a required unchanged state. Those observations define one failure contract; splitting them can conceal forbidden mutation.

**Q:** What does a passing DOM snapshot fail to establish?

**A:** It checks the reviewed serialized structure. It does not establish layout, keyboard behavior, screen-reader output or the correctness of an unreviewed update.

## Summary

Control the smallest useful boundary and exercise the real consumer. Keep the double’s configured behavior, timer state and separate fixture data explicit so a passing result supports only the intended claim.

## See Also

- [Section learning flow](INDEX.md) — revisit owned fixtures and observable oracles before substituting dependencies

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
