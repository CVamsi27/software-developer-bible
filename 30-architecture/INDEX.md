# Architecture Stack

> **Study time:** ≈ 18 h 13 m of reading (121 files, ~9 min average).
> **System design + design patterns** — shared by both the [indian-sde-faang lane](../81-lanes-indian-sde-faang/INDEX.md) and the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> The architecture stack is what you need for system design rounds. Do this after you've covered frontend and backend stacks (10-frontend, 20-backend).

[![Files](https://img.shields.io/badge/files-121-blue)](INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-3-green)](#study-order)

---

## Sections (in study order)

| Section | Files | Topics |
| ------------------------------------------------------- | ----: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Design Patterns](30.1-design-patterns/INDEX.md) | 38 | **Foundations** (SOLID, OOP, UML) + **Creational** (Singleton, Factory, Builder, Abstract Factory, Prototype) + **Structural** (Adapter, Facade, Decorator, Proxy, Module, Composite, Bridge, Flyweight) + **Behavioral** (Strategy, Observer, Chain, State, Template Method, Iterator, Mediator, Memento, Command, Visitor, Interpreter) + **Architectural** (Repository, CQRS+DI, Event Sourcing, Saga) + 50+ interview questions. All 23 GoF patterns + modern patterns. |
| [System Design](30.2-system-design/INDEX.md) | 54 | Theory (CAP, consistency, sharding, caching, queues, transactions, rate limiting, consensus, failures, capacity, transport, DNS and TLS) + approach/interview practice and advanced mechanisms (probabilistic structures, outbox/CDC, resilience and multi-region) + case studies (URL shortener, WhatsApp, Uber, Netflix, payment gateway, ticket booking, etc.) |
| [Infrastructure Patterns](30.3-infra-patterns/INDEX.md) | 17 | Health and lifecycle, resilience and recovery, coordination, scaling and multi-tenant systems, deployments, technical debt, FinOps, data retention, and interview practice |

---

## Design Patterns — Category Map

The Design Patterns section groups patterns using the **Gang of Four classification**: creating objects, combining objects, and coordinating their behavior. It also covers modern architectural patterns. Each category has its own INDEX with detailed descriptions, decision flowcharts, and comparisons.

| Category | Subfolder | Count | Purpose |
| -------------- | -------------------------------------------------------------------- | ----------: | ------------------------------------- |
| Foundations | [01-foundations](30.1-design-patterns/01-foundations/INDEX.md) | 4 files | SOLID, OOP, UML — read these first |
| Creational | [02-creational](30.1-design-patterns/02-creational/INDEX.md) | 5 patterns | Object creation mechanisms |
| Structural | [03-structural](30.1-design-patterns/03-structural/INDEX.md) | 8 patterns | Class/object composition |
| Behavioral | [04-behavioral](30.1-design-patterns/04-behavioral/INDEX.md) | 11 patterns | Object collaboration & responsibility |
| Architectural | [05-architectural](30.1-design-patterns/05-architectural/INDEX.md) | 4 patterns | Modern distributed systems |
| Interview Prep | [06-interview-prep](30.1-design-patterns/06-interview-prep/INDEX.md) | 1 file | 50+ curated Q&A |

 **Start here: [Design Patterns Index](30.1-design-patterns/INDEX.md)** — full pattern map and category learning paths.

---

## Study Order

1. **Design Patterns first**
   - [Foundations](30.1-design-patterns/01-foundations/INDEX.md) — SOLID, OOP, UML (1.5 hrs)
   - At least 1 pattern from each category (4-6 hrs)
   - Deep dive on 3-4 patterns you use daily (3-4 hrs)
   - [Interview Questions](30.1-design-patterns/06-interview-prep/30.1.6.01-interview-questions.md) for 50+ Qs (2-3 hrs)

2. **System Design theory** (CAP, consistency, sharding, caching, queues) — concepts.

3. **System Design case studies** (URL shortener, Uber, Netflix) — applied examples.

4. **Infrastructure patterns** — operational contracts for scaling, resilience, release and recovery.

Use the category REVISION companions after their learning chapters, then the separate interview drills. For case studies, state assumptions, trace one request/change through its authorities and test a failure condition; remembering a diagram alone is insufficient.

---

**Lane-specific overlays:** Add interview strategy context, behavioral stories, and prep plans in [Interview Lanes](../80-lanes-abroad-full-stack/INDEX.md) — the stacks stay stack-pure.

---

## Docita Anchor

Category indexes map concepts to Docita source: strategy registries, builders, facades, repository ports, rate limiting, PostgreSQL queues and outbox delivery. Use the [Docita cases](../projects/docita/INDEX.md) to trace the current implementation and its limitations. Heartbeat telemetry records scheduler activity; it is not leader election. A source anchor locates a mechanism rather than proving deployment, complete enforcement or a business result.

---

[← Previous: Backend Stack](../20-backend/INDEX.md) · [Next: Platform Stack →](../40-platform/INDEX.md)
