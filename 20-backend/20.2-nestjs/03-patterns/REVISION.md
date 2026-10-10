<!-- section: NestJS | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-NestJS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# NestJS — Patterns Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## CQRS in NestJS

Source: [CQRS in NestJS](20.2.3.01-cqrs.md)

**Q:** Why might reads and writes need different data models?

**A:** Writes care about invariants and transactions; reads care about denormalized, query-friendly views. Forcing both through one model produces either slow reads or awkward writes.

**Q:** How does a command differ from a query?

**A:** The naming split is the discipline: `UpdateOrderStatus` (command, requests a change, may fail) vs `GetOrder` (query, side-effect-free). The distinction makes audit, validation, and authorization per-intent rather than per-CRUD-verb.

**Q:** When can a separate read model return older data, and when is that acceptable?

**A:** An asynchronously updated projection can lag behind a committed write. Dashboards may tolerate this, but a reservation confirmation may need the authoritative result or a version barrier. Separate storage is optional.

## NestJS Microservices

Source: [NestJS Microservices](20.2.3.02-microservices.md)

**Q:** Why should transport handlers delegate business rules to shared services?

**A:** The controller abstraction extends to message patterns — `@EventPattern` handlers are controllers for the message transport, keeping business logic transport-agnostic.

**Q:** Which delivery behavior should be checked before choosing a Nest transport?

**A:** TCP (request/response), Redis pub/sub, NATS, Kafka (at-least-once with consumer groups), gRPC (typed streaming). Each carries the same handler contract but different guarantees — the same delivery-semantics questions as webhooks and Redis streams.

**Q:** What connection and failure responsibilities does ClientProxy introduce?

**A:** The client owns connection setup/cleanup, subscriptions, serialization and deadlines. HTTP clients also need failure and retry policies; neither protocol knows whether a timed-out write committed.

## Dispatch and delivery boundaries

Sources: [CQRS](20.2.3.01-cqrs.md), [Microservices](20.2.3.02-microservices.md)

**Q:** Does a successful command require the query handler to read a different database?

**A:** No. Separate interfaces can share a database. Another read store adds projection lag and recovery work.

**Q:** A command commits, then the process stops before publication. What preserves the downstream update?

**A:** A transactional outbox record written with the change. A relay publishes it and the consumer handles duplicates.

**Q:** Why should payment success trigger an email instead of emitting payment and email commands together?

**A:** Emitting commands together does not establish completion order. The email depends on the accepted payment fact and durable workflow progress.

**Q:** Why does constructing `client.send(...)` without a subscription send nothing?

**A:** Its Observable is cold. Subscribe directly or use `firstValueFrom`, with a bounded deadline.

**Q:** Can Redis persistence recover a Nest pub/sub event missed by an offline subscriber?

**A:** No. This transport uses pub/sub, not a durable backlog for that subscriber.

**Q:** The client times out after a reservation commits. What should a retry preserve?

**A:** The same operation identity and reconciliation contract; a new identity could create a second effect.

## Summary

Use these prompts after the reading pass to recall the patterns mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for module boundaries and durable work

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
