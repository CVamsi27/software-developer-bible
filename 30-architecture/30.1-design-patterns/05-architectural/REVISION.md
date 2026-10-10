<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Architectural — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Repository Pattern

Source: [Repository Pattern](30.1.5.01-repository.md)

**Q:** What abstraction should a Repository expose to domain code?

**A:** Expose operations expressed in business terms, such as finding unpaid orders or saving an approved change, rather than every database feature. Merely wrapping an ORM—the tool that maps records to application objects—does not help unless the wrapper simplifies what callers need to know.

**Q:** Trace markPaid when the stored order is pending at version 4.

**A:** The service loads the record, validates pending, and saves paid with expected version 4. An adapter must atomically check 4, persist the change and return an incremented version.

**Q:** What if another writer changes version 4 before save?

**A:** The conditional write conflicts. Reload and reevaluate the domain operation; injection and an in-memory test double do not make the database update atomic.

## CQRS & Dependency Injection

Source: [CQRS & Dependency Injection](30.1.5.02-cqrs-di.md)

**Q:** Does CQRS require separate databases or event sourcing?

**A:** No. Separating command and query models can begin in one process and datastore. Separate stores and event sourcing are additional architectural choices.

**Q:** Trace a rename followed by details when both contracts use one store.

**A:** The command trims and validates the name, then invokes the supplied write adapter. The query invokes the supplied read adapter. The visibility guarantee follows that store and transaction contract.

**Q:** What changes when details uses an asynchronous projection?

**A:** Define write-to-projection propagation, durable progress, duplicates and read-after-write behavior. Return accepted state, use an authoritative read or wait for a known projection version when required.

## Event Sourcing Pattern

Source: [Event Sourcing Pattern](30.1.5.03-event-sourcing.md)

**Q:** Why are snapshots insufficient to replace the event log in event sourcing?

**A:** Snapshots accelerate reconstruction but do not preserve every historical transition. Their schema and consistency point must remain tied to the authoritative event stream.

**Q:** Fold opened, deposited(100), withdrawn(30) in order.

**A:** Opening creates balance 0, deposit produces 100 and withdrawal produces 70. Replay derives state and must not charge or email again.

**Q:** What if two commands loaded stream version N?

**A:** Only an atomic expected-version append can accept the first without losing concurrency evidence. The other reloads and reevaluates; blindly retrying an obsolete accepted decision is unsafe.

## Saga Pattern

Source: [Saga Pattern](30.1.5.04-saga.md)

**Q:** Why is refunding a payment compensation rather than rollback?

**A:** The original charge committed and may have been observed. A refund is a later business transaction with its own failure, timing and audit consequences.

**Q:** Trace flight success followed by a definitive hotel rejection.

**A:** Record hotel rejection, request flight cancellation and record its confirmed result. Failed cancellation stays compensation-pending for retry or reconciliation.

**Q:** What if hotel booking times out instead of rejecting?

**A:** Its outcome is unknown. Reconcile using stable operation identity or the provider idempotency/status contract before treating it as failed; a timeout does not cancel remote work.

## DDD Tactical Patterns — Aggregates & Value Objects

Source: [DDD Tactical Patterns — Aggregates & Value Objects](30.1.5.05-ddd-tactical-patterns-aggregates-value-objects.md)

**Q:** What should commit together when an aggregate change must emit a domain event?

**A:** The aggregate mutation and durable outbox intent should share the local transaction. Publication then retries, and receivers deduplicate; this does not guarantee immediate delivery.

**Q:** Trace USD 250 cents multiplied by 2 and compare USD 500.

**A:** Quantity validation succeeds; construction validates the product 500 as a safe nonnegative integer. Equal amount and currency produce true without requiring object identity.

**Q:** What if two valid order instances modify the same stored version?

**A:** The class invariant is insufficient for concurrent persistence. Use conditional versioning or appropriate transaction locking, and reevaluate conflicts before committing state and outbox intent.

**Q:** Does an ORM relationship from order to customer put the customer inside the order aggregate?

**A:** No. Aggregate membership follows owned lifecycle and immediate invariants, not navigation convenience. A customer can be referenced by identity while its contact details change independently. Persisting or loading a graph does not establish the domain boundary.

**Q:** Which part loads and saves an order, and which part decides whether its lines allow placement?

**A:** The application service coordinates the use case, persistence and outgoing intent. The aggregate owns its line and lifecycle rules; a domain service can own a business rule that does not naturally belong to one object. Remote calls require their own explicit recovery contract.

## Anti-Corruption Layer (ACL)

Source: [Anti-Corruption Layer (ACL)](30.1.5.06-anti-corruption-layer.md)

**Q:** Why should an Anti-Corruption Layer translate meaning as well as field names?

**A:** Its purpose is to protect the local domain model from the external model's assumptions. Renaming fields alone still leaves local code dependent on what those external fields mean and how they behave.

**Q:** Translate CU-000123, spaced Clinic name and status A.

**A:** Validate the identity and name, map A to local active, preserve string 000123, trim Clinic and freeze the flat local record. The mapping assumes the documented illustrative billing meaning.

**Q:** What if status becomes a new code or a second vendor uses CU-000123?

**A:** Reject or deliberately extend the unknown status mapping. Preserve vendor namespace or use an explicit identity map; identical foreign strings do not establish the same local entity.

## Service Locator vs Dependency Injection

Source: [Service Locator vs Dependency Injection](30.1.5.07-service-locator-vs-dependency-injection.md)

**Q:** Why does constructor injection make dependencies easier to inspect than Service Locator?

**A:** The required dependencies appear in the constructor contract. Locator lookups hide them in runtime behavior and can defer missing-dependency errors.

**Q:** Trace the two reports returning count 3.

**A:** LocatedReport requests Orders from its injected registry during run. InjectedReport calls its already supplied Orders. Both can use the same fake and neither needs a global.

**Q:** What if dependency construction is lazy or selection depends on an uploaded format?

**A:** Lazy injection can fail after startup. Runtime format selection can justify a narrow injected registry with explicit unknown-name behavior; do not hide unrelated fixed dependencies in a whole-container lookup.

## Presentation Patterns — MVC, MVP, MVVM

Source: [Presentation Patterns — MVC, MVP, MVVM](30.1.5.08-presentation-patterns-mvc-mvp-mvvm.md)

**Q:** How do you distinguish MVP from MVVM by the presentation boundary?

**A:** A Presenter typically directs a view through an interface. A ViewModel exposes presentation state and commands for binding; concrete framework implementations may blend them.

**Q:** Trace the passive-view presenter with totalCents 1250.

**A:** It reads the model, validates safe nonnegative integer cents, formats USD 12.50 and calls showTotal. The view does not compute the price.

**Q:** What if an earlier asynchronous refresh completes after a newer one?

**A:** Ignore or cancel obsolete results under an explicit request/version policy. Pattern names and bindings alone do not prevent stale presentation; authoritative validation remains outside this screen.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
