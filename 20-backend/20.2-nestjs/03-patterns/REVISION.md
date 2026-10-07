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

**A:** Writes care about invariants and transactions; reads care about denormalized, query-friendly views. Forcing both through one model produces either slow reads or awkward writes .

**Q:** How does a command differ from a query?

**A:** The naming split is the discipline: `UpdateOrderStatus` (command, handled once, may fail) vs `GetOrder` (query, side-effect-free). The distinction makes audit, validation, and authorization per-intent rather than per-CRUD-verb.

**Q:** When can a separate read model return older data, and when is that acceptable?

**A:** — acceptable when read staleness of seconds is tolerable (dashboards, search), overkill for simple CRUD. CQRS is a scaling decision, not a fashion.

## NestJS Microservices

Source: [NestJS Microservices](20.2.3.02-microservices.md)

**Q:** Why should transport handlers delegate business rules to shared services?

**A:** The controller abstraction extends to message patterns — `@EventPattern` handlers are controllers for the message transport, keeping business logic transport-agnostic .

**Q:** Which delivery behavior should be checked before choosing a Nest transport?

**A:** TCP (request/response), Redis pub/sub, NATS, Kafka (at-least-once with consumer groups), gRPC (typed streaming). Each carries the same handler contract but different guarantees — the same delivery-semantics questions as webhooks  and Redis streams .

**Q:** What connection and failure responsibilities does ClientProxy introduce?

**A:** cross-transport calls lose HTTP's ubiquity — no browser, no curl. The client (`ClientProxy`) must handle connection lifecycle, serialization, and retries that HTTP got free.

## Summary

Use these prompts after the reading pass to recall the patterns mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
