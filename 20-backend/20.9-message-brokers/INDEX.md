# Message Brokers — Index

> **Study time:** ≈ 29 min of reading (5 files, ~6 min average).
> The transport layer of event-driven systems: Kafka's log model and RabbitMQ's queue model, delivery semantics, durability configuration, consumer-group operations, and the patterns (envelopes, DLQs, outbox, idempotency) that make async pipelines production-safe. Pairs with [Microservices](../20.6-microservices/INDEX.md) (the architecture that uses brokers) and [Queues & Async](../../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) (the theory).

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
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
| 2 | [Kafka Internals & Operations](20.9.02-kafka-internals-and-operations.md) | `acks=all` and the ISR acceptance floor; consumer groups and rebalance storms; lag as the SLI; compaction and replay-as-restart |
| 3 | [Event-Driven Patterns on a Broker](20.9.03-event-driven-patterns.md) | Envelopes and schema contracts that survive version skew; retry→DLQ policy; outbox for atomic write+publish; consumer idempotency patterns |
| 4 | [Interview Questions](20.9.04-interview-questions.md) | 25 Q&A with follow-up traps |

## The Decision Map (memorize)

```text
Need a reply now?            → HTTP, no broker
One consumer, low rate?      → job table / in-process queue, no broker
Replay + stream analytics?   → Kafka (log model)
Rich routing + work queues?  → RabbitMQ (queue model)
Ordering?                    → per partition/queue ONLY — key by entity id
Delivery?                    → configure acknowledgments/durability; make retries idempotent
DB write + publish atomic?   → transactional outbox
Anything can be poison?      → bounded retries → DLQ → alert → review
```

## Review the Mechanisms

After the three chapters, use [Revision](REVISION.md) to explain acknowledgment, replay, and quarantine boundaries from memory. Then use the interview bank to practice a concise failure story.

## Cross-References

- [Microservices & Distributed Patterns](../20.6-microservices/INDEX.md) — saga, CQRS, outbox, service mesh
- [Queues & Async (theory)](../../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) — backpressure, Little's law, the architecture why
- [Idempotency Keys](../../30-architecture/30.3-infra-patterns/02-failure-and-recovery/30.3.2.03-idempotency-keys.md) — the consumer-side contract
- [Observability](../../40-platform/40.4-observability/INDEX.md) — lag dashboards, tracing across async hops

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Broker-or-not decision | [Async processing doc](../../projects/docita/03-async-processing.md) - decision matrix: Postgres-as-queue at ~0.4 jobs/sec vs Redis/Kafka ops overhead; the 20.9.01 "when not to add a broker" call, shipped |
| Transactional enqueue | `apps/api/src/shared/modules/queue/postgres-queue.service.ts` - job enqueued in the same Prisma transaction as the business write |
| Idempotent enqueue | idempotency-key dedup on submit - recent completed jobs short-circuit duplicates |
| Bounded retries → DLQ | max 5 attempts with `delayedUntil` backoff → `DEAD_LETTERED` status for manual inspection |
| Exactly-one claiming | `FOR UPDATE SKIP LOCKED` polling - concurrent claims select distinct locked rows; recovery/retry can still duplicate effects, so idempotent execution is required |
| Stale-worker recovery | jobs stuck `ACTIVE` >10 min re-queued by the recovery pass - the crash-between-claim-and-ack hole, closed |
| Outbox relay | `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts` + `outbox.service.ts` - `OutboxEvent` rows polled and republished after commit |

Docita ships **zero Kafka/RabbitMQ - deliberately.** The broker chapters' real-world anchor here is the decision matrix that kept them out, plus the patterns implemented broker-free (idempotency, retry→DLQ, claiming, outbox). If load ever demands a broker, the outbox relay's publish target changes - the contracts (envelope, idempotency keys, DLQ semantics) do not.

## Navigation

[← Previous: Caching](../20.8-caching/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: AI Engineering →](../20.12-ai-engineering/INDEX.md)
