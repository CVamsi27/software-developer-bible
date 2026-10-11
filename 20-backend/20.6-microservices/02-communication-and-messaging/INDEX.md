# Communication & Messaging - Microservices

> **Study time:** ≈ 41 min of reading (7 files, ~6 min average).
> **7 files.** How services talk: gRPC (+ streaming) for typed RPC over HTTP/2, Kafka and RabbitMQ for messaging, broker selection discipline, and event-driven architecture.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Communication%20%26%20Messaging-blue)](../INDEX.md)

---

## Learning flow

Trace a typed unary call before studying stream lifetime and cancellation. Then compare Kafka partition progress with RabbitMQ routed deliveries, use broker selection to choose the actual storage model, and finish with durable event publication and consumers. Use [revision](REVISION.md) before the [interview bank](../05-interview-drills/20.6.5.01-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [gRPC](20.6.2.01-grpc.md) | Protobuf, HTTP/2, code generation, contract-first design, interceptor chains | Important | Important | 6 min |
| 02 | [gRPC Streaming](20.6.2.02-grpc-streaming.md) | Streaming modes, flow control, cancellation, gRPC-Web and client trade-offs | Important | Important | 5 min |
| 03 | [Kafka](20.6.2.03-kafka.md) | Partitioned log, keys, consumer groups, ordering, transactions within Kafka's boundary and replay | Important | Important | 7 min |
| 04 | [RabbitMQ](20.6.2.04-rabbitmq.md) | AMQP, exchanges/bindings, dead-letter queues, per-message acks, task distribution | Important | Important | 7 min |
| 05 | [Message Brokers](20.6.2.05-message-brokers.md) | Kafka vs RabbitMQ selection, DLQ discipline, delivery guarantees | Important | Important | 6 min |
| 06 | [Event-Driven Architecture](20.6.2.06-event-driven-architecture.md) | When events beat requests; producer/consumer coupling, reprocessing | Essential | Important | 7 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) source paths illustrate current in-process/provider boundaries; inspect their actual completion contract rather than treating them as broker deployments:

| Topic | Docita evidence |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| In-process event bus | `apps/api/src/shared/common/events/event.service.ts` - typed publish over EventEmitter2 |
| Event catalog | `apps/api/src/shared/common/events/domain-events.ts` - enum'd appointment/patient/billing/prescription events |
| Channel abstraction | `apps/api/src/shared/modules/messaging/notification-orchestrator.service.ts` - channel-agnostic notification fan-out |
| Provider adapter isolation | `apps/api/src/shared/modules/messaging/email/providers/zeptomail-email.provider.ts` - circuit-broken ZeptoMail behind IEmailProvider |

Kafka, RabbitMQ, and gRPC not used — justified while events stay inside one deployable; a cross-deployable requirement would need an explicit transport and acknowledgment contract. It does not automatically require a particular broker.
---

[← Previous: Service Topology](../01-service-topology/INDEX.md) · [Next: Data & Consistency →](../03-data-and-consistency/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
