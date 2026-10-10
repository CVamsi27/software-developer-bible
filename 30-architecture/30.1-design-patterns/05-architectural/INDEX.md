# Architectural Patterns

> **Study time:** ≈ 43 min of reading (9 files, ~5 min average).
> **9 files.** Modern, distributed-systems patterns plus DDD tactical design and UI architecture. These are NOT part of the original GoF set — they emerged as software engineering evolved to handle scale, distributed systems, domain-driven design, and rich frontends.

[![Files](https://img.shields.io/badge/files-9-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architectural-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What architectural patterns solve

GoF patterns describe collaborations among objects. This category extends the discussion to persistence, domain meaning, recoverable workflows and presentation boundaries. Some choices remain inside one process; others cross databases and deployment units. Distribution is a consequence of the chosen boundary, not a requirement for every pattern.

These show up heavily in:
- Senior backend / staff engineer interviews
- System design rounds
- Microservices and distributed systems discussions
- Domain-driven design conversations

---

## The 8 patterns

| # | Pattern | Intent | Use when | Avoid when | Role priority | General importance |
| --: | --------- | -------- | ---------- | ------------ | --- | --- |
| 1 | [Repository](30.1.5.01-repository.md) | Data access abstraction | Domain-oriented persistence contracts | Simple CRUD with one model | Important | Foundational |
| 2 | [CQRS & DI](30.1.5.02-cqrs-di.md) | Read/write separation + explicit dependencies | Complex domains, asymmetric read/write load | One read/write model already fits | Important | Specialized |
| 3 | [Event Sourcing](30.1.5.03-event-sourcing.md) | Store events, derive state | Accepted event history must be authoritative | Current records with audit/history satisfy the need | Important | Specialized |
| 4 | [Saga](30.1.5.04-saga.md) | Recoverable workflows across local commits | Multi-service business flows | Single DB transaction works | Important | Specialized |
| 5 | [DDD Tactical Patterns](30.1.5.05-ddd-tactical-patterns-aggregates-value-objects.md) | Entities, value objects, aggregate boundaries | Complex domains with invariants to enforce | CRUD apps without business rules | Important | Specialized |
| 6 | [Anti-Corruption Layer](30.1.5.06-anti-corruption-layer.md) | Isolate legacy/external models from your domain | Integrating legacy systems, vendors, strangler migrations | Models already share the required meaning | Important | Specialized |
| 7 | [Service Locator vs Dependency Injection](30.1.5.07-service-locator-vs-dependency-injection.md) | How dependencies get resolved | Understanding hidden deps, choosing a wiring strategy | A broad locator hides fixed requirements | Important | Foundational |
| 8 | [Presentation Patterns MVC/MVP/MVVM](30.1.5.08-presentation-patterns-mvc-mvp-mvvm.md) | Separating UI state, logic, and rendering | Frontend architecture discussions and refactors | Trivial static UIs | Important | Specialized |

---

## Read the boundaries in a useful order

Start with Repository and dependency wiring to identify where persistence and construction belong. Then use DDD and the Anti-Corruption Layer to define the model being protected. CQRS separates read/write responsibilities; Event Sourcing changes the authoritative record. Saga addresses recoverable coordination across local commits. Presentation patterns bring the same ownership questions to UI interaction.

Use the table to select the problem, then follow that chapter's concrete trace. The patterns compose where their contracts meet; they are not a package that every application must adopt.

---

## Decision flowchart

```
How is your data accessed / persisted?
│
├─ Just need data access abstraction? ──→ Repository
│
├─ Read and write models are very different? ──→ CQRS
│
├─ Need accepted events as the authoritative history? ──→ Event Sourcing
│
├─ Workflow accepts partial commits across services? ──→ Saga
│
├─ Complex domain with invariants to enforce? ──→ DDD Aggregates
│
├─ Legacy/vendor model polluting your domain? ──→ Anti-Corruption Layer
│
└─ Fixed collaborators? ──→ explicit DI; dynamic capability choice? → narrow registry
```

---

## How they compose

These patterns are often used together in real systems:

| Composition | What you get |
| ----------------------------------------------- | -------------------------------------------------------------------------- |
| **Repository + DI** | Domain persistence contracts; adapters still preserve database semantics |
| **CQRS + Event Sourcing** | Reads are projections of the event log; commands emit events |
| **CQRS + Saga** | Separate read/write roles within a recoverable workflow |
| **DDD Aggregates + Repository + Domain Events** | Invariant-enforcing boundaries feeding outbox-driven integrations |
| **ACL + Strangler Fig** | Translation seams for incrementally replacing legacy systems |
| **Selective composition** | Boundaries matched to the actual invariants and operational needs |

---

## When NOT to use architectural patterns

**Choose each boundary for a demonstrated problem, including in an early product. Plain dependency injection or a focused repository can be small; distributed projections and workflows introduce larger operational responsibilities.** Choose them when:
- You've identified a specific problem (read/write asymmetry, audit, distributed tx)
- You have team capacity to maintain the new moving parts
- The scale or compliance requirement justifies the cost

For a CRUD blog with straightforward queries and no need for authoritative event history, ordinary persistence is usually easier to maintain. Justify each added boundary by the requirement it serves.

---

## Reading Path and Completion Check

Start with Repository and explicit dependencies, then domain boundaries. Read CQRS and event sourcing before saga coordination; finish by comparing presentation boundaries.

Explain which changes must succeed together to preserve a rule, when events are safely stored, and which failures across service boundaries require an action that reverses or offsets earlier work. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

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
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Repository | `shared/common/repositories/base.repository.ts` (+ `prisma-read-base.ts`), per-domain repos bound via DI tokens (CI-enforced) |
| CQRS & DI | CQRS-lite command/query split in `domains/appointments/application/services/*`; explicit constructor/provider wiring; inspect the relevant module |
| Ports & Adapters (hexagonal) | `domains/*/application/ports/*` + `infrastructure/repositories/*`; boundary-check scripts express restrictions; this review did not rerun Docita CI |
| Anti-Corruption Layer | `abdm/core/repositories/abdm.repository.interface.ts` and `abdm/infrastructure/abdm-abha.client.ts` show a local port and foreign client; inspect mappings before calling the whole integration an ACL |
| Service Locator vs DI | Constructor/provider wiring and focused registries are concrete examples; these pointers do not prove an exhaustive absence of service lookup |
| Event Sourcing / Saga / MVC-MVP-MVVM | Transactional outbox is a related publishing mechanism; these pointers do not establish or rule out authoritative event history, durable saga coordination or a presentation pattern |
