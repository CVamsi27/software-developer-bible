# Microservices & Distributed Patterns — Index

> **Study time:** ≈ 2 h 11 m of reading (23 files, ~6 min average).
> **23 files — the single home for distributed-systems patterns.** Learn service topology and communication first, then data ownership, partial-failure recovery and migration. Use each category’s revision companion before interview practice.
>
> Canonical source for saga, circuit breaker, bulkhead, strangler fig, service discovery, API gateway, CQRS/event sourcing, monolith database decomposition, gRPC — the thinner twins in `30.3-infra-patterns` were consolidated here.

[![Files](https://img.shields.io/badge/files-23-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The categories group responsibilities in a distributed system. Each learning category has its own staged INDEX and a separate revision companion.

| Category | Files | Why it matters |
| -------------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------------------------------------------- |
| [Service Topology](01-service-topology/INDEX.md) | 4 | Service discovery, API gateway, service mesh, strangler fig — how services find each other and evolve safely |
| [Communication & Messaging](02-communication-and-messaging/INDEX.md) | 6 | gRPC (+ streaming), Kafka, RabbitMQ, message brokers, event-driven architecture — how services talk |
| [Data & Consistency](03-data-and-consistency/INDEX.md) | 6 | Saga, distributed transactions, event sourcing, CQRS, database decomposition — atomicity and truth across service boundaries |
| [Resilience](04-resilience/INDEX.md) | 2 | Circuit breaker, bulkhead — surviving partial failure |
| [Interview Drills](05-interview-drills/INDEX.md) | 1 | 30 deep answers and quick follow-up prompts |

---

## The Flow

```text
Topology and RPC -> data ownership and consistency -> bounded failure recovery
                  -> durable messaging and migration -> revision -> interview practice
```

---

## Revision before interview practice

After each learning pass, use its source-linked companion: [Topology](01-service-topology/REVISION.md), [Communication](02-communication-and-messaging/REVISION.md), [Data and consistency](03-data-and-consistency/REVISION.md), and [Resilience](04-resilience/REVISION.md). Then combine the mechanisms in the interview bank.

## The Study Order

| Pass | # | File | Topics | Role priority | General importance |
| -------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| I | 01 | [Service Discovery](01-service-topology/20.6.1.01-service-discovery.md) | Client vs server-side, Consul, Eureka, DNS-based | Important | Important |
| I | 02 | [API Gateway](01-service-topology/20.6.1.02-api-gateway.md) | Routing, aggregation, auth, rate limiting at the edge | Important | Important |
| I | 03 | [gRPC](02-communication-and-messaging/20.6.2.01-grpc.md) | Protobuf, HTTP/2, code generation | Important | Important |
| II | 04 | [Event Sourcing](03-data-and-consistency/20.6.3.03-event-sourcing.md) | Event store, rebuilding state, snapshots | Important | Important |
| II | 05 | [CQRS](03-data-and-consistency/20.6.3.04-cqrs.md) | Command/query separation, read models, eventual consistency | Important | Important |
| II | 06 | [Saga Pattern](03-data-and-consistency/20.6.3.01-saga-pattern.md) | Choreography vs orchestration, compensating transactions | Important | Important |
| II | 07 | [Distributed Transactions](03-data-and-consistency/20.6.3.02-distributed-transactions.md) | Saga, outbox, 2PC trade-offs | Important | Important |
| II | 08 | [Decomposing the Monolith Database](03-data-and-consistency/20.6.3.05-decomposing-monolith-database.md) | Shared-DB hazards, data strangulation, dual-write vs CDC sync, backfills | Important | Important |
| III | 09 | [Circuit Breaker](04-resilience/20.6.4.01-circuit-breaker.md) | States, fallbacks, resilience wiring | Essential | Important |
| III | 10 | [Bulkhead Pattern](04-resilience/20.6.4.02-bulkhead-pattern.md) | Pool isolation, tenant isolation | Important | Important |
| III | 11 | [Service Mesh](01-service-topology/20.6.1.03-service-mesh.md) | Istio, Linkerd, mTLS, sidecar and ambient data planes, traffic policy and application trace context | Important | Important |
| IV | 12 | [Kafka](02-communication-and-messaging/20.6.2.03-kafka.md) | Topics, partitions, classic/share consumers, ordering and transactions within Kafka's boundary | Important | Important |
| IV | 13 | [RabbitMQ](02-communication-and-messaging/20.6.2.04-rabbitmq.md) | Exchanges, queues, durability | Important | Important |
| IV | 14 | [Message Brokers](02-communication-and-messaging/20.6.2.05-message-brokers.md) | Kafka vs RabbitMQ, DLQ discipline | Important | Important |
| IV | 15 | [Event-Driven Architecture](02-communication-and-messaging/20.6.2.06-event-driven-architecture.md) | Asynchronous facts, producer/consumer contracts, outbox and reprocessing | Essential | Important |
| IV | 16 | [Strangler Fig](01-service-topology/20.6.1.04-strangler-fig.md) | Legacy migration, parallel run, dual-write | Important | Important |
| V | 17 | [gRPC Streaming](02-communication-and-messaging/20.6.2.02-grpc-streaming.md) | Streaming modes, flow control, cancellation and gRPC-Web trade-offs | Important | Important |
| Practice | 18 | [Interview Questions](05-interview-drills/20.6.5.01-interview-questions.md) | 30 deep answers and 29 additional quick prompts | Important | Important |

---

**Cross-references:** Ops-level siblings in [30.3 Infra Patterns](../../30-architecture/30.3-infra-patterns/INDEX.md) (retries, idempotency, health checks, leader election) · [NestJS Microservices](../20.2-nestjs/INDEX.md) · [System Design theory](../../30-architecture/30.2-system-design/INDEX.md) · [Docker](../../40-platform/40.1-docker/INDEX.md)

---

## Navigation

[← Previous: Security (Auth track)](../20.5-security/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: GraphQL →](../20.7-graphql/INDEX.md)

---

## Docita Anchor

The local [Docita](https://github.com/CVamsi27/docita) source inspected on 10 October 2026 supplies examples, not evidence of a live deployment or distributed-system guarantees. In particular, a relay timeout does not cancel underlying listeners; retries can repeat effects. Inspect identity and transaction boundaries before making a resume or interview claim:

| Topic | Docita evidence |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Transactional outbox | `apps/api/src/shared/modules/outbox/` - `outbox.service.ts` appends events in the business `$transaction`; `outbox-relay.scheduler.ts` drains them |
| Postgres-backed queue | `apps/api/src/shared/modules/queue/postgres-queue.service.ts` + `queue.module.ts` + `queue.worker.module.ts` - durable job queue on Postgres rows |
| In-memory queue (dev) | `apps/api/src/shared/modules/queue/in-memory-queue.service.ts` - same port, no persistence, for tests/CI |
| DLQ & replay | `apps/api/src/shared/modules/queue/dlq.controller.ts` + `dlq-replay.scheduler.ts` - dead-letter inspection and scheduled replay |
| HTTP retry identity | `apps/api/src/shared/modules/idempotency/` - HTTP interceptor/service; this does not prove every background job is idempotent |
| Event-driven flow | `apps/api/src/shared/common/events/` - `event.service.ts` + `domain-events.ts`/`application-events.ts` on EventEmitter2 |
| Retry on transient errors | `apps/api/src/shared/common/interceptors/prisma-retry.interceptor.ts` - bounded retry for Prisma connection errors |
| Saga / 2PC | No counterpart - payments use idempotency + webhooks + reconciliation instead of a saga orchestrator |
| Kafka / RabbitMQ / gRPC / service mesh | No counterpart - the queue is intentionally Postgres-based; the chapters are the interview framing for when a broker earns its keep |
