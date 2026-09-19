# Message Brokers — Index

> **Study time:** ≈ 25 min of reading (4 files, ~6 min average).
> The transport layer of event-driven systems: Kafka's log model and RabbitMQ's queue model, delivery semantics, durability configuration, consumer-group operations, and the patterns (envelopes, DLQs, outbox, idempotency) that make async pipelines production-safe. Pairs with [Microservices](../20.6-microservices/INDEX.md) (the architecture that uses brokers) and [Queues & Async](../../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) (the theory).

[![Files](https://img.shields.io/badge/files-4-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 4 content files classify into 3 conceptual categories + drills.

| Category | Files | Why it matters |
| --------------------- | ----: | -------------------------------------------------------------------------------- |
| **Model & Semantics** | 1 | Log vs queue, delivery guarantees, when a broker is the wrong tool |
| **Operations** | 1 | Replication/ISR, produce durability, consumer groups, rebalances, lag as the SLI |
| **Patterns** | 1 | Envelopes, schema evolution, DLQ policy, outbox, idempotent consumers |
| **Interview Drills** | 1 | 25 Q&A with follow-up traps |

---

## Study Order

| # | File | You can defend… |
| - | ---- | --------------- |
| 1 | [Message Brokers](20.9.01-message-brokers.md) | Why decoupling in time is worth a cluster; Kafka vs RabbitMQ models; at-least-once + idempotency as the default contract; when *not* to add a broker |
| 2 | [Kafka Internals & Operations](20.9.02-kafka-internals-and-operations.md) | `acks=all` + `min.insync.replicas` quorum math; consumer groups and rebalance storms; lag as the SLI; compaction and replay-as-restart |
| 3 | [Event-Driven Patterns on a Broker](20.9.03-event-driven-patterns.md) | Envelopes and schema contracts that survive version skew; retry→DLQ policy; outbox for atomic write+publish; consumer idempotency patterns |
| 4 | [Interview Questions](20.9.04-interview-questions.md) | 25 Q&A with follow-up traps |

## The Decision Map (memorize)

```text
Need a reply now?            → HTTP, no broker
One consumer, low rate?      → job table / in-process queue, no broker
Replay + stream analytics?   → Kafka (log model)
Rich routing + work queues?  → RabbitMQ (queue model)
Ordering?                    → per partition/queue ONLY — key by entity id
Delivery?                    → at-least-once + idempotent consumer (always)
DB write + publish atomic?   → transactional outbox
Anything can be poison?      → bounded retries → DLQ → alert → review
```

## Cross-References

- [Microservices & Distributed Patterns](../20.6-microservices/INDEX.md) — saga, CQRS, outbox, service mesh
- [Queues & Async (theory)](../../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) — backpressure, Little's law, the architecture why
- [Idempotency Keys](../../30-architecture/30.3-infra-patterns/02-failure-and-recovery/30.3.2.03-idempotency-keys.md) — the consumer-side contract
- [Observability](../../40-platform/40.4-observability/INDEX.md) — lag dashboards, tracing across async hops

## Navigation

[← Previous: Caching](../20.8-caching/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: AI Engineering →](../20.12-ai-engineering/INDEX.md)
