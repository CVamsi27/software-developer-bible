<!-- section: Microservices | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Microservices — Data And Consistency Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Saga Pattern

Source: [Saga Pattern](20.6.3.01-saga-pattern.md)

**Q:** How can two-phase commit couple the availability of participants?

**A:** Prepared participants may retain locks while the global outcome is uncertain. Slow or unavailable participants can delay progress; a saga instead exposes local commits with explicit recovery behavior.

**Q:** Why must saga compensation be defined as business behavior?

**A:** A refund or reservation release is a new committed operation, not erasure of earlier history. Some effects are irreversible, and compensation can fail, so model retries, recovery and operator escalation.

**Q:** How do choreography and orchestration expose different coordination costs?

**A:** Choreography distributes reactions across participants; orchestration keeps process state in an explicit coordinator. Both need durable progress, duplicate-safe steps and policies for uncertain outcomes.

**Q:** A payment call times out after inventory was reserved. Why is immediate compensation unsafe?

**A:** The payment may have succeeded without its response arriving. Persist the step identity and unknown outcome, reconcile through the provider's contract and preserve the reservation under a defined expiry policy before deciding to retry or compensate.

**Q:** Can compensation alone prevent two concurrent sagas from overselling stock?

**A:** No. Each local commit can become visible before the saga ends. The inventory service needs an invariant-preserving reservation or atomic conditional mutation; compensation handles failed completion after that boundary.

## Distributed Transactions

Source: [Distributed Transactions](20.6.3.02-distributed-transactions.md)

**Q:** How can a network partition affect consistent reads and transaction progress?

**A:** CAP concerns linearizable consistency and availability during a partition, not atomicity. An atomic commit protocol must additionally prevent participants from making conflicting commit or abort decisions when communication is uncertain.

**Q:** Why can a prepared two-phase-commit participant wait after coordinator failure?

**A:** After voting prepared, a participant cannot safely infer the global decision from a timeout alone. It may need coordinator recovery or another recovery path to learn the durable outcome.

**Q:** When do local transactions and an explicit workflow fit better than global atomic commit?

**A:** Use local transactions and a saga when business rules permit intermediate states and compensation. Choose an atomic commit protocol only when its participant support, blocking and recovery costs fit the required invariant.

**Q:** Does a shared two-phase-commit outcome alone establish global serializable isolation?

**A:** No. Atomic commit coordinates the commit/abort decision. Participant isolation, protocol integration and concurrent reads determine the separate isolation/visibility contract; prepared-state recovery also affects availability.

## Event Sourcing

Source: [Event Sourcing](20.6.3.03-event-sourcing.md)

**Q:** What does making events authoritative change about stored state?

**A:** Accepted events become the authoritative history; state is a derived result of applying them. Reconstruction depends on complete permitted history and deterministic interpretation, not simply on using a broker.

**Q:** How can replay support a new read model or recovery?

**A:** A new projection can consume retained events to build a different view, and recovery can replay from a compatible snapshot. Keep historical effects disabled or idempotent when replaying.

**Q:** Which read, schema-evolution and retention costs does event sourcing introduce?

**A:** Queries often need projections or snapshots, and historical schemas need interpretation rules. Define correction, erasure and retention policy; an immutable append convention does not remove these obligations.

## CQRS (Command Query Responsibility Segregation)

Source: [CQRS (Command Query Responsibility Segregation)](20.6.3.04-cqrs.md)

**Q:** When do read and write workloads justify distinct models?

**A:** Separate models help when enforcing write invariants and serving read shapes require materially different structures. They can still live in one process and database; separation is not automatically a performance win.

**Q:** How does projection synchronization determine read freshness?

**A:** Asynchronous projection creates a lag window, while a synchronous design can have different freshness. Define read-your-writes behavior and monitor or expose projection progress.

**Q:** What scaling benefits and operational costs can CQRS introduce?

