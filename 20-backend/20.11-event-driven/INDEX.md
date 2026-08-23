# Event-Driven Architecture — Index

> **Asynchronous, decoupled systems** — when events beat requests, and the patterns that keep them reliable.

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

## Contents

| File | Topics |
|------|--------|
| [Event-Driven Architecture](20.11.01-event-driven-architecture.md) | Kafka architecture (brokers, topics, partitions), producer/consumer patterns, event sourcing with aggregates, CQRS read/write models, dead letter queues, reprocessing |

## The Reliability Stack (read together)

| Concern | Pattern | Deep dive |
|---------|---------|-----------|
| Atomic state+event | Transactional outbox | [Microservices](../20.6-microservices/INDEX.md) · theory: [Outbox & CDC](../../30-architecture/30.2-system-design/00-theory/INDEX.md) |
| Duplicate delivery | Idempotent consumers + idempotency keys | [Idempotency Keys](../../30-architecture/30.3-infra-patterns/30.3.14-idempotency-keys.md) |
| Poison messages | DLQ + bounded replay | covered in [20.11.01](20.11.01-event-driven-architecture.md) |
| Broker choice | Postgres-as-queue → broker when volume demands | case study: Docita ADR 0001 ([80.21 §Q5](../../80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md)) |

## Cross-references

[Microservices patterns](../20.6-microservices/INDEX.md) · [WebSockets](../20.9-websockets/INDEX.md) · [System design: queues & backpressure](../../30-architecture/30.2-system-design/00-theory/INDEX.md)

---

## Navigation

[← Previous: GraphQL](../20.7-graphql/INDEX.md) · [🏠 Back to Index](../../INDEX.md)
