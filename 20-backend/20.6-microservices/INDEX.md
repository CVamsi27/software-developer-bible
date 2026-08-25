# Microservices & Distributed Patterns — Index

> **18 files — the single home for distributed-systems patterns.** Learn in four passes: **I. Foundations** (how services find and talk to each other) → **II. Data patterns** (consistency across services) → **III. Resilience** (surviving partial failure) → **IV. Messaging & migration** (brokers, evolution) → drills.
>
> Canonical source for saga, circuit breaker, bulkhead, strangler fig, service discovery, API gateway, CQRS/event sourcing, monolith database decomposition, gRPC — the thinner twins in `30.3-infra-patterns` were consolidated here.

[![Files](https://img.shields.io/badge/files-18-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 18 content files classify into 5 categories, each with its own INDEX — the "GoF classification" of distributed systems.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Service Topology](01-service-topology/INDEX.md) | 4 | Service discovery, API gateway, service mesh, strangler fig — how services find each other and evolve safely |
| [Communication & Messaging](02-communication-and-messaging/INDEX.md) | 6 | gRPC (+ streaming), Kafka, RabbitMQ, message brokers, event-driven architecture — how services talk |
| [Data & Consistency](03-data-and-consistency/INDEX.md) | 5 | Saga, distributed transactions, event sourcing, CQRS, database decomposition — atomicity and truth across service boundaries |
| [Resilience](04-resilience/INDEX.md) | 2 | Circuit breaker, bulkhead — surviving partial failure |
| [Interview Drills](05-interview-drills/INDEX.md) | 1 | 50+ curated Q&A |

---

## The Flow

```text
PASS I — FOUNDATIONS       PASS II — DATA PATTERNS     PASS III — RESILIENCE    PASS IV — MESSAGING
01-service-topology     →  03-data-and-consistency  →  04-resilience         →  02-communication
service discovery          event sourcing              circuit breaker           kafka / rabbitmq
api gateway                cqrs                        bulkhead                  message brokers
grpc (+streaming)          saga                        (overview: 30.3           event-driven arch
service mesh               distributed transactions    resilience)               strangler fig
```

---

## The Study Order

| Pass | # | File | Topics |
|---|---|------|--------|
| I | 01 | [Service Discovery](01-service-topology/20.6.1.01-service-discovery.md) | Client vs server-side, Consul, Eureka, DNS-based |
| I | 02 | [API Gateway](01-service-topology/20.6.1.02-api-gateway.md) | Routing, aggregation, auth, rate limiting at the edge |
| I | 03 | [gRPC](02-communication-and-messaging/20.6.2.01-grpc.md) | Protobuf, HTTP/2, code generation |
| II | 04 | [Event Sourcing](03-data-and-consistency/20.6.3.03-event-sourcing.md) | Event store, rebuilding state, snapshots |
| II | 05 | [CQRS](03-data-and-consistency/20.6.3.04-cqrs.md) | Command/query separation, read models, eventual consistency |
| II | 06 | [Saga Pattern](03-data-and-consistency/20.6.3.01-saga-pattern.md) | Choreography vs orchestration, compensating transactions |
| II | 07 | [Distributed Transactions](03-data-and-consistency/20.6.3.02-distributed-transactions.md) | Saga, outbox, 2PC trade-offs |
| II | 08 | [Decomposing the Monolith Database](03-data-and-consistency/20.6.3.05-decomposing-monolith-database.md) | Shared-DB hazards, data strangulation, dual-write vs CDC sync, backfills |
| III | 09 | [Circuit Breaker](04-resilience/20.6.4.01-circuit-breaker.md) | States, fallbacks, resilience wiring |
| III | 10 | [Bulkhead Pattern](04-resilience/20.6.4.02-bulkhead-pattern.md) | Pool isolation, tenant isolation |
| III | 11 | [Service Mesh](01-service-topology/20.6.1.03-service-mesh.md) | Istio, Linkerd, mTLS, traffic management |
| IV | 12 | [Kafka](02-communication-and-messaging/20.6.2.03-kafka.md) | Topics, partitions, consumer groups, exactly-once |
| IV | 13 | [RabbitMQ](02-communication-and-messaging/20.6.2.04-rabbitmq.md) | Exchanges, queues, durability |
| IV | 14 | [Message Brokers](02-communication-and-messaging/20.6.2.05-message-brokers.md) | Kafka vs RabbitMQ, DLQ discipline |
| IV | 15 | [Event-Driven Architecture](02-communication-and-messaging/20.6.2.06-event-driven-architecture.md) | When events beat requests; producer/consumer, reprocessing |
| IV | 16 | [Strangler Fig](01-service-topology/20.6.1.04-strangler-fig.md) | Legacy migration, parallel run, dual-write |
| V | 17 | [gRPC Streaming](02-communication-and-messaging/20.6.2.02-grpc-streaming.md) | Streaming modes, gRPC-Web, when gRPC beats REST |
| | 18 | [Interview Questions](05-interview-drills/20.6.5.01-interview-questions.md) | 50+ curated Q&A |

---

**Cross-references:** Ops-level siblings in [30.3 Infra Patterns](../../30-architecture/30.3-infra-patterns/INDEX.md) (retries, idempotency, health checks, leader election) · [NestJS Microservices](../20.2-nestjs/INDEX.md) · [System Design theory](../../30-architecture/30.2-system-design/INDEX.md) · [Docker](../../40-platform/40.1-docker/INDEX.md)

---

## Navigation

[← Previous: Security (Auth track)](../20.5-security/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: GraphQL →](../20.7-graphql/INDEX.md)
