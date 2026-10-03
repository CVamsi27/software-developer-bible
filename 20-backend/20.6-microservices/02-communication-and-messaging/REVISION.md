<!-- section: Microservices | category: Reference | tags: revision| general-importance: important| general-importance: important | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Microservices — Communication And Messaging Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## gRPC

Source: [gRPC](20.6.2.01-grpc.md)

**Q:** What core constraint explains why http/2 gives multiplexing governs grpc?

**A:** many concurrent calls on one connection — no head-of-line blocking at the HTTP layer, bidirectional streaming as a first-class citizen. The transport enables the API shape.

**Q:** What core constraint explains why protobuf gives the contract governs grpc?

**A:** schemas typed, versioned, and code-generated for every language — with binary encoding an order of magnitude smaller than JSON. The contract-first discipline  with a binary wire format.

**Q:** What core constraint explains why the trade is browser ubiquity. governs grpc?

**A:** Browsers speak JSON natively; gRPC-Web exists but adds a translation layer. So gRPC wins east-west (service-to-service) and loses north-south (public APIs) — knowing *which edge* you're designing is the whole decision.

## gRPC Streaming

Source: [gRPC Streaming](20.6.2.02-grpc-streaming.md)

**Q:** What core constraint explains why three shapes cover all flows governs grpc streaming?

**A:** server-streaming (one request, many responses — feeds, logs), client-streaming (many requests, one answer — uploads, metrics batches), bidirectional (chat, live sync). Each is the response to a real interaction shape that unary RPC models awkwardly.

**Q:** What core constraint explains why streams are long-lived connections, so backpressure and lifecycle matter governs grpc streaming?

**A:** flow control (HTTP/2 window), cancellation (context propagation — the client hanging up must cancel server work), and reconnect-with-resume are part of the contract, not edge cases.

**Q:** What core constraint explains why the failure mode is the forgotten close governs grpc streaming?

**A:** streams leak connections when neither side terminates — every streaming handler needs cancellation deadlines and explicit completion, the same resource-lifetime discipline as file handles .

## Apache Kafka

Source: [Apache Kafka](20.6.2.03-kafka.md)

**Q:** What core constraint explains why an append-only log is the cheapest durable write governs apache kafka?

**A:** (sequential disk I/O) and the cheapest replay (seek to offset). Everything Kafka offers — durability, replay, multiple independent consumers — is a property of append-only + offsets.

**Q:** What core constraint explains why consumer groups solve scale-out with ordering governs apache kafka?

**A:** partitions divide the log; a group's members each own partitions exclusively — parallelism with per-partition order preserved. The trade: ordering exists *within* a partition only, so partition-key design is application architecture.

**Q:** What core constraint explains why retention replaces the queue's delete-after-consume. governs apache kafka?

**A:** Messages persist (days/forever), so new consumers can replay history and multiple groups read the same events independently — Kafka is an event *database*, not a message queue, and the difference is architectural.

## RabbitMQ

Source: [RabbitMQ](20.6.2.04-rabbitmq.md)

**Q:** What core constraint explains why the exchange is the router. governs rabbitmq?

**A:** Direct (by key), topic (by pattern), fanout (broadcast), headers (by metadata) — producers publish to exchanges, not queues; binding rules decide delivery. This is publish-subscribe as a first-class routing engine, which Kafka deliberately is not.

**Q:** What core constraint explains why acknowledgment semantics are the reliability story. governs rabbitmq?

**A:** Unacked messages redeliver (at-least-once — consumers must be idempotent, → 20.3.3.05); DLX captures the repeatedly-failed; quorum queues replicate. Each is an answer to "what happens when a consumer dies mid-task?".

**Q:** What core constraint explains why task queues are its native shape governs rabbitmq?

**A:** work distribution with per-message ack, priority, and TTL — the opposite trade from Kafka's broadcast log. Choosing between them is "route discrete jobs" vs "broadcast events for many consumers.".

## Message Brokers: Kafka vs RabbitMQ

Source: [Message Brokers: Kafka vs RabbitMQ](20.6.2.05-message-brokers.md)

**Q:** What core constraint explains why a synchronous call fails when either side fails. governs message brokers: kafka vs rabbitmq?

**A:** The broker is the buffer between lifecycles: producer succeeds if the *broker* accepts, consumer processes when *it* can — availability decouples, at the price of eventual processing and new failure modes (broker down, lag, poison messages).

**Q:** What core constraint explains why delivery semantics are the contract governs message brokers: kafka vs rabbitmq?

**A:** at-most-once (fire and forget), at-least-once (acks + redelivery — duplicates possible, consumers must dedupe), exactly-once (transactional + idempotency end-to-end — the expensive, often-unnecessary one). Every queue technology is a point in this space; every consumer design starts by picking it.

**Q:** What core constraint explains why ordering and duplication fight each other governs message brokers: kafka vs rabbitmq?

**A:** exactly-once ordering requires single-partition serialization; global ordering kills parallelism. Real designs choose per-domain: money flows get ordering + idempotency; telemetry gets at-most-once.

## Event-Driven Architecture — Kafka, Event Sourcing, CQRS

Source: [Event-Driven Architecture — Kafka, Event Sourcing, CQRS](20.6.2.06-event-driven-architecture.md)

**Q:** What core constraint explains why the producer cannot know its consumers. governs event-driven architecture — kafka, event sourcing, cqrs?

**A:** "OrderPlaced" is a fact; email, inventory, analytics, fraud each react independently — adding a consumer requires *zero producer change*. That decoupling is the entire value and the reason events are past-tense facts, not commands.

**Q:** What core constraint explains why event-carried state transfer vs notifications is the data design governs event-driven architecture — kafka, event sourcing, cqrs?

**A:** fat events (all data, consumers independent of the source DB) vs thin events (ID + consumers call back — coupling returns). The choice governs how much coupling the architecture actually removed.

**Q:** What core constraint explains why the costs are structural governs event-driven architecture — kafka, event sourcing, cqrs?

**A:** eventual consistency everywhere (the UI must show "processing"), harder debugging (no single request trace — hence correlation IDs and event lineage), and schema evolution as a first-class discipline (consumers outlive producer versions).

## Summary

Use these prompts after the reading pass to recall the communication and messaging mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
