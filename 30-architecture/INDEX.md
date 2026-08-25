# Architecture Stack

> **System design + design patterns** — shared by both the [indian-sde-faang lane](../81-lanes-indian-sde-faang/INDEX.md) and the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> The architecture stack is what you need for system design rounds. Do this after you've covered frontend and backend stacks (10-frontend, 20-backend).

[![Files](https://img.shields.io/badge/files-85-blue)](INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-3-green)](#study-order)

---

## Sections (in study order)

| Section | Files | Topics |
|---------|------:|--------|
| [Design Patterns](30.1-design-patterns/INDEX.md) | 30+ | **Foundations** (SOLID, OOP, UML) + **Creational** (Singleton, Factory, Builder, Abstract Factory, Prototype) + **Structural** (Adapter, Facade, Decorator, Proxy, Module, Composite, Bridge, Flyweight) + **Behavioral** (Strategy, Observer, Chain, State, Template Method, Iterator, Mediator, Memento, Command, Visitor, Interpreter) + **Architectural** (Repository, CQRS+DI, Event Sourcing, Saga) + 50+ interview questions. All 23 GoF patterns + modern patterns. |
| [System Design](30.2-system-design/INDEX.md) | 42 | 14 foundational theory files (CAP, consistency, sharding, caching, queues, distributed transactions, rate limiting, consensus, failure modes, architecture patterns, capacity planning, backpressure, distributed locks) + 6 meta guides (approach framework, interview bank, probabilistic structures, outbox/CDC, resilience deep-dive, multi-region) + 22 case studies (URL shortener, WhatsApp, Uber, Netflix, payment gateway, ticket booking, etc.) |
| [Infrastructure Patterns](30.3-infra-patterns/INDEX.md) | 10 | Database scaling (partitioning, replication, connection pooling), resilience patterns (circuit breaker, bulkhead, retry), leader election & consensus, technical debt management, zero-downtime deployments, data pipelines, health checks & graceful shutdown, retry patterns, idempotency keys, CDN architecture |

---

## Design Patterns — Category Map

The Design Patterns section is now organized by the **Gang of Four classification** + modern architectural patterns. Each category has its own INDEX with detailed descriptions, decision flowcharts, and comparisons.

| Category | Subfolder | Count | Purpose |
|----------|-----------|------:|---------|
| Foundations | [30.1.0-foundations](30.1-design-patterns/30.1.0-foundations/INDEX.md) | 4 files | SOLID, OOP, UML — read these first |
| Creational | [30.1.1-creational](30.1-design-patterns/30.1.1-creational/INDEX.md) | 5 patterns | Object creation mechanisms |
| Structural | [30.1.2-structural](30.1-design-patterns/30.1.2-structural/INDEX.md) | 8 patterns | Class/object composition |
| Behavioral | [30.1.3-behavioral](30.1-design-patterns/30.1.3-behavioral/INDEX.md) | 11 patterns | Object collaboration & responsibility |
| Architectural | [30.1.4-architectural](30.1-design-patterns/30.1.4-architectural/INDEX.md) | 4+ patterns | Modern distributed systems |
| Interview Prep | [30.1.5-interview-prep](30.1-design-patterns/30.1.5-interview-prep/INDEX.md) | 1 file | 50+ curated Q&A |

 **Start here: [Design Patterns Index](30.1-design-patterns/INDEX.md)** — full pattern map and decision cheat sheet.

---

## Study Order

1. **Design Patterns first**
   - [Foundations](30.1-design-patterns/30.1.0-foundations/INDEX.md) — SOLID, OOP, UML (1.5 hrs)
   - At least 1 pattern from each category (4-6 hrs)
   - Deep dive on 3-4 patterns you use daily (3-4 hrs)
   - [Interview Questions](30.1-design-patterns/30.1.5-interview-prep/30.1.51-interview-questions.md) for 50+ Qs (2-3 hrs)

2. **System Design theory** (CAP, consistency, sharding, caching, queues) — concepts.

3. **System Design case studies** (URL shortener, Uber, Netflix) — applied examples.

4. **Infrastructure patterns** — production-grade scaling, resilience, deployment.

---

**Lane-specific overlays:** Add interview strategy context, behavioral stories, and prep plans in [Interview Lanes](../80-lanes-abroad-full-stack/INDEX.md) — the stacks stay stack-pure.
