# Microservices & Distributed Patterns — Index

> **17 files — the single home for distributed-systems patterns.** Learn in four passes: **I. Foundations** (how services find and talk to each other) → **II. Data patterns** (consistency across services) → **III. Resilience** (surviving partial failure) → **IV. Messaging & migration** (brokers, evolution) → drills.
>
> Canonical source for saga, circuit breaker, bulkhead, strangler fig, service discovery, API gateway, CQRS/event sourcing, gRPC — the thinner twins in `30.3-infra-patterns` were consolidated here.

[![Files](https://img.shields.io/badge/files-17-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 16 content files classify into 5 conceptual categories — the "GoF classification" of distributed systems.

| Category | Files | Why it matters |
|----------|------:|----------------|
| **Service Topology** | 4 | Service discovery, API gateway, service mesh, strangler fig — how services find each other and evolve safely |
| **Communication & Messaging** | 5 | gRPC (+ streaming), Kafka, RabbitMQ, message brokers, event-driven architecture — how services talk |
| **Data Consistency Patterns** | 4 | Saga, distributed transactions, event sourcing, CQRS — atomicity and truth across service boundaries |
| **Resilience Patterns** | 2 | Circuit breaker, bulkhead — surviving partial failure |
| **Interview Drills** | 1 | 50+ curated Q&A |

---

## The Flow

```text
PASS I — FOUNDATIONS PASS II — DATA PATTERNS PASS III — RESILIENCE PASS IV — MESSAGING
01 service discovery → 07 event sourcing → 04 circuit breaker → 05 Kafka
02 API gateway 13 CQRS 14 bulkhead 06 RabbitMQ
09 gRPC (+16 streaming) 11 distributed transactions (overview: 15 message brokers
                            03 saga pattern 30.3 resilience) 17 event-driven architecture
                                                           10 service mesh 12 strangler fig
```

| Pass | # | File | Topics |
|---|---|------|--------|
| I | 01 | [Service Discovery](20.6.01-service-discovery.md) | Client vs server-side, Consul, Eureka, DNS-based |
| I | 02 | [API Gateway](20.6.02-api-gateway.md) | Routing, aggregation, auth, rate limiting at the edge |
| I | 03 | [gRPC](20.6.09-grpc.md) | Protobuf, HTTP/2, code generation |
| II | 04 | [Event Sourcing](20.6.07-event-sourcing.md) | Event store, rebuilding state, snapshots |
| II | 05 | [CQRS](20.6.13-cqrs.md) | Command/query separation, read models, eventual consistency |
| II | 06 | [Saga Pattern](20.6.03-saga-pattern.md) | Choreography vs orchestration, compensating transactions |
| II | 07 | [Distributed Transactions](20.6.11-distributed-transactions.md) | Saga, outbox, 2PC trade-offs |
| III | 08 | [Circuit Breaker](20.6.04-circuit-breaker.md) | States, fallbacks, resilience wiring |
| III | 09 | [Bulkhead Pattern](20.6.14-bulkhead-pattern.md) | Pool isolation, tenant isolation |
| III | 10 | [Service Mesh](20.6.10-service-mesh.md) | Istio, Linkerd, mTLS, traffic management |
| IV | 11 | [Kafka](20.6.05-kafka.md) | Topics, partitions, consumer groups, exactly-once |
| IV | 12 | [RabbitMQ](20.6.06-rabbitmq.md) | Exchanges, queues, durability |
| IV | 13 | [Message Brokers](20.6.15-message-brokers.md) | Kafka vs RabbitMQ, DLQ discipline |
| IV | 14 | [Event-Driven Architecture](20.6.17-event-driven-architecture.md) | When events beat requests; producer/consumer, reprocessing |
| IV | 15 | [Strangler Fig](20.6.12-strangler-fig.md) | Legacy migration, parallel run, dual-write |
| V | 16 | [gRPC Streaming](20.6.16-grpc-streaming.md) | Streaming modes, gRPC-Web, when gRPC beats REST |
| | 17 | [Interview Questions](20.6.08-interview-questions.md) | 50+ curated Q&A |

---

**Cross-references:** Ops-level siblings in [30.3 Infra Patterns](../../30-architecture/30.3-infra-patterns/INDEX.md) (retries, idempotency, health checks, leader election) · [NestJS Microservices](../20.2-nestjs/INDEX.md) · [System Design theory](../../30-architecture/30.2-system-design/INDEX.md) · [Docker](../../40-platform/40.1-docker/INDEX.md)

---

## Navigation

[← Previous: Security (Auth track)](../20.5-security/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: GraphQL →](../20.7-graphql/INDEX.md)
