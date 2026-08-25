# Design Patterns — Index

> **33 files — all 23 GoF patterns plus modern architectural ones, classified by GoF category and purpose.** Design patterns are reusable solutions to recurring problems in software design. The Gang of Four (GoF) formalized 23 classic patterns; we cover all 23 plus modern architectural patterns. Senior LLD/HLD interviews assume fluent recall of these.

[![Files](https://img.shields.io/badge/files-33-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)
[![GoF Coverage](https://img.shields.io/badge/GoF%20Coverage-23%2F23-success)](#)

**Why patterns matter in interviews:** A senior engineer is expected to (1) recognize the pattern in unfamiliar code, (2) pick the right pattern for a given LLD problem, and (3) articulate tradeoffs vs alternatives. Memorizing the catalog is not enough — every pattern in this index is paired with anti-patterns, real-world examples, and "when NOT to use" guidance.

---

## Classification

Design patterns are classified into **3 GoF categories** (creational, structural, behavioral) + **foundations** (principles you need first) + **architectural** (modern patterns for distributed systems) + **interview prep**.

| Category | Purpose | Subfolder | # Patterns |
|----------|---------|-----------|-----------:|
| **Foundations** | Principles, OOP, UML — read first | [01-foundations](01-foundations/INDEX.md) | 4 theory files |
| **Creational** | Object creation mechanisms (decoupling construction from use) | [02-creational](02-creational/INDEX.md) | 5 patterns |
| **Structural** | Class/object composition (assemble larger structures from parts) | [03-structural](03-structural/INDEX.md) | 8 patterns |
| **Behavioral** | Object collaboration and responsibility distribution | [04-behavioral](04-behavioral/INDEX.md) | 11 patterns |
| **Architectural** | Modern, distributed-systems patterns (not in original GoF) | [05-architectural](05-architectural/INDEX.md) | 4 patterns |
| **Interview Prep** | Curated question bank, mock interview scenarios | [06-interview-prep](06-interview-prep/INDEX.md) | 1 file (50+ Qs) |

---

## How to Navigate

### If you're new to design patterns

1. Start with [Foundations](01-foundations/INDEX.md) — SOLID, OOP, UML. The patterns below are meaningless without these.
2. Read one pattern from each category (start with the iconic ones: Singleton, Adapter, Observer).
3. Then go deep on the patterns that map to your daily work.

### If you're prepping for an interview

1. Skim the [category overview](01-foundations/INDEX.md) (5 min).
2. Read **all 5 creational** + **8 structural** + **11 behavioral** at the "TL;DR + When to use" level (1-2 hrs).
3. Deep-dive on 3-4 patterns you don't know cold.
4. Hit [Interview Questions](06-interview-prep/30.1.6.01-interview-questions.md) for 50+ curated questions.

### If you're picking a pattern for a real problem

Use this decision cheat sheet (full version in each category INDEX):

| Need | Category | Pick one of |
|------|----------|-------------|
| Create objects flexibly | Creational | Factory, Builder, Abstract Factory, Prototype, Singleton |
| Compose classes into larger structures | Structural | Adapter, Decorator, Facade, Proxy, Composite, Bridge, Module |
| Manage object interactions | Behavioral | Observer, Strategy, State, Command, Mediator, Chain of Responsibility, Iterator, Visitor, Memento, Template Method, Interpreter |
| Distributed systems | Architectural | Repository, CQRS+DI, Event Sourcing, Saga, Outbox |

---

## Sub-Index Links

### [01 — Foundations](01-foundations/INDEX.md)
SOLID, OOP concepts, UML diagrams, DRY/KISS/YAGNI. Read these before any pattern.

### [02 — Creational Patterns](02-creational/INDEX.md) (5 files)
Object creation. Decouple "how to construct" from "what to do with the constructed thing."

- [Singleton](02-creational/30.1.2.01-singleton.md) — one global instance
- [Factory Method](02-creational/30.1.2.02-factory-method.md) — subclass decides what to instantiate
- [Builder](02-creational/30.1.2.03-builder.md) — step-by-step construction of complex objects
- [Abstract Factory](02-creational/30.1.2.04-abstract-factory.md) — families of related objects
- [Prototype](02-creational/30.1.2.05-prototype.md) — clone instead of construct

### [03 — Structural Patterns](03-structural/INDEX.md) (8 files)
Class/object composition. Combine small pieces into larger structures while keeping them flexible.

- [Adapter](03-structural/30.1.3.01-adapter.md) — bridge incompatible interfaces
- [Facade](03-structural/30.1.3.02-facade.md) — simplified front for a complex subsystem
- [Decorator](03-structural/30.1.3.03-decorator.md) — add behavior dynamically without subclassing
- [Proxy](03-structural/30.1.3.04-proxy.md) — controlled access (lazy, protection, remote, caching)
- [Module Pattern](03-structural/30.1.3.05-module-pattern.md) — encapsulation at the file level
- [Composite](03-structural/30.1.3.06-composite.md) — tree structures, treat part-whole uniformly
- [Bridge](03-structural/30.1.3.07-bridge.md) — decouple abstraction from implementation
- [Flyweight](03-structural/30.1.3.08-flyweight.md) — share state to support many fine-grained objects

### [04 — Behavioral Patterns](04-behavioral/INDEX.md) (11 files)
Object collaboration. Manage algorithms, responsibilities, and communication between objects.

- [Strategy](04-behavioral/30.1.4.01-strategy.md) — swap algorithms at runtime
- [Observer](04-behavioral/30.1.4.02-observer.md) — event-driven, pub/sub
- [Chain of Responsibility](04-behavioral/30.1.4.03-chain-of-responsibility.md) — pass request along a chain
- [State](04-behavioral/30.1.4.04-state.md) — behavior changes with internal state
- [Template Method](04-behavioral/30.1.4.05-template-method.md) — skeleton + steps
- [Iterator](04-behavioral/30.1.4.06-iterator.md) — sequential access without exposing internals
- [Mediator](04-behavioral/30.1.4.07-mediator.md) — central authority for object communication
- [Memento](04-behavioral/30.1.4.08-memento.md) — capture/restore internal state
- [Command](04-behavioral/30.1.4.09-command.md) — encapsulate a request as an object
- [Visitor](04-behavioral/30.1.4.10-visitor.md) — add operations without modifying classes
- [Interpreter](04-behavioral/30.1.4.11-interpreter.md) — grammar + interpreter for a DSL

### [05 — Architectural Patterns](05-architectural/INDEX.md) (4 files)
Modern, distributed-systems patterns. Cross-cutting; not part of the original GoF set.

- [Repository](05-architectural/30.1.5.01-repository.md) — data access abstraction
- [CQRS & DI](05-architectural/30.1.5.02-cqrs-di.md) — command/query separation + dependency injection
- [Event Sourcing](05-architectural/30.1.5.03-event-sourcing.md) — store events, not state
- [Saga](05-architectural/30.1.5.04-saga.md) — distributed transactions

### [06 — Interview Prep](06-interview-prep/INDEX.md) (1 file, 50+ Qs)
- [Design Pattern Interview Questions](06-interview-prep/30.1.6.01-interview-questions.md) — 50+ curated Qs with answers

---

## Pattern Map (one-glance cheat sheet)

| Pattern | Category | Intent | Use when | Avoid when |
|---------|----------|--------|----------|------------|
| **Singleton** | Creational | One global instance | Logger, config, connection pool | Testability matters, multiple envs |
| **Factory Method** | Creational | Defer instantiation to subclass | Plugin system, multiple impls | Only one type, simple new |
| **Abstract Factory** | Creational | Families of related objects | Cross-platform UI, theme systems | Few object types, no family concept |
| **Builder** | Creational | Step-by-step complex object | 5+ optional fields, immutability | Simple objects with 2-3 fields |
| **Prototype** | Creational | Clone instead of construct | Object creation is expensive | Class hierarchy is simple |
| **Adapter** | Structural | Bridge incompatible interfaces | 3rd-party SDK, legacy integration | You control both sides |
| **Facade** | Structural | Simple front for complex system | Library/SDK, multi-subsystem workflow | Single subsystem, already simple |
| **Decorator** | Structural | Add behavior dynamically | Cross-cutting concerns (logging, auth) | Many combinations → combinatorial explosion |
| **Proxy** | Structural | Controlled access | Lazy loading, caching, auth checks | Direct access is fine |
| **Module** | Structural | Encapsulation at file level | Always (in modern JS/TS) | N/A (it's a default) |
| **Composite** | Structural | Part-whole tree | File system, UI tree, org chart | Flat structures, no recursion |
| **Bridge** | Structural | Decouple abstraction/implementation | Multiple dimensions of variation | One dimension, stable axis |
| **Flyweight** | Structural | Share state to scale | Many similar objects (chars, particles) | Few objects, no memory pressure |
| **Strategy** | Behavioral | Swap algorithms at runtime | Multiple ways to do same thing | Only one algorithm ever |
| **Observer** | Behavioral | Event-driven notification | UI events, pub/sub, reactive streams | Tight coupling is acceptable |
| **Chain of Responsibility** | Behavioral | Pass request along chain | Middleware, validation pipelines | Single handler always |
| **State** | Behavioral | Behavior depends on state | State machines, workflow engines | Few states, no transitions |
| **Template Method** | Behavioral | Skeleton + customizable steps | Algorithm with varying steps | Algorithm is fully fixed |
| **Iterator** | Behavioral | Sequential access | Collections, lazy sequences | Trivial arrays |
| **Mediator** | Behavioral | Central communication hub | Many-to-many object interactions | Few objects, direct refs are fine |
| **Memento** | Behavioral | Capture/restore state | Undo, snapshots, transactions | No history needed |
| **Command** | Behavioral | Request as object | Undo/redo, queueing, macro recording | Simple one-shot operations |
| **Visitor** | Behavioral | Add ops without modifying classes | ASTs, compilers, complex object structures | Class hierarchy is unstable |
| **Interpreter** | Behavioral | Grammar + interpreter | DSLs, configuration formats | Performance-critical parsing |
| **Repository** | Architectural | Data access abstraction | Domain-driven design, testing | Simple CRUD with one model |
| **CQRS** | Architectural | Separate read/write models | High-read or high-write asymmetry | Simple CRUD, low scale |
| **Event Sourcing** | Architectural | State from event log | Audit-required domains, temporal queries | State is ephemeral, no audit |
| **Saga** | Architectural | Distributed transactions | Microservices, multi-step business flow | Single DB transaction works |

---

## Cross-References

- [System Design](../30.2-system-design/INDEX.md) — many system design patterns build on these (circuit breaker → proxy, pub/sub → observer, …)
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — algorithm patterns (sliding window, DP), unrelated but interview-adjacent
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — uses Module, DI, Repository, CQRS, Observer extensively
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — Saga, Event Sourcing, Outbox, CQRS

---

## Navigation

[← Back: Architecture](../INDEX.md) · [ Bible Index](../../INDEX.md) · [Next: System Design →](../30.2-system-design/INDEX.md)
