# Design Patterns — Index

> **20 files** — 4 foundational theory files (SOLID, DRY/KISS/YAGNI, OOP concepts, UML basics) + 16 GoF and enterprise design patterns from Singleton and Factory to CQRS, dependency injection, module, state machines, and interview questions.

[![Files](https://img.shields.io/badge/files-20-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

**Read the theory first.** The 4 `00-*` files below cover the principles and concepts you need to know. Then read the GoF patterns for applied examples.

---

## Foundational Theory (read these first)

| # | File | Concepts covered | Why it matters |
|---|------|------------------|----------------|
| 00 | [SOLID Principles](00-SOLID-Principles.md) | SRP, OCP, LSP, ISP, DIP — the 5 principles every OOP design should follow | Foundation of every GoF pattern. Most LLD questions test these. |
| 00 | [DRY, KISS, YAGNI & More](00-DRY-KISS-YAGNI.md) | DRY, KISS, YAGNI, Rule of Three, Composition over Inheritance, POLA, SoC | The other 6 principles that show up in code reviews and LLD. |
| 00 | [OOP Concepts](00-OOP-Concepts.md) | Encapsulation, inheritance, polymorphism, abstraction, association, aggregation, composition | The 4 pillars. Plus the "has-a" relationships that come up in class diagrams. |
| 00 | [UML Basics](00-UML-Basics.md) | Class diagram, sequence diagram, relationships, multiplicities | Visualize your design. LLD interviews expect you to draw these on a whiteboard. |

---

## GoF and Enterprise Patterns

| # | File | Topics |
|---|------|--------|
| 01 | [Singleton](01-Singleton.md) | Lazy/eager initialization, thread safety, enum singleton, use cases |
| 02 | [Factory](02-Factory.md) | Simple factory, factory method, abstract factory, when to use |
| 03 | [Strategy](03-Strategy.md) | Strategy pattern, dependency inversion, functional alternatives |
| 04 | [Observer](04-Observer.md) | Subject/observer, event emitters, pub/sub, reactive patterns |
| 05 | [Repository](05-Repository.md) | Data access abstraction, ORM integration, testing benefits |
| 06 | [Builder](06-Builder.md) | Builder pattern, fluent interfaces, immutable objects |
| 07 | [Adapter](07-Adapter.md) | Class adapter, object adapter, integration patterns |
| 08 | [Facade](08-Facade.md) | Simplified interfaces, subsystem hiding, API wrapping |
| 09 | [Decorator](09-Decorator.md) | Wrapper pattern, TypeScript decorators, mixin composition |
| 10 | [Proxy](10-Proxy.md) | Virtual proxy, protection proxy, caching proxy, lazy loading |
| 11 | [Chain of Responsibility](11-Chain-of-Responsibility.md) | Middleware chains, request processing, handler pipelines |
| 12 | [CQRS & DI](12-CQRS-DI.md) | Command/query separation, dependency injection containers |
| 14 | [Module Pattern](14-Module-Pattern.md) | ES modules, IIFE, revealing module, tree-shaking, barrels |
| 15 | [State Pattern & State Machines](15-State-Pattern.md) | Discriminated unions, XState, statecharts, transition functions |
| 16 | [Interview Questions](16-Interview-Questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [NestJS (DI)](../06-NestJS/) | [JavaScript](../../10-Frontend-Stack/01-JavaScript/) | [System Design](../../30-Architecture-Stack/11-System-Design/) | [Coding Patterns](../../70-Interview-Toolkit/19-Coding-Patterns/)
---

## Navigation

[← Previous: Security](../09-Security/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: System Design →](../../30-Architecture-Stack/11-System-Design/INDEX.md)
