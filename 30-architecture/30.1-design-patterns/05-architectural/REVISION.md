<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Architectural — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Repository Pattern

Source: [Repository Pattern](30.1.5.01-repository.md)

**Q:** What abstraction should a Repository expose to domain code?

**A:** Operations in the domain's collection or persistence language, rather than every database feature. Avoid wrapping an ORM mechanically without simplifying the dependency.

## CQRS & Dependency Injection

Source: [CQRS & Dependency Injection](30.1.5.02-cqrs-di.md)

**Q:** Does CQRS require separate databases or event sourcing?

**A:** No. Separating command and query models can begin in one process and datastore. Separate stores and event sourcing are additional architectural choices.

## Event Sourcing Pattern

Source: [Event Sourcing Pattern](30.1.5.03-event-sourcing.md)

**Q:** Why are snapshots insufficient to replace the event log in event sourcing?

**A:** Snapshots accelerate reconstruction but do not preserve every historical transition. Their schema and consistency point must remain tied to the authoritative event stream.

## Saga Pattern

Source: [Saga Pattern](30.1.5.04-saga.md)

**Q:** Why is refunding a payment compensation rather than rollback?

**A:** The original charge committed and may have been observed. A refund is a later business transaction with its own failure, timing and audit consequences.

## DDD Tactical Patterns — Aggregates & Value Objects

Source: [DDD Tactical Patterns — Aggregates & Value Objects](30.1.5.05-ddd-tactical-patterns-aggregates-value-objects.md)

**Q:** What should commit together when an aggregate change must emit a domain event?

**A:** The aggregate mutation and durable outbox intent should share the local transaction. Publication then retries, and receivers deduplicate; this does not guarantee immediate delivery.

## Anti-Corruption Layer (ACL)

Source: [Anti-Corruption Layer (ACL)](30.1.5.06-anti-corruption-layer.md)

**Q:** Why should an Anti-Corruption Layer translate meaning as well as field names?

**A:** Its purpose is to protect the local domain model from the external model's assumptions. Renaming fields alone leaves semantic coupling intact.

## Service Locator vs Dependency Injection

Source: [Service Locator vs Dependency Injection](30.1.5.07-service-locator-vs-dependency-injection.md)

**Q:** Why does constructor injection make dependencies easier to inspect than Service Locator?

**A:** The required dependencies appear in the constructor contract. Locator lookups hide them in runtime behavior and can defer missing-dependency errors.

## Presentation Patterns — MVC, MVP, MVVM

Source: [Presentation Patterns — MVC, MVP, MVVM](30.1.5.08-presentation-patterns-mvc-mvp-mvvm.md)

**Q:** How do you distinguish MVP from MVVM by the presentation boundary?

**A:** A Presenter typically directs a view through an interface. A ViewModel exposes presentation state and commands for binding; concrete framework implementations may blend them.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
