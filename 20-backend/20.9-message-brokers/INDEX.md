# Message Brokers — Index

> **Study time:** ≈ 35 min of reading (5 files, ~7 min average).
> The transport layer of event-driven systems: Kafka's log model and RabbitMQ's queue model, delivery semantics, durability configuration, consumer-group operations, and the patterns (envelopes, DLQs, outbox, idempotency) that make async pipelines production-safe. Pairs with [Microservices](../20.6-microservices/INDEX.md) (the architecture that uses brokers) and [Queues & Async](../../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) (the theory).

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 4 content files classify into 3 conceptual categories + drills.

| Category | Files | Why it matters |
| --------------------- | ----: | --------------------------------------------------------------------------------------------------------- |
| **Model & Semantics** | 1 | Log vs queue, delivery guarantees, when a broker is the wrong tool |
| **Operations** | 1 | Replication/ISR, produce durability, classic groups, KIP-848, Share Groups, rebalances and lag boundaries |
| **Patterns** | 1 | Envelopes, schema evolution, DLQ policy, outbox, idempotent consumers |
| **Interview Drills** | 1 | 25 Q&A with follow-up traps |

---

## Study Order

| # | File | You can defend… | Role priority | General importance |
| - | ---- | --------------- | --- | --- |
| 1 | [Message Brokers](20.9.01-message-brokers.md) | Why decoupling in time is worth a cluster; Kafka vs RabbitMQ models; at-least-once + idempotency as the default contract; when *not* to add a broker | Important | Specialized |
| 2 | [Kafka Internals & Operations](20.9.02-kafka-internals-and-operations.md) | `acks=all` and the ISR acceptance floor; classic groups, KIP-848 and Share Groups; rebalance storms; offset lag and replay boundaries | Important | Specialized |
| 3 | [Event-Driven Patterns on a Broker](20.9.03-event-driven-patterns.md) | Envelopes and schema contracts that survive version skew; retry→DLQ policy; outbox for atomic write+publication intent; consumer idempotency patterns | Important | Specialized |
| — | [Revision](REVISION.md) | Explain the crash, offset reset, key remapping, and missing-blob cases before drilling | Important | Specialized |
| 4 | [Interview Questions](20.9.04-interview-questions.md) | 25 Q&A with follow-up traps | Important | Specialized |

## Choose the Required Contract

```text
Need a reply now?            → HTTP, no broker
One consumer, low rate?      → job table / in-process queue, no broker
Replay + stream analytics?   → Kafka classic consumer group (log model)
Per-record work distribution? → Kafka 4.2+ Share Groups or RabbitMQ queues; compare acknowledgment and ordering contracts
Rich routing + work queues?  → RabbitMQ exchanges and queues
Ordering?                    → Kafka classic group: per partition; RabbitMQ: strongest with a single active consumer and no requeue/priority effects; key by entity id
Delivery?                    → configure acknowledgments/durability; make retries idempotent
DB write + event intent atomic? → transactional outbox
Anything can be poison?      → bounded retries → DLQ → alert → review
```

## Review the Mechanisms

After the three chapters, use [Revision](REVISION.md) to explain acknowledgment, replay, and quarantine boundaries from memory. Then use the interview bank to practice a concise failure story.

## Cross-References

- [Microservices & Distributed Patterns](../20.6-microservices/INDEX.md) — saga, CQRS, outbox, service mesh
- [Queues & Async (theory)](../../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) — backpressure, Little's law, the architecture why
- [Idempotency Keys](../../30-architecture/30.3-infra-patterns/02-failure-and-recovery/30.3.2.03-idempotency-keys.md) — the consumer-side contract
- [Observability](../../40-platform/40.4-observability/INDEX.md) — lag dashboards, tracing across async hops
- [Kafka 4.3 — release notes and Share Groups](https://kafka.apache.org/43/getting-started/upgrade/) — versioned boundary between classic groups and per-record share consumption
- [RabbitMQ 4.3.6 — queue ordering](https://www.rabbitmq.com/docs/queues) — conditions that affect dequeue and processing order

## Docita Anchor

The [Docita study material](../../projects/docita/03-async-processing.md) describes a PostgreSQL worker design. The following implementation details are study pointers; confirm the current checkout and call sites before presenting them as deployed behavior:

| Topic | Docita evidence | Role priority | General importance |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ |
| Broker-or-not decision | [Async processing doc](../../projects/docita/03-async-processing.md) - evaluate PostgreSQL queue tradeoffs from measured workload; no verified jobs/sec result is implied | Essential | Important |
| Transactional enqueue | Ordinary PostgresQueueService.enqueue creates a job in its own operation; atomic business/job intent requires an explicitly shared transaction or an outbox at the actual call site | Varies | Varies |
| Idempotent enqueue | name/key lookup for completed jobs within 24 hours; it does not atomically suppress concurrent or still-running submissions | Varies | Varies |
| Bounded retries → DLQ | Default maxAttempts=5 can be overridden; delayedUntil backoff and terminal failure preserve local attempt state, not external exactly-once effects | Varies | Varies |
| Exactly-one claiming | `FOR UPDATE SKIP LOCKED` polling - concurrent claims select distinct locked rows; recovery/retry can still duplicate effects, so idempotent execution is required | Varies | Varies |
| Stale-worker recovery | ACTIVE jobs older than ten minutes are recovered with a delay; an older worker can still finish later, so ownership fencing and effect idempotency remain separate concerns | Varies | Varies |
| Outbox relay | `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts` + `outbox.service.ts` - `OutboxEvent` rows polled and republished after commit | Varies | Varies |

The referenced Docita design uses PostgreSQL workers rather than Kafka/RabbitMQ; this is an architectural study example, not current deployment evidence. The broker chapters' real-world anchor here is the decision matrix that kept them out, plus the patterns implemented broker-free (idempotency, retry→DLQ, claiming, outbox). A broker migration requires explicit changes to acknowledgments, ownership, delivery/replay and consumer contracts; replacing a publish target alone is not enough.

## Navigation

[← Previous: Caching](../20.8-caching/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: AI Engineering →](../20.12-ai-engineering/INDEX.md)
