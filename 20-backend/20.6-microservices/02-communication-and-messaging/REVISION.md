<!-- section: Microservices | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Microservices — Communication And Messaging Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## gRPC

Source: [gRPC](20.6.2.01-grpc.md)

**Q:** How does HTTP/2 multiplex concurrent gRPC calls?

**A:** HTTP/2 carries independent streams over one connection. It avoids HTTP/1 application-level serialization, but TCP packet loss can still stall streams sharing that transport connection.

**Q:** How does a Protocol Buffers schema define a cross-language contract?

**A:** The schema names services, fields and messages so clients can generate compatible code. Binary size and speed depend on data and tooling; field evolution still requires compatibility discipline.

**Q:** Why do browser clients need a different gRPC integration path?

**A:** Browser networking APIs do not expose the same transport capabilities as native gRPC clients. gRPC-Web commonly uses an adapter or proxy, with streaming support depending on the chosen implementation.

## gRPC Streaming

Source: [gRPC Streaming](20.6.2.02-grpc-streaming.md)

**Q:** Which interaction patterns need server, client or bidirectional streaming?

**A:** Server streaming returns many messages for one request; client streaming sends many messages for one response; bidirectional streaming allows both sides to send sequences. Unary calls remain appropriate for a single exchange.

**Q:** Why do long-lived streams require backpressure and cancellation policies?

**A:** Flow control regulates transport pressure, but applications must also bound buffers and propagate cancellation. Deadlines and completion rules define how resources are released and whether reconnect/resume is supported.

**Q:** What happens when a stream never completes or notices cancellation?

**A:** A stream can retain connections, memory and downstream work. Handle deadlines, cancellation and terminal events; a client disconnect does not automatically stop every application task.

## Apache Kafka

Source: [Apache Kafka](20.6.2.03-kafka.md)

**Q:** How does an append-only log support durable recording and replay?

**A:** Appending records supports sequential storage, while offsets identify consumption positions for replay. Durability also depends on replication and acknowledgment settings; required history must remain within retention.

**Q:** How do partitions and consumer groups combine parallelism with ordering?

**A:** Partitions define the ordering boundary; a group's usual assignment gives each partition to one active member. More consumers than partitions do not add partition-level parallelism, and concurrent effects still need ordering discipline.

**Q:** How does retention differ from removing work after acknowledgment?

**A:** Kafka retains records independently of one group's consumption. Time, size and compaction policies determine available history; ordinary work queues instead remove completed deliveries under their acknowledgment contract.

## RabbitMQ

Source: [RabbitMQ](20.6.2.04-rabbitmq.md)

**Q:** How do exchanges and bindings route a RabbitMQ publication?

**A:** Publishers send to exchanges; bindings route messages to eligible queues by exact keys, patterns, fan-out or headers. Independent consumers need routing that gives each the intended copy.

**Q:** What do publisher confirms and consumer acknowledgments establish separately?

**A:** Publisher confirms address broker acceptance under the selected queue and persistence contract. Consumer acknowledgments address completed delivery handling; neither alone proves the application's end-to-end outcome.

**Q:** When does a queue-based work-distribution model fit a workload?

**A:** A queue fits routed jobs assigned to competing workers with per-delivery acknowledgments. Kafka and RabbitMQ Streams fit retained replay differently; compare the specific storage contract rather than the product name.

## Message Brokers: Kafka vs RabbitMQ

Source: [Message Brokers: Kafka vs RabbitMQ](20.6.2.05-message-brokers.md)

**Q:** How does a broker decouple producer and consumer availability?

**A:** A producer can complete after broker acceptance while consumers work later. This shifts the failure boundary to broker durability, backlog and eventual processing; it does not guarantee unlimited buffering.

**Q:** How do at-most-once, at-least-once and transactional processing differ?

**A:** At-most-once permits loss; at-least-once permits redelivery; transactional processing can provide exactly-once effects within a defined boundary. External APIs and sinks need their own atomicity or idempotency contract.

**Q:** Why must delivery guarantees and ordering scope be designed separately?

**A:** Delivery duplication and order are different properties. Define ordering per entity, queue or partition; retries and concurrent workers can change completion order even when transport order is preserved.

## Event-Driven Architecture — Kafka, Event Sourcing, CQRS

Source: [Event-Driven Architecture — Kafka, Event Sourcing, CQRS](20.6.2.06-event-driven-architecture.md)

**Q:** How can a new consumer react to an event without changing the producer?

**A:** A consumer can subscribe to an existing fact contract when it already contains the needed data and permits that access. Adding new data or semantics can still require a producer change.

**Q:** How do notification events and state-carrying events change consumer dependencies?

**A:** Notifications keep payloads small but may require a source lookup that returns newer state. State-carrying events reduce that dependency at the cost of copied data, larger contracts and retention obligations.

**Q:** What consistency, debugging and schema costs accompany asynchronous events?

**A:** Downstream effects can lag committed source state. Trace identity, replay policy and compatible schema evolution are necessary; local operations can still have stronger consistency boundaries.

## Summary

Use these prompts after the reading pass to recall the communication and messaging mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.

## Broker storage and acknowledgments

Source: [Learning chapter](20.6.2.05-message-brokers.md)

**Q:** Is replay a Kafka-versus-RabbitMQ yes/no distinction?

**A:** No. Kafka retains partition records; ordinary RabbitMQ queues track unfinished deliveries, but RabbitMQ Streams also support retained log replay. Compare the actual storage type and retention contract.

**Q:** What does a publisher confirm fail to establish?

**A:** It does not prove consumer business completion. Unroutable-message handling is also distinct from broker acceptance; uncertain acknowledgments can require duplicate-safe retry.


## Event publication and consumer crashes

Source: [Learning chapter](20.6.2.06-event-driven-architecture.md)

**Q:** Which failure gap does an outbox close, and which remains?

**A:** Committing state and publication intent together prevents losing the event when a process dies after the database commit. Publish/ack uncertainty can still deliver duplicates.

**Q:** Why must a processed-event marker and projection update share a transaction?

**A:** Separate writes can mark unfinished work complete or repeat a completed mutation after a crash. Atomic commitment makes a redelivery observe one consistent outcome.

**Q:** How do event ID, correlation ID and aggregate version differ?

**A:** Event ID identifies one occurrence; correlation ID groups related work; aggregate version orders changes for one entity. Schema version instead identifies the payload format.
