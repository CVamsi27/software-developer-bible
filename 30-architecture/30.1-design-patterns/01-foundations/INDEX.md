# Foundations — Principles, OOP & UML

> **Study time:** ≈ 1 h 9 m of reading (5 files, ~14 min average).
> **5 files.** Read these BEFORE any design pattern. SOLID, OOP, and UML are the language every GoF pattern is written in. Use them to explain the state, caller promises, and relationships a pattern is meant to protect.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this folder exists

Begin with state ownership and caller contracts. Then assess a real change using SOLID and other design heuristics. Finally, draw the relationships and trace success plus a failure in UML. A named pattern is useful when its mechanism resolves one of these concrete problems.

**Read order:** OOP → SOLID → Other principles → UML.

| Order | File | Time | What it unlocks | Role priority | General importance |
| ----: | ------------------------------------------------------ | -----: | ----------------------------------------------------------------------------------- | ------------- | ------------------ |
| 1 | [OOP Concepts](30.1.1.03-oop-concepts.md) | 25 min | The 4 pillars + "has-a" relationships | Important | Specialized |
| 2 | [SOLID Principles](30.1.1.01-solid-principles.md) | 30 min | Five heuristics for evaluating dependency and change boundaries | Important | Foundational |
| 3 | [DRY, KISS, YAGNI & More](30.1.1.02-dry-kiss-yagni.md) | 20 min | Decide when knowledge should be shared and which complexity a requirement justifies | Important | Foundational |
| 4 | [UML Basics](30.1.1.04-uml-basics.md) | 25 min | Sketch class & sequence diagrams on a whiteboard | Important | Specialized |

**Total: ~1.5 hours** to read all 4 once. After that, treat them as a reference.

---

## File Index

### [SOLID Principles](30.1.1.01-solid-principles.md)
Five diagnostics for responsibility, extension, substitution, client contracts, and dependency direction. Apply them to a concrete change rather than treating interface counts as design quality.

- **SRP** — Single Responsibility Principle: one reason to change
- **OCP** — Open/Closed: open for extension, closed for modification
- **LSP** — Liskov Substitution: subtypes must be substitutable
- **ISP** — Interface Segregation: clients depend on the operations they need
- **DIP** — Dependency Inversion: depend on abstractions, not concretions

### [DRY, KISS, YAGNI & More](30.1.1.02-dry-kiss-yagni.md)
Heuristics for comparing coordination, reading, maintenance, and speculative-feature costs.

- **DRY** — Don't Repeat Yourself
- **KISS** — Keep It Simple, Stupid
- **YAGNI** — You Aren't Gonna Need It
- **Rule of Three** — a third case often clarifies variation; not a mandatory threshold
- **Composition over Inheritance** — delegate reuse when a behavioral subtype promise is unnecessary
- **POLA** — Principle of Least Astonishment
- **SoC** — Separation of Concerns

### [OOP Concepts](30.1.1.03-oop-concepts.md)
State invariants, caller contracts, dispatch, and explicitly modeled ownership.

- **Encapsulation** — hide state behind behavior
- **Inheritance** — a subtype relationship whose behavior must satisfy the caller contract
- **Polymorphism** — same interface, different behavior
- **Abstraction** — hide complexity behind a simple interface
- **Association, Aggregation, Composition** — distinguish references, grouping, and modeled ownership

### [UML Basics](30.1.1.04-uml-basics.md)
The visual language of software design. LLD interviews expect you to sketch these on a whiteboard.

- **Class diagrams** — classes, attributes, methods, relationships, multiplicities
- **Sequence diagrams** — object interactions over time
- **When to use which** — class for structure, sequence for behavior

---

## Use foundations to evaluate a pattern

| Foundation | Patterns to examine | Interview question it answers |
| ----------------- | ------------------------------------------------- | --------------------------------------------------------------- |
| **SRP** | Facade, Mediator, Module | "Why is this class 2000 lines?" |
| **OCP** | Strategy, Decorator, Chain of Responsibility | "How do you add a new behavior without breaking existing code?" |
| **LSP** | Template Method, Composite, Iterator | "Can I substitute subtype X for parent Y?" |
| **ISP** | Adapter, Proxy | "Why is your interface 30 methods?" |
| **DIP** | Factory, Abstract Factory, DI, Repository | "How do you make this testable?" |
| **OOP contracts** | Patterns using state, subtyping, or collaborators | "Is pattern X inheritance or composition?" |
| **UML** | — | "Draw the class diagram for the parking lot LLD." |

---

## Reading Path and Completion Check

Read object behavior before design heuristics, then use UML to make one concrete interaction visible. Revisit SOLID and DRY/KISS/YAGNI against that example.

Show one case where applying a principle reduces change cost and one where it adds unnecessary abstraction. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Navigation

[← Design Patterns Home](../INDEX.md) · [Next: Creational Patterns →](../02-creational/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS (NestJS monorepo) — exercises these foundations in real code.

| Topic | Docita evidence |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DIP / Dependency Inversion | Repository token and constructor-injection checks in `scripts/checks/check-repository-di-tokens.mjs` |
| OCP | Strategy registries (`search-strategy.registry.ts`, `bulk-import-strategy.registry.ts`) — examples of registration boundaries; callers still need stable strategy contracts |
| SRP | Command/query service split: `appointment-command.service.ts` vs `appointment-query.service.ts` |
| ISP | Narrow per-domain ports: `domains/*/application/ports/*`, `shared/common/ports/clock.port.ts` |
| SoC / module boundaries | Domain layout enforced in CI by `scripts/checks/check-api-domain-layout.mjs` + cross-domain import checks |
