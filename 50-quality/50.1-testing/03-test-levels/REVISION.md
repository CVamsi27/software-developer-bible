<!-- section: Testing | category: Reference | tags: revision, practice| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Testing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Testing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Unit Testing

Source: [Unit Testing](50.1.3.01-unit-testing.md)

**Q:** When is mocking an internal helper counterproductive?

**A:** When the assertion depends on a helper-call sequence instead of the unit's contract. Mock an external boundary when control or isolation is necessary, and exercise real internal behavior.

## Integration Testing

Source: [Integration Testing](50.1.3.02-integration-testing.md)

**Q:** Why can a transaction rollback fail to isolate an API integration test?

**A:** The API may use a different database connection/transaction. Isolation must encompass the application's writes through a test schema/database, injected transaction, or reliable cleanup strategy.

**Q:** What does a mocked external service leave unverified?

**A:** The real service's protocol, authorization, schema, timing, and failure behavior. Pair controlled doubles with targeted contract or sandbox integration evidence.

**Q:** Why does a preliminary free-slot read fail to prevent two bookings?

**A:** Both callers can observe absence before either writes. The database constraint or supported atomic transaction protocol must arbitrate the write; verify competing requests and the durable winner.

**Q:** Why can a SQL fake return success while the real API returns an error?

**A:** It can ignore column mapping, driver types, uniqueness or transaction semantics. Exercise the actual query/constraint through the database boundary and observe stored state.

**Q:** When is TRUNCATE acceptable test cleanup?

**A:** When the test fixture exclusively owns the affected database/tables and no concurrent test or consumer can write there. Shared parallel suites need isolated namespaces or another supported strategy.

## E2E Testing

Source: [E2E Testing](50.1.3.03-e2e-testing.md)

**Q:** What should a critical browser journey assert beyond a successful click?

**A:** The intended observable outcome, such as a persisted order, confirmation state, or authorized access. Automatic waiting finds actionable elements; it does not prove the business effect succeeded.

**Q:** Why avoid a fixed sleep before asserting?

**A:** It waits too long when the condition is ready and too little when delayed. Wait on the actual observable state with a bounded deadline.

**Q:** Why does registering waitForResponse after clicking create an intermittent failure?

**A:** A fast response can arrive before the observer exists. Register the observer before the triggering action, then await both the action and the intended response/outcome.

**Q:** What does the intercepted 503 note test establish, and what does it leave unverified?

**A:** It establishes that the UI keeps the entered title, shows failure and does not invent a saved note for that controlled browser response. It does not establish the real backend's failure protocol or persistence behavior.

**Q:** Why are random note titles insufficient isolation?

**A:** They avoid name collisions, but tests can still share account, tenant, quotas or server records. Scope fixtures and clean up after failure/retry as well as success.

**Q:** Why should storageState and traces have stricter handling than ordinary test reports?

**A:** Auth state may permit account impersonation, and traces can capture credentials or private response content. Use synthetic identities, exclude auth files from version control/general uploads, and restrict artifact access and retention.

## Summary

Choose the narrowest boundary that reveals the failure, then cross the necessary real seams. Separate browser state from server data and controlled-response evidence from provider compatibility.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
