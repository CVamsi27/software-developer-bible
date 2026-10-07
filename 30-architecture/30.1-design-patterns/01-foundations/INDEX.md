# Foundations — Principles, OOP & UML

> **Study time:** ≈ 1 h 5 m of reading (5 files, ~13 min average).
> **5 files.** Read these BEFORE any design pattern. SOLID, OOP, and UML are the language every GoF pattern is written in. Without them, the patterns are unmotivated syntax.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this folder exists

Many questions about a design pattern examine: "How does this pattern help you follow SOLID?" or "What's the OOP concept at work here?" If you can't answer those, the pattern name is meaningless.

**Read order:** OOP → SOLID → Other principles → UML.

| Order | File | Time | What it unlocks | Role priority | General importance |
| ----: | ------------------------------------------------------ | -----: | --------------------------------------------------------------- | ------------- | ------------------ |
| 1 | [SOLID Principles](30.1.1.01-solid-principles.md) | 30 min | Five heuristics for evaluating dependency and change boundaries | Important | Foundational |
| 2 | [DRY, KISS, YAGNI & More](30.1.1.02-dry-kiss-yagni.md) | 20 min | The other 6 principles that show up in code review | Important | Foundational |
| 3 | [OOP Concepts](30.1.1.03-oop-concepts.md) | 25 min | The 4 pillars + "has-a" relationships | Important | Specialized |
| 4 | [UML Basics](30.1.1.04-uml-basics.md) | 25 min | Sketch class & sequence diagrams on a whiteboard | Important | Specialized |

**Total: ~1.5 hours** to read all 4 once. After that, treat them as a reference.

---

## File Index

### [SOLID Principles](30.1.1.01-solid-principles.md)
The 5 principles every OOP design should follow. The basis of most design patterns. Most LLD interviews test these directly.

- **SRP** — Single Responsibility Principle: one reason to change
- **OCP** — Open/Closed: open for extension, closed for modification
- **LSP** — Liskov Substitution: subtypes must be substitutable
- **ISP** — Interface Segregation: many small interfaces > one fat interface
- **DIP** — Dependency Inversion: depend on abstractions, not concretions

### [DRY, KISS, YAGNI & More](30.1.1.02-dry-kiss-yagni.md)
The "other 6" principles that show up in code reviews and LLD interviews.

- **DRY** — Don't Repeat Yourself
- **KISS** — Keep It Simple, Stupid
- **YAGNI** — You Aren't Gonna Need It
- **Rule of Three** — a third case often clarifies variation; not a mandatory threshold
- **Composition over Inheritance** — favor "has-a" over "is-a"
- **POLA** — Principle of Least Astonishment
- **SoC** — Separation of Concerns

### [OOP Concepts](30.1.1.03-oop-concepts.md)
The 4 pillars + the "has-a" relationships that show up in class diagrams.

- **Encapsulation** — hide state behind behavior
- **Inheritance** — "is-a" (use sparingly)
- **Polymorphism** — same interface, different behavior
- **Abstraction** — hide complexity behind a simple interface
- **Association, Aggregation, Composition** — the 3 flavors of "has-a"

### [UML Basics](30.1.1.04-uml-basics.md)
The visual language of software design. LLD interviews expect you to sketch these on a whiteboard.

- **Class diagrams** — classes, attributes, methods, relationships, multiplicities
- **Sequence diagrams** — object interactions over time
- **When to use which** — class for structure, sequence for behavior

---

## How foundations map to the rest of the patterns

| Foundation | Patterns it makes possible | Interview question it answers |
| --------------- | -------------------------------------------- | --------------------------------------------------------------- |
| **SRP** | Facade, Mediator, Module | "Why is this class 2000 lines?" |
| **OCP** | Strategy, Decorator, Chain of Responsibility | "How do you add a new behavior without breaking existing code?" |
| **LSP** | Template Method, Composite, Iterator | "Can I substitute subtype X for parent Y?" |
| **ISP** | Adapter, Proxy | "Why is your interface 30 methods?" |
| **DIP** | Factory, Abstract Factory, DI, Repository | "How do you make this testable?" |
| **OOP pillars** | Every pattern | "Is pattern X inheritance or composition?" |
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
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| DIP / Dependency Inversion | Constructor injection throughout; repositories bound to DI tokens and enforced by `scripts/checks/check-repository-di-tokens.mjs` |
| OCP | Strategy registries (`search-strategy.registry.ts`, `bulk-import-strategy.registry.ts`) — new behavior is registered, not edited in |
| SRP | Command/query service split: `appointment-command.service.ts` vs `appointment-query.service.ts` |
| ISP | Narrow per-domain ports: `domains/*/application/ports/*`, `shared/common/ports/clock.port.ts` |
| SoC / module boundaries | Domain layout enforced in CI by `scripts/checks/check-api-domain-layout.mjs` + cross-domain import checks |
