# Architectural Patterns

> **4+ files.** Modern, distributed-systems patterns. These are NOT part of the original GoF set — they emerged as software engineering evolved to handle scale, distributed systems, and domain-driven design.

[![Files](https://img.shields.io/badge/files-4%2B-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architectural-red)](#)
[![Status](https://img.shields.io/badge/status-growing-yellow)](#)

---

## What architectural patterns solve

GoF patterns are about classes and objects within a single process. Architectural patterns are about **how services, modules, or layers of a system interact** — across process boundaries, databases, teams, and deployment units.

These show up heavily in:
- Senior backend / staff engineer interviews
- System design rounds
- Microservices and distributed systems discussions
- Domain-driven design conversations

---

## The 4+ patterns

| # | Pattern | Intent | Use when | Avoid when |
|--:|---------|--------|----------|------------|
| 1 | [Repository](30.1.5.01-repository.md) | Data access abstraction | DDD, testability, multi-DB support | Simple CRUD with one model |
| 2 | [CQRS & DI](30.1.5.02-cqrs-di.md) | Command/query separation + DI container | Complex domains, asymmetric read/write load | Simple CRUD, low scale |
| 3 | [Event Sourcing](30.1.5.03-event-sourcing.md) | Store events, derive state | Audit-required domains, temporal queries, debugging | State is ephemeral, no audit needed |
| 4 | [Saga](30.1.5.04-saga.md) | Distributed transactions | Multi-service business flows | Single DB transaction works |

---

## Pattern Index

### [Repository](30.1.5.01-repository.md)
Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects. Repository encapsulates the logic of persisting and retrieving domain objects.

**When to use:**
- You want your domain logic independent of the persistence layer
- You want testable data access (mock the repo, no real DB)
- You want to swap persistence (PostgreSQL → MongoDB → in-memory) without changing business code
- You're practicing Domain-Driven Design

**When NOT to use:**
- Simple CRUD with one entity type
- Your ORM already provides this abstraction (Prisma's `prisma.user` is essentially a Repository)
- You have a 2-table app and adding a repo layer is overkill

### [CQRS & DI](30.1.5.02-cqrs-di.md)
**CQRS (Command Query Responsibility Segregation):** Separate the model that writes data (Commands) from the model that reads data (Queries). Each side can be optimized independently.

**DI (Dependency Injection):** A technique where one object supplies the dependencies of another, instead of the dependent object creating them itself.

**When to use CQRS:**
- Read and write workloads differ drastically (e.g., 1000× more reads)
- You need different models for read vs write (e.g., denormalized read store)
- You want to scale reads independently from writes
- You want clearer separation of intent in code

**When to use DI:**
- Always, in any non-trivial app — it's the standard way to make code testable
- When you want to swap implementations (different DB in tests, different HTTP client in production)

### [Event Sourcing](30.1.5.03-event-sourcing.md) *(new)*
Capture all changes to an application state as a sequence of events. The current state is derived by replaying events. Instead of storing just the latest state, you store the full history of what happened.

**When to use:**
- You need a complete audit trail (finance, healthcare, legal)
- You need temporal queries ("what did the system look like at time T?")
- You want to debug by replaying events
- You want to derive multiple read models from the same event stream

**When NOT to use:**
- State is ephemeral (chat messages with no audit)
- You can't pay the complexity cost (event store, snapshots, projections)
- Your domain is simple CRUD

### [Saga](30.1.5.04-saga.md) *(new)*
Manage distributed transactions across multiple services by breaking them into local transactions and compensating actions. Each service commits its local transaction, and if one fails, compensating transactions undo the prior steps.

**When to use:**
- A business transaction spans multiple services
- You can't use a single DB transaction (2-phase commit doesn't scale across services)
- You need eventual consistency with rollback capability

**When NOT to use:**
- You can use a single DB transaction (single service, single DB)
- The business logic is simple enough to fit in one service
- You can't tolerate eventual consistency

---

## Decision flowchart

```
How is your data accessed / persisted?
│
├─ Just need data access abstraction? ──→ Repository
│
├─ Read and write models are very different? ──→ CQRS
│
├─ Need full history / audit / temporal queries? ──→ Event Sourcing
│
├─ Transaction spans multiple services? ──→ Saga
│
└─ Just want loose coupling + testability? ──→ DI (always)
```

---

## How they compose

These patterns are often used together in real systems:

| Composition | What you get |
|-------------|--------------|
| **Repository + DI** | Domain code with mocked data access, swappable persistence |
| **CQRS + Event Sourcing** | Reads are projections of the event log; commands emit events |
| **CQRS + Saga** | Commands trigger multi-service workflows; queries serve denormalized views |
| **All four** | Full DDD microservices stack (Axon, EventStore, NestJS CQRS) |

---

## When NOT to use architectural patterns

**None of these belong in a startup MVP.** They are heavyweight, require team expertise, and add complexity. Reach for them when:
- You've identified a specific problem (read/write asymmetry, audit, distributed tx)
- You have team capacity to maintain the new moving parts
- The scale or compliance requirement justifies the cost

If a junior engineer is proposing CQRS + Event Sourcing for a CRUD blog, that is over-engineering.

---

## Cross-References

- [Microservices & Distributed Patterns](../../../20-backend/20.6-microservices/INDEX.md) — Saga, Outbox, Event Sourcing are covered in depth there
- [NestJS](../../../20-backend/20.2-nestjs/INDEX.md) — DI, CQRS modules, Repository pattern
- [System Design](../../30.2-system-design/INDEX.md) — event-driven architecture, eventual consistency

---

## Navigation

[← Behavioral Patterns](../04-behavioral/INDEX.md) · [↑ Design Patterns Home](../INDEX.md) · [Next: Interview Prep →](../06-interview-prep/INDEX.md)
