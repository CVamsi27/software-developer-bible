# Architectural Patterns

> **8 files.** Modern, distributed-systems patterns plus DDD tactical design and UI architecture. These are NOT part of the original GoF set — they emerged as software engineering evolved to handle scale, distributed systems, domain-driven design, and rich frontends.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architectural-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What architectural patterns solve

GoF patterns are about classes and objects within a single process. Architectural patterns are about **how services, modules, or layers of a system interact** — across process boundaries, databases, teams, and deployment units.

These show up heavily in:
- Senior backend / staff engineer interviews
- System design rounds
- Microservices and distributed systems discussions
- Domain-driven design conversations

---

## The 8 patterns

| # | Pattern | Intent | Use when | Avoid when |
| --: | --------- | -------- | ---------- | ------------ |
| 1 | [Repository](30.1.5.01-repository.md) | Data access abstraction | DDD, testability, multi-DB support | Simple CRUD with one model |
| 2 | [CQRS & DI](30.1.5.02-cqrs-di.md) | Command/query separation + DI container | Complex domains, asymmetric read/write load | Simple CRUD, low scale |
| 3 | [Event Sourcing](30.1.5.03-event-sourcing.md) | Store events, derive state | Audit-required domains, temporal queries, debugging | State is ephemeral, no audit needed |
| 4 | [Saga](30.1.5.04-saga.md) | Distributed transactions | Multi-service business flows | Single DB transaction works |
| 5 | [DDD Tactical Patterns](30.1.5.05-ddd-tactical-patterns-aggregates-value-objects.md) | Entities, value objects, aggregate boundaries | Complex domains with invariants to enforce | CRUD apps without business rules |
| 6 | [Anti-Corruption Layer](30.1.5.06-anti-corruption-layer.md) | Isolate legacy/external models from your domain | Integrating legacy systems, vendors, strangler migrations | You own both sides of the boundary |
| 7 | [Service Locator vs Dependency Injection](30.1.5.07-service-locator-vs-dependency-injection.md) | How dependencies get resolved | Understanding hidden deps, choosing a wiring strategy | (DI is the default; locator only for plugin registries) |
| 8 | [Presentation Patterns MVC/MVP/MVVM](30.1.5.08-presentation-patterns-mvc-mvp-mvvm.md) | Separating UI state, logic, and rendering | Frontend architecture discussions and refactors | Trivial static UIs |

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

### [DDD Tactical Patterns](30.1.5.05-ddd-tactical-patterns-aggregates-value-objects.md) *(new)*
Entities (identity over time), Value Objects (immutable, attribute-defined equality), and Aggregates (consistency boundaries with a single root and enforced invariants). Includes the aggregate rules: small boundaries, reference by ID, one transaction per aggregate, domain events for cross-aggregate updates, repository per root.

**When to use:**
- Complex domains where invariants must hold atomically ("order total is always the sum of valid lines")
- Business rules keep leaking into controllers/services
- Write contention or inconsistent state from unbounded object graphs

**When NOT to use:**
- Simple CRUD with no real invariants
- Reporting/read-only models
- Teams without capacity to maintain a rich domain layer

### [Anti-Corruption Layer](30.1.5.06-anti-corruption-layer.md) *(new)*
An isolation boundary that keeps legacy/external system concepts (status codes, sentinel nulls, alien DTOs) out of your domain model — implemented as Facade + Adapter + Translator, living inside the consuming bounded context.

**When to use:**
- Integrating a legacy system or third-party vendor whose model conflicts with yours
- Strangler-fig migrations needing a stable seam
- Long-lived integrations you don't control

**When NOT to use:**
- You own both sides (refactor instead)
- Trivial integration over a clean API
- Project lifespan shorter than the layer's build time

### [Service Locator vs Dependency Injection](30.1.5.07-service-locator-vs-dependency-injection.md) *(new)*
Two strategies for inversion of control over dependency construction. Constructor injection makes dependencies visible, compile-checked, and trivially mockable; a service locator hides them behind runtime registry lookups. Covers IoC containers, the "container-as-locator" anti-pattern, and the narrow legitimate locator case (plugin registries).

**When to read/use:**
- Choosing or defending a wiring strategy in interviews
- Refactoring hidden-dependency legacy code toward testability
- Building plugin/command registries keyed by runtime data

### [Presentation Patterns MVC/MVP/MVVM](30.1.5.08-presentation-patterns-mvc-mvp-mvvm.md) *(new)*
Three strategies for splitting UI into model/view/intermediary, differing in who talks to whom and how updates flow. Includes original Smalltalk MVC vs web MVC, MVP's passive view, MVVM's observable view-model, an honest mapping of what React/Vue/Angular/Rails actually do, and the classic interview traps.

**When to read/use:**
- Frontend architecture interviews ("is React MVC?")
- Extracting testable UI logic from framework components
- Choosing a pattern per app/module based on framework grain

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
├─ Complex domain with invariants to enforce? ──→ DDD Aggregates
│
├─ Legacy/vendor model polluting your domain? ──→ Anti-Corruption Layer
│
└─ Just want loose coupling + testability? ──→ DI (always, never locator)
```

---

## How they compose

These patterns are often used together in real systems:

| Composition | What you get |
| ----------------------------------------------- | -------------------------------------------------------------------------- |
| **Repository + DI** | Domain code with mocked data access, swappable persistence |
| **CQRS + Event Sourcing** | Reads are projections of the event log; commands emit events |
| **CQRS + Saga** | Commands trigger multi-service workflows; queries serve denormalized views |
| **DDD Aggregates + Repository + Domain Events** | Invariant-enforcing boundaries feeding outbox-driven integrations |
| **ACL + Strangler Fig** | Safe seams for incrementally replacing legacy systems |
| **All of the above** | Full DDD microservices stack (Axon, EventStore, NestJS CQRS) |

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

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS (NestJS monorepo) — does architecture for real.

| Topic | Docita evidence |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Repository | `shared/common/repositories/base.repository.ts` (+ `prisma-read-base.ts`), per-domain repos bound via DI tokens (CI-enforced) |
| CQRS & DI | CQRS-lite command/query split in `domains/appointments/application/services/*`; constructor injection wired in every `*.module.ts` |
| Ports & Adapters (hexagonal) | `domains/*/application/ports/*` + `infrastructure/repositories/*`; cross-domain infrastructure imports blocked by CI checks |
| Anti-Corruption Layer | The whole `abdm` domain isolates India's ABDM government API behind its own core/application/presentation layers |
| Service Locator vs DI | Constructor injection chosen everywhere; no locator — registry-style lookups confined to strategy registries |
| Event Sourcing / Saga / MVC-MVP-MVVM | _No direct docita implementation yet._ (transactional outbox is the closest cousin to event-driven publishing) |