**A:** Read and write capacity can evolve independently when the architecture separates them. The costs include extra models, synchronization, duplicate handling and operational evidence for freshness.

## Decomposing the Monolith Database

Source: [Decomposing the Monolith Database](20.6.3.05-decomposing-monolith-database.md)

**Q:** How does a shared schema couple service releases and availability?

**A:** Shared tables and migrations expose multiple services to schema and transaction changes. Clear data ownership reduces that coupling; independent APIs can still recreate it if ownership remains ambiguous.

**Q:** Why should database decomposition examine data ownership and access paths?

**A:** Identify authoritative writers, invariants, queries and reports before choosing boundaries. An entity's name alone does not reveal whether moving it breaks a cross-table transaction.

**Q:** Why must the migration's intermediate state be designed explicitly?

**A:** Old and new paths can coexist with different schema and ownership rules. Plan synchronization, validation and rollback through that period rather than treating the final diagram as the whole migration.

## Transactional Outbox Pattern

Source: [Transactional Outbox Pattern](20.6.3.06-transactional-outbox.md)

**Q:** What failure gap exists between a database commit and a broker publish?

**A:** A process can crash after committing business data but before publishing its event, or publish data whose database commit later fails. Separate local and broker writes do not share atomicity merely because they are adjacent.

**Q:** How does recording an event intent with business data close that gap?

**A:** Commit the event intent with the business mutation, then recover publication through a relay. Delivery depends on relay recovery and broker availability; an uncertain acknowledgment can still create duplicates.

**Q:** Which ordering and relay-lag requirements remain after adding an outbox?

**A:** Monitor oldest pending work and relay failure. Preserve required per-aggregate order through relay and partition design, and retain identity so duplicate deliveries can be processed safely.

**Q:** An email succeeds, then the consumer crashes before writing its cache marker. What does retry risk?

**A:** The message can be sent again. A cache lookup and marker do not share a transaction with an external provider. Reuse a provider-supported idempotency key within its retention contract, reconcile uncertain results when possible, or document the remaining duplicate risk.

**Q:** Why must a processed-event marker and a database projection update commit together?

**A:** A marker committed before a failed update can make the retry skip missing work. Keep both in one transaction, verify the intended mutation happened and roll back the marker on failure. A unique consumer/event identity prevents repeated effects for that consumer.

## Replay, projection and migration failure cases

Sources: [event sourcing](20.6.3.03-event-sourcing.md), [CQRS](20.6.3.04-cqrs.md), [database decomposition](20.6.3.05-decomposing-monolith-database.md).

**Q:** Two commands read stream version four. Why must append check that version atomically?

**A:** Both may have passed an invariant against the same old state. One successful append changes that state; the other must reload and re-evaluate instead of accepting its stale decision.

**Q:** Why is a snapshot of version ten labeled version twelve unsafe?

**A:** Replay starts after twelve and skips accepted changes eleven and twelve. Snapshot state and its exact source version must belong together.

**Q:** Can a full-state projection accept version twelve after version ten without seeing eleven?

**A:** It can under a validated complete-state contract. A delta consumer cannot generally skip eleven because its missing operation may change the result.

**Q:** Why must a lagging payment view not trigger another charge?

**A:** Read-model lag is not evidence of rejected payment. Query authoritative status or reconcile the original stable operation identity before deciding on another effect.

**Q:** Why is a PostgreSQL LSN not sufficient as a unique changed-row identity?

**A:** Multiple changes can share a source position. Use the connector's full transaction/record identity and order contract, with atomic target mutation and progress.

**Q:** Why must a deletion tombstone survive an older snapshot record?

**A:** Dropping deletion ordering allows the stale snapshot to recreate the row. A version/order-aware target must reject that older record and retain appropriate tombstone/checkpoint history.

## Summary

Use these prompts after the reading pass to recall the data and consistency mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for history, projections and distributed recovery

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
