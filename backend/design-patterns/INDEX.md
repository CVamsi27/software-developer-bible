# Design Patterns — Index

> **20 files** — 4 foundational theory files (SOLID, DRY/KISS/YAGNI, OOP concepts, UML basics) + 16 GoF and enterprise design patterns from Singleton and Factory to CQRS, dependency injection, module, state machines, and interview questions.

[![Files](https://img.shields.io/badge/files-19-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

**Read the theory first.** The 4 `00-*` files below cover the principles and concepts you need to know. Then read the GoF patterns for applied examples.

---

## Foundational Theory (read these first)

| # | File | Concepts covered | Why it matters |
|---|------|------------------|----------------|
| 00 | [SOLID Principles](solid-principles.md) | SRP, OCP, LSP, ISP, DIP — the 5 principles every OOP design should follow | Foundation of every GoF pattern. Most LLD questions test these. |
| 00 | [DRY, KISS, YAGNI & More](dry-kiss-yagni.md) | DRY, KISS, YAGNI, Rule of Three, Composition over Inheritance, POLA, SoC | The other 6 principles that show up in code reviews and LLD. |
| 00 | [OOP Concepts](oop-concepts.md) | Encapsulation, inheritance, polymorphism, abstraction, association, aggregation, composition | The 4 pillars. Plus the "has-a" relationships that come up in class diagrams. |
| 00 | [UML Basics](uml-basics.md) | Class diagram, sequence diagram, relationships, multiplicities | Visualize your design. LLD interviews expect you to draw these on a whiteboard. |

---

## GoF and Enterprise Patterns

| # | File | Topics |
|---|------|--------|
| 01 | [Singleton](singleton.md) | Lazy/eager initialization, thread safety, enum singleton, use cases |
| 02 | [Factory](factory.md) | Simple factory, factory method, abstract factory, when to use |
| 03 | [Strategy](strategy.md) | Strategy pattern, dependency inversion, functional alternatives |
| 04 | [Observer](observer.md) | Subject/observer, event emitters, pub/sub, reactive patterns |
| 05 | [Repository](repository.md) | Data access abstraction, ORM integration, testing benefits |
| 06 | [Builder](builder.md) | Builder pattern, fluent interfaces, immutable objects |
| 07 | [Adapter](adapter.md) | Class adapter, object adapter, integration patterns |
| 08 | [Facade](facade.md) | Simplified interfaces, subsystem hiding, API wrapping |
| 09 | [Decorator](decorator.md) | Wrapper pattern, TypeScript decorators, mixin composition |
| 10 | [Proxy](proxy.md) | Virtual proxy, protection proxy, caching proxy, lazy loading |
| 11 | [Chain of Responsibility](chain-of-responsibility.md) | Middleware chains, request processing, handler pipelines |
| 12 | [CQRS & DI](cqrs-di.md) | Command/query separation, dependency injection containers |
| 14 | [Module Pattern](module-pattern.md) | ES modules, IIFE, revealing module, tree-shaking, barrels |
| 15 | [State Pattern & State Machines](state-pattern.md) | Discriminated unions, XState, statecharts, transition functions |
| 16 | [Interview Questions](interview-questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [NestJS (DI)](../../backend/) | [JavaScript](../../frontend/javascript/) | [System Design](../../architecture/system-design/) | [Coding Patterns](../../interview-toolkit/coding-patterns/)
---

## Navigation

[← Previous: Security](../security/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: System Design →](../../architecture/system-design/INDEX.md)
