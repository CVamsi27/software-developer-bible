<!-- section: Microservices | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)

# Microservices — Data And Consistency Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Saga Pattern

Source: [Saga Pattern](20.6.3.01-saga-pattern.md)

**Q:** What core constraint explains why two-phase commit across services couples availability and blocks on the slowest participant. governs saga pattern?

**A:** A coordinator holding locks while a service is down = systemic stall. So: no distributed ACID. The saga replaces it with *sequenced local transactions* — each service commits its own piece.

**Q:** What core constraint explains why compensation is the price of no rollback. governs saga pattern?

**A:** Step 4 failing means steps 1–3 must be *semantically* undone (refund, release inventory) — compensation transactions, which are business logic and cannot be automatic. Every saga is a state machine with a compensation arc per step.

**Q:** What core constraint explains why coordination is choreography vs orchestration governs saga pattern?

**A:** events + each service reacts (decoupled, flow invisible) vs a central orchestrator holding the state machine (visible, one more failure point). Either way, the design work is the same: enumerate every failure point and its compensation. Idempotency  is assumed throughout, because retries are certain.

## Distributed Transactions

Source: [Distributed Transactions](20.6.3.02-distributed-transactions.md)

**Q:** What core constraint explains why you cannot have atomicity, availability, and partition-tolerance at once (cap). governs distributed transactions?

**A:** Network partitions are physical reality; so every distributed "transaction" chooses: block (2PC: consistent, unavailable during partition) or proceed and reconcile (eventual consistency).

**Q:** What core constraint explains why 2pc's blocking is the lesson, not a flaw governs distributed transactions?

**A:** a coordinator crash between prepare and commit leaves participants locked — the protocol proves *why* the industry moved to coordination-via-compensation (sagas, → 20.6.3.01) instead of locking across services.

**Q:** What core constraint explains why the modern answer: keep acid local, make the workflow explicit. governs distributed transactions?

**A:** One DB transaction per service, sagas across services, outbox for reliable publishing  — the composition gives you *observable* eventual consistency instead of *invisible* blocking.

## Event Sourcing

Source: [Event Sourcing](20.6.3.03-event-sourcing.md)

**Q:** What core constraint explains why state is derived; events are permanent. governs event sourcing?

**A:** A bank balance is the *sum* of its transactions — store the transactions, compute the state. Lose the ability to reconstruct state and you've lost audit, time travel, and debugging in one blow; store events and all three are free.

**Q:** What core constraint explains why replay is the superpower governs event sourcing?

**A:** rebuild state, build new read models from history, debug by replaying production into staging. The same property Kafka exploits , applied to your domain data.

**Q:** What core constraint explains why the costs are the reads and the evolution governs event sourcing?

**A:** nothing is mutable — every read is a projection (snapshots are the optimization), and event *schemas are forever* (upcasting old events is the discipline). Event sourcing is a decision to be made per-domain for audit/replay needs, never as a default architecture.

## CQRS (Command Query Responsibility Segregation)

Source: [CQRS (Command Query Responsibility Segregation)](20.6.3.04-cqrs.md)

**Q:** What core constraint explains why writes normalize for invariants; reads denormalize for queries. governs cqrs (command query responsibility segregation)?

**A:** One model cannot optimize both , so split them and let each be shaped for its job — write to Postgres, project to Elasticsearch, cache, whatever the query needs.

**Q:** What core constraint explains why the sync mechanism is the architecture governs cqrs (command query responsibility segregation)?

**A:** events from the write side project into read models  — which makes read staleness structural. Product decisions must tolerate "paid but not yet visible.".

**Q:** What core constraint explains why the payoff compounds with scale governs cqrs (command query responsibility segregation)?

**A:** read models scale independently (add replicas, caches, per-query stores), write model stays lean and transactional. The cost: two models to maintain, projection lag to monitor, and idempotent projections as a hard requirement.

## Decomposing the Monolith Database

Source: [Decomposing the Monolith Database](20.6.3.05-decomposing-monolith-database.md)

**Q:** What core constraint explains why shared schema = shared fate. governs decomposing the monolith database?

**A:** Two services joining the same tables change-lock each other; releases, scaling, and even uptime couple. Decomposition's real work is finding *data boundaries* (bounded contexts), because service boundaries drawn without them reunify in the dark (crawling joins via APIs).

**Q:** What core constraint explains why extract along read/write paths, not entity names. governs decomposing the monolith database?

**A:** "Order service" fails when Checkout and Fulfillment need wildly different shapes and scales of the same data — the split follows who *writes* what and who *reads* what (CQRS lens, → 20.6.3.04).

**Q:** What core constraint explains why the intermediate state is the design governs decomposing the monolith database?

**A:** shared DB while code decouples (modular monolith), then per-service schemas with outbox-driven sync  — never a weekend cutover, always a strangler  timeline.

## Transactional Outbox Pattern

Source: [Transactional Outbox Pattern](20.6.3.06-transactional-outbox.md)

**Q:** What core constraint explains why two systems cannot share one transaction. governs transactional outbox pattern?

**A:** Commit the DB then publish = publish may be lost on crash; publish then commit = events about uncommitted data. Both orders are wrong because the broker isn't transactional .

**Q:** What core constraint explains why so make the event a row in the same db transaction. governs transactional outbox pattern?

**A:** The outbox table commits atomically with the business change — then a relay publishes outbox rows (poll or CDC/Debezium) and marks them sent. At-least-once delivery is guaranteed; consumers dedupe . Atomicity achieved by *renaming the problem*: one transaction, one system.

**Q:** What core constraint explains why ordering and lag are the operational care-abouts governs transactional outbox pattern?

**A:** relay lag = downstream staleness; per-aggregate ordering needs partition-aware relay design. The pattern is now the *default* answer for event publishing — anything else is accepting silent event loss.

## Summary

Use these prompts after the reading pass to recall the data and consistency mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
