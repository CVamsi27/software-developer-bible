# Design Patterns — Index

> **30+ files, classified by GoF category and purpose.** Design patterns are reusable solutions to recurring problems in software design. The Gang of Four (GoF) formalized 23 classic patterns; we cover all 23 plus 5 modern architectural patterns. Senior LLD/HLD interviews assume fluent recall of these.

[![Files](https://img.shields.io/badge/files-30%2B-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)
[![GoF Coverage](https://img.shields.io/badge/GoF%20Coverage-23%2F23-success)](#)

**Why patterns matter in interviews:** A senior engineer is expected to (1) recognize the pattern in unfamiliar code, (2) pick the right pattern for a given LLD problem, and (3) articulate tradeoffs vs alternatives. Memorizing the catalog is not enough — every pattern in this index is paired with anti-patterns, real-world examples, and "when NOT to use" guidance.

---

## 🗂️ Classification

Design patterns are classified into **3 GoF categories** (creational, structural, behavioral) + **foundations** (principles you need first) + **architectural** (modern patterns for distributed systems) + **interview prep**.

| Category | Purpose | Subfolder | # Patterns |
|----------|---------|-----------|-----------:|
| **Foundations** | Principles, OOP, UML — read first | [30.1.0-foundations](30.1.0-foundations/INDEX.md) | 4 theory files |
| **Creational** | Object creation mechanisms (decoupling construction from use) | [30.1.1-creational](30.1.1-creational/INDEX.md) | 5 patterns |
| **Structural** | Class/object composition (assemble larger structures from parts) | [30.1.2-structural](30.1.2-structural/INDEX.md) | 7 patterns |
| **Behavioral** | Object collaboration and responsibility distribution | [30.1.3-behavioral](30.1.3-behavioral/INDEX.md) | 11 patterns |
| **Architectural** | Modern, distributed-systems patterns (not in original GoF) | [30.1.4-architectural](30.1.4-architectural/INDEX.md) | 4+ patterns |
| **Interview Prep** | Curated question bank, mock interview scenarios | [30.1.5-interview-prep](30.1.5-interview-prep/INDEX.md) | 1 file (50+ Qs) |

---

## 🧭 How to Navigate

### If you're new to design patterns

1. Start with [Foundations](30.1.0-foundations/INDEX.md) — SOLID, OOP, UML. The patterns below are meaningless without these.
2. Read one pattern from each category (start with the iconic ones: Singleton, Adapter, Observer).
3. Then go deep on the patterns that map to your daily work.

### If you're prepping for an interview

1. Skim the [category overview](30.1.0-foundations/INDEX.md) (5 min).
2. Read **all 5 creational** + **7 structural** + **11 behavioral** at the "TL;DR + When to use" level (1-2 hrs).
3. Deep-dive on 3-4 patterns you don't know cold.
4. Hit [Interview Questions](30.1.5-interview-prep/30.1.51-interview-questions.md) for 50+ curated questions.

### If you're picking a pattern for a real problem

Use this decision cheat sheet (full version in each category INDEX):

| Need | Category | Pick one of |
|------|----------|-------------|
| Create objects flexibly | Creational | Factory, Builder, Abstract Factory, Prototype, Singleton |
| Compose classes into larger structures | Structural | Adapter, Decorator, Facade, Proxy, Composite, Bridge, Module |
| Manage object interactions | Behavioral | Observer, Strategy, State, Command, Mediator, Chain of Responsibility, Iterator, Visitor, Memento, Template Method, Interpreter |
| Distributed systems | Architectural | Repository, CQRS+DI, Event Sourcing, Saga, Outbox |

---

## 📁 Sub-Index Links

### [00 — Foundations](30.1.0-foundations/INDEX.md)
SOLID, OOP concepts, UML diagrams, DRY/KISS/YAGNI. Read these before any pattern.

### [01 — Creational Patterns](30.1.1-creational/INDEX.md) (5 files)
Object creation. Decouple "how to construct" from "what to do with the constructed thing."

- [Singleton](30.1.1-creational/30.1.11-singleton.md) — one global instance
- [Factory Method](30.1.1-creational/30.1.12-factory-method.md) — subclass decides what to instantiate
- [Builder](30.1.1-creational/30.1.13-builder.md) — step-by-step construction of complex objects
- [Abstract Factory](30.1.1-creational/30.1.14-abstract-factory.md) — families of related objects
- [Prototype](30.1.1-creational/30.1.15-prototype.md) — clone instead of construct

### [02 — Structural Patterns](30.1.2-structural/INDEX.md) (7 files)
Class/object composition. Combine small pieces into larger structures while keeping them flexible.

- [Adapter](30.1.2-structural/30.1.21-adapter.md) — bridge incompatible interfaces
- [Facade](30.1.2-structural/30.1.22-facade.md) — simplified front for a complex subsystem
- [Decorator](30.1.2-structural/30.1.23-decorator.md) — add behavior dynamically without subclassing
- [Proxy](30.1.2-structural/30.1.24-proxy.md) — controlled access (lazy, protection, remote, caching)
- [Module Pattern](30.1.2-structural/30.1.25-module-pattern.md) — encapsulation at the file level
- [Composite](30.1.2-structural/30.1.26-composite.md) — tree structures, treat part-whole uniformly
- [Bridge](30.1.2-structural/30.1.27-bridge.md) — decouple abstraction from implementation
- [Flyweight](30.1.2-structural/30.1.28-flyweight.md) — share state to support many fine-grained objects

### [03 — Behavioral Patterns](30.1.3-behavioral/INDEX.md) (11 files)
Object collaboration. Manage algorithms, responsibilities, and communication between objects.

- [Strategy](30.1.3-behavioral/30.1.31-strategy.md) — swap algorithms at runtime
- [Observer](30.1.3-behavioral/30.1.32-observer.md) — event-driven, pub/sub
- [Chain of Responsibility](30.1.3-behavioral/30.1.33-chain-of-responsibility.md) — pass request along a chain
- [State](30.1.3-behavioral/30.1.34-state.md) — behavior changes with internal state
- [Template Method](30.1.3-behavioral/30.1.35-template-method.md) — skeleton + steps
- [Iterator](30.1.3-behavioral/30.1.36-iterator.md) — sequential access without exposing internals
- [Mediator](30.1.3-behavioral/30.1.37-mediator.md) — central authority for object communication
- [Memento](30.1.3-behavioral/30.1.38-memento.md) — capture/restore internal state
- [Command](30.1.3-behavioral/30.1.39-command.md) — encapsulate a request as an object
- [Visitor](30.1.3-behavioral/30.1.40-visitor.md) — add operations without modifying classes
- [Interpreter](30.1.3-behavioral/30.1.41-interpreter.md) — grammar + interpreter for a DSL

### [04 — Architectural Patterns](30.1.4-architectural/INDEX.md) (4+ files)
Modern, distributed-systems patterns. Cross-cutting; not part of the original GoF set.

- [Repository](30.1.4-architectural/30.1.41-repository.md) — data access abstraction
- [CQRS & DI](30.1.4-architectural/30.1.42-cqrs-di.md) — command/query separation + dependency injection
- [Event Sourcing](30.1.4-architectural/30.1.43-event-sourcing.md) — store events, not state
- [Saga](30.1.4-architectural/30.1.44-saga.md) — distributed transactions

### [05 — Interview Prep](30.1.5-interview-prep/INDEX.md) (1 file, 50+ Qs)
- [Design Pattern Interview Questions](30.1.5-interview-prep/30.1.51-interview-questions.md) — 50+ curated Qs with answers

---

## 🗺️ Pattern Map (one-glance cheat sheet)

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

## 🔗 Cross-References

- [System Design](../../INDEX.md) — many system design patterns build on these (circuit breaker → proxy, pub/sub → observer, …)
- [Coding Patterns](../../INDEX.md) — algorithm patterns (sliding window, DP), unrelated but interview-adjacent
- [NestJS](../../INDEX.md) — uses Module, DI, Repository, CQRS, Observer extensively
- [Microservices](../../INDEX.md) — Saga, Event Sourcing, Outbox, CQRS

---

## Navigation

[← Back: Architecture](../INDEX.md) · [🏠 Bible Index](../../INDEX.md) · [Next: System Design →](../../INDEX.md)
