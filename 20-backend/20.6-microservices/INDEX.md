# Microservices — Index

> **15 files** — Microservices architecture patterns from service discovery and API gateways to saga pattern, circuit breakers, messaging, gRPC, service mesh, CQRS, bulkhead, strangler fig, message brokers, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

| # | File | Topics |
|---|------|--------|
| 01 | [Service Discovery](20.6.01-service-discovery.md) | Client-side vs server-side discovery, Consul, Eureka, DNS-based |
| 02 | [API Gateway](20.6.02-api-gateway.md) | Gateway patterns, aggregation, routing, auth, rate limiting |
| 03 | [Saga Pattern](20.6.03-saga-pattern.md) | Choreography vs orchestration, compensating transactions |
| 04 | [Circuit Breaker](20.6.04-circuit-breaker.md) | Closed/open/half-open states, fallback strategies, resilience |
| 05 | [Kafka](20.6.05-kafka.md) | Topics, partitions, producers, consumers, consumer groups, exactly-once |
| 06 | [RabbitMQ](20.6.06-rabbitmq.md) | Exchanges, queues, bindings, routing, message durability |
| 07 | [Event Sourcing](20.6.07-event-sourcing.md) | Event store, rebuilding state, CQRS integration, snapshots |
| 08 | [Interview Questions](20.6.08-interview-questions.md) | 50+ curated questions with answers |
| 09 | [gRPC](20.6.09-grpc.md) | Protobuf, HTTP/2, bidirectional streaming, code generation |
| 10 | [Service Mesh](20.6.10-service-mesh.md) | Istio, Linkerd, Envoy, mTLS, traffic management, observability |
| 11 | [Distributed Transactions](20.6.11-distributed-transactions.md) | Saga choreography/orchestration, outbox pattern, 2PC |
| 12 | [Strangler Fig](20.6.12-strangler-fig.md) | Legacy migration, strangler facade, parallel run, feature flags, dual-write |
| 13 | [CQRS](20.6.13-cqrs.md) | Command/query separation, event sourcing integration, mediator pattern, read/write models, eventual consistency |
| 14 | [Bulkhead Pattern](20.6.14-bulkhead-pattern.md) | Thread pool isolation, semaphore, circuit breaker integration, tenant isolation, resilience |
| 15 | [Message Brokers](20.6.15-message-brokers.md) | Kafka vs RabbitMQ comparison, event sourcing, saga pattern, dead letter queues |

---

**Cross-references:** [NestJS Microservices](../20.2-nestjs/INDEX.md) | [System Design](../../30-architecture/30.2-system-design/INDEX.md) | [Docker](../../40-platform/40.1-docker/INDEX.md) | [Kubernetes](../../40-platform/40.2-kubernetes/INDEX.md)
---

## Navigation

[← Previous: Security](../20.5-security/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: GraphQL →](../20.7-graphql/INDEX.md)
