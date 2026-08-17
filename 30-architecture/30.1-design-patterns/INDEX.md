# Design Patterns — Index

> **19 files** — 4 foundational theory files (SOLID, DRY/KISS/YAGNI, OOP concepts, UML basics) + 15 GoF and enterprise design patterns from Singleton and Factory to CQRS, dependency injection, module, state machines, and interview questions.

[![Files](https://img.shields.io/badge/files-19-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Read the theory first.** The 4 `00-*` files below cover the principles and concepts you need to know. Then read the GoF patterns for applied examples.

---

## Foundational Theory (read these first)

| # | File | Concepts covered | Why it matters |
|---|------|------------------|----------------|
| 00 | [SOLID Principles](30.1.01-solid-principles.md) | SRP, OCP, LSP, ISP, DIP — the 5 principles every OOP design should follow | Foundation of every GoF pattern. Most LLD questions test these. |
| 00 | [DRY, KISS, YAGNI & More](30.1.02-dry-kiss-yagni.md) | DRY, KISS, YAGNI, Rule of Three, Composition over Inheritance, POLA, SoC | The other 6 principles that show up in code reviews and LLD. |
| 00 | [OOP Concepts](30.1.03-oop-concepts.md) | Encapsulation, inheritance, polymorphism, abstraction, association, aggregation, composition | The 4 pillars. Plus the "has-a" relationships that come up in class diagrams. |
| 00 | [UML Basics](30.1.04-uml-basics.md) | Class diagram, sequence diagram, relationships, multiplicities | Visualize your design. LLD interviews expect you to draw these on a whiteboard. |

---

## GoF and Enterprise Patterns

| # | File | Topics |
|---|------|--------|
| 01 | [Singleton](30.1.05-singleton.md) | Lazy/eager initialization, thread safety, enum singleton, use cases |
| 02 | [Factory](30.1.06-factory.md) | Simple factory, factory method, abstract factory, when to use |
| 03 | [Strategy](30.1.07-strategy.md) | Strategy pattern, dependency inversion, functional alternatives |
| 04 | [Observer](30.1.08-observer.md) | Subject/observer, event emitters, pub/sub, reactive patterns |
| 05 | [Repository](30.1.09-repository.md) | Data access abstraction, ORM integration, testing benefits |
| 06 | [Builder](30.1.10-builder.md) | Builder pattern, fluent interfaces, immutable objects |
| 07 | [Adapter](30.1.11-adapter.md) | Class adapter, object adapter, integration patterns |
| 08 | [Facade](30.1.12-facade.md) | Simplified interfaces, subsystem hiding, API wrapping |
| 09 | [Decorator](30.1.13-decorator.md) | Wrapper pattern, TypeScript decorators, mixin composition |
| 10 | [Proxy](30.1.14-proxy.md) | Virtual proxy, protection proxy, caching proxy, lazy loading |
| 11 | [Chain of Responsibility](30.1.15-chain-of-responsibility.md) | Middleware chains, request processing, handler pipelines |
| 12 | [CQRS & DI](30.1.16-cqrs-di.md) | Command/query separation, dependency injection containers |
| 14 | [Module Pattern](30.1.17-module-pattern.md) | ES modules, IIFE, revealing module, tree-shaking, barrels |
| 15 | [State Pattern & State Machines](30.1.18-state-pattern.md) | Discriminated unions, XState, statecharts, transition functions |
| 16 | [Interview Questions](30.1.19-interview-questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [NestJS (DI)](../../20-backend/INDEX.md) | [JavaScript](../../10-frontend/10.1-javascript/INDEX.md) | [System Design](../30.2-system-design/INDEX.md) | [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md)
---

## Navigation

[← Previous: Architecture Index](../INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: System Design →](../30.2-system-design/INDEX.md)
