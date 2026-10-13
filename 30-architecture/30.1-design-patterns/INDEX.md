# Design Patterns — Index

> **Study time:** ≈ 4 h 28 m of reading (43 files, ~6 min average).
> **43 files — all 23 GoF patterns plus modern architectural ones, classified by GoF category and purpose.** Design patterns are reusable solutions to recurring problems in software design. The Gang of Four (GoF) formalized 23 classic patterns; we cover all 23 plus modern architectural patterns. Use the catalog to explain responsibilities and trade-offs in low-level and high-level design discussions.

[![Files](https://img.shields.io/badge/files-43-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)
[![GoF Coverage](https://img.shields.io/badge/GoF%20Coverage-23%2F23-success)](#)

**Why patterns matter in interviews:** A senior engineer is expected to (1) recognize the pattern in unfamiliar code, (2) choose a pattern for a low-level design (LLD) problem about classes and their interactions, and (3) explain its tradeoffs against alternatives. Memorizing the catalog is not enough: every pattern in this index is paired with common misuses, real-world examples, and guidance on when to avoid it.

---

## Classification

Design patterns are classified into **3 GoF categories** (creational, structural, behavioral) + **foundations** (principles you need first) + **architectural** (application and cross-boundary design) + **interview prep**.

| Category | Purpose | Subfolder | # Patterns |
| ------------------ | ---------------------------------------------------------------- | ----------------------------------------------- | --------------: |
| **Foundations** | Principles, OOP, UML — read first | [01-foundations](01-foundations/INDEX.md) | 4 theory files |
| **Creational** | Object creation mechanisms (decoupling construction from use) | [02-creational](02-creational/INDEX.md) | 5 patterns |
| **Structural** | Class/object composition (assemble larger structures from parts) | [03-structural](03-structural/INDEX.md) | 8 patterns |
| **Behavioral** | Object collaboration and responsibility distribution | [04-behavioral](04-behavioral/INDEX.md) | 12 patterns |
| **Architectural** | Application, domain and presentation boundaries (outside GoF) | [05-architectural](05-architectural/INDEX.md) | 8 patterns |
| **Interview Prep** | Curated question bank, mock interview scenarios | [06-interview-prep](06-interview-prep/INDEX.md) | 1 file (50+ Qs) |

---

Module and Null Object are additional patterns in this catalog. The GoF set has five creational, seven structural and eleven behavioral patterns; the category lists also include these additions.

## How to Navigate

### If you're new to design patterns

1. Start with [Foundations](01-foundations/INDEX.md) — SOLID, OOP, UML. These principles help explain the contracts and tradeoffs in later chapters.
2. Read one pattern from each category (start with the iconic ones: Singleton, Adapter, Observer).
3. Then go deep on the patterns that map to your daily work.

### If you're prepping for an interview

1. Skim the [category overview](01-foundations/INDEX.md) (5 min).
2. Read **all 5 creational** + **8 structural** + **12 behavioral** through each chapter's concrete problem and execution trace.
3. Deep-dive on 3-4 patterns you don't know cold.
4. Hit [Interview Questions](06-interview-prep/30.1.6.01-interview-questions.md) for 50+ curated questions.

### If you're picking a pattern for a real problem

Use this decision cheat sheet (full version in each category INDEX):

| Need | Category | Pick one of |
| --------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Create objects flexibly | Creational | Factory Method, Builder, Abstract Factory, Prototype, scoped Singleton |
| Compose classes into larger structures | Structural | Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight, Module |
| Manage object interactions | Behavioral | Observer, Strategy, State, Command, Mediator, Chain of Responsibility, Iterator, Visitor, Memento, Template Method, Interpreter, Null Object |
| Application boundaries and distributed coordination | Architectural | Repository, CQRS+DI, Event Sourcing, Saga, DDD Aggregates, Anti-Corruption Layer, Service Locator vs DI, MVC/MVP/MVVM |

---

## Sub-Index Links

### [01 — Foundations](01-foundations/INDEX.md)
SOLID, OOP concepts, UML diagrams, DRY/KISS/YAGNI. Read these before any pattern.

### [02 — Creational Patterns](02-creational/INDEX.md) (5 files)
Object creation. Decouple "how to construct" from "what to do with the constructed thing."

- [Singleton](02-creational/30.1.2.01-singleton.md) — one instance in a defined scope
- [Factory Method](02-creational/30.1.2.02-factory-method.md) — subclass decides what to instantiate
- [Builder](02-creational/30.1.2.03-builder.md) — step-by-step construction of complex objects
- [Abstract Factory](02-creational/30.1.2.04-abstract-factory.md) — families of related objects
- [Prototype](02-creational/30.1.2.05-prototype.md) — create from a configured prototype with an explicit copy contract

### [03 — Structural Patterns](03-structural/INDEX.md) (8 files)
Class/object composition. Combine small pieces into larger structures while keeping them flexible.

- [Adapter](03-structural/30.1.3.01-adapter.md) — translate an existing interface to the client's contract
- [Facade](03-structural/30.1.3.02-facade.md) — simplify common operations across a complex subsystem
- [Decorator](03-structural/30.1.3.03-decorator.md) — add behavior dynamically without subclassing
- [Proxy](03-structural/30.1.3.04-proxy.md) — controlled access (lazy, protection, remote, caching)
- [Module Pattern](03-structural/30.1.3.05-module-pattern.md) — encapsulation at the file level
- [Composite](03-structural/30.1.3.06-composite.md) — tree structures, treat part-whole uniformly
- [Bridge](03-structural/30.1.3.07-bridge.md) — decouple abstraction from implementation
- [Flyweight](03-structural/30.1.3.08-flyweight.md) — share state to support many fine-grained objects

### [04 — Behavioral Patterns](04-behavioral/INDEX.md) (12 files)
Object collaboration. Manage algorithms, responsibilities, and communication between objects.

- [Strategy](04-behavioral/30.1.4.01-strategy.md) — delegate to an interchangeable selected policy
- [Observer](04-behavioral/30.1.4.02-observer.md) — explicit notification registrations
- [Chain of Responsibility](04-behavioral/30.1.4.03-chain-of-responsibility.md) — pass request along a chain
- [State](04-behavioral/30.1.4.04-state.md) — behavior changes with internal state
- [Template Method](04-behavioral/30.1.4.05-template-method.md) — skeleton + steps
- [Iterator](04-behavioral/30.1.4.06-iterator.md) — sequential access without exposing internals
- [Mediator](04-behavioral/30.1.4.07-mediator.md) — central authority for object communication
- [Memento](04-behavioral/30.1.4.08-memento.md) — capture/restore internal state
- [Command](04-behavioral/30.1.4.09-command.md) — encapsulate a request as an object
- [Visitor](04-behavioral/30.1.4.10-visitor.md) — add operations over an established element/visitor contract
- [Interpreter](04-behavioral/30.1.4.11-interpreter.md) — grammar + interpreter for a DSL
- [Null Object](04-behavioral/30.1.4.12-null-object.md) — encapsulated no-op behavior instead of null

### [05 — Architectural Patterns](05-architectural/INDEX.md) (8 files)
Persistence, domain, coordination and UI boundaries. Some remain in one process; these are outside the original GoF set.

- [Repository](05-architectural/30.1.5.01-repository.md) — data access abstraction
- [CQRS & DI](05-architectural/30.1.5.02-cqrs-di.md) — command/query separation + dependency injection
- [Event Sourcing](05-architectural/30.1.5.03-event-sourcing.md) — events as the authoritative state history
- [Saga](05-architectural/30.1.5.04-saga.md) — recoverable workflows across committed local transactions
- [DDD Tactical Patterns](05-architectural/30.1.5.05-ddd-tactical-patterns-aggregates-value-objects.md) — entities, value objects, aggregate boundaries
- [Anti-Corruption Layer](05-architectural/30.1.5.06-anti-corruption-layer.md) — translate foreign model meaning at a context boundary
- [Service Locator vs DI](05-architectural/30.1.5.07-service-locator-vs-dependency-injection.md) — consumer lookup versus externally supplied collaborators
- [Presentation Patterns MVC/MVP/MVVM](05-architectural/30.1.5.08-presentation-patterns-mvc-mvp-mvvm.md) — UI separation strategies and what frameworks really use

### [06 — Interview Prep](06-interview-prep/INDEX.md) (1 file, 50+ Qs)
- [Design Pattern Interview Questions](06-interview-prep/30.1.6.01-interview-questions.md) — 50+ curated Qs with answers

---

## Check the boundary before the label

The category indexes contain focused comparison tables. For a real problem, identify what changes: construction, wrapper behavior, policy, lifecycle, coordination or persistence. Then choose the smallest boundary that keeps its contract visible. A familiar pattern can simplify that decision; adding every pattern only adds obligations.

After each category, use its separate revision companion. Finish with the interview bank's scenarios, where local class shapes must be connected to concurrency, failure and recovery.

---

## Cross-References

- [System Design](../30.2-system-design/INDEX.md) — many system design patterns build on these (failure control and delivery contracts extend beyond local wrapper/callback shapes)
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — algorithm patterns (sliding window, DP), unrelated but interview-adjacent
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — uses Module, DI, Repository, CQRS, Observer extensively
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — Saga, Event Sourcing, Outbox, CQRS

---

## Navigation

[← Back: Architecture](../INDEX.md) · [ Bible Index](../../INDEX.md) · [Next: System Design →](../30.2-system-design/INDEX.md)
