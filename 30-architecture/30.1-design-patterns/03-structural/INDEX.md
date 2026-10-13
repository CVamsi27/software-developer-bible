# Structural Patterns

> **Study time:** ≈ 1 h 6 m of reading (9 files, ~7 min average).
> **9 files.** Class and object composition. These patterns are about how to assemble larger structures from classes and objects while keeping the structure flexible and efficient.

[![Files](https://img.shields.io/badge/files-9-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Structural-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What structural patterns solve

Inheritance couples a subtype to a base contract and implementation. Structural patterns let you compose objects at runtime to get new functionality, instead of baking it into a class hierarchy.

### Common signals you need one

- "I need to use a 3rd-party class but its interface doesn't match mine."
- "I want to add behavior to an object without affecting other instances of the same class."
- "I have a complex subsystem and want a single, simple entry point."
- "Loading this object is expensive — I want lazy / cached / proxied access."

---

## The 8 patterns

| # | Pattern | Intent | Use when | Avoid when | Role priority | General importance |
| --: | --------- | -------- | ---------- | ------------ | --- | --- |
| 1 | [Adapter](30.1.3.01-adapter.md) | Translate an existing interface to the client's contract | 3rd-party SDK, legacy integration | Refactoring both sides already preserves compatibility | Important | Foundational |
| 2 | [Facade](30.1.3.02-facade.md) | Simplify common access to a complex subsystem | Library/SDK, multi-subsystem workflow | Single subsystem, already simple | Important | Specialized |
| 3 | [Decorator](30.1.3.03-decorator.md) | Add a responsibility around a component | Per-instance logging, metrics or transformation | Wrapper order obscures the contract | Important | Specialized |
| 4 | [Proxy](30.1.3.04-proxy.md) | Controlled access (lazy, protection, remote, caching) | Image/DB lazy loading, RBAC checks, network stubs | Direct access is fine | Important | Specialized |
| 5 | [Module](30.1.3.05-module-pattern.md) | Encapsulation at the file level | File/package visibility boundaries | N/A | Important | Specialized |
| 6 | [Composite](30.1.3.06-composite.md) | Apply shared operations across a part-whole tree | File and directory aggregation, AST operations, nested menus | Flat data or no meaningful common operation | Important | Specialized |
| 7 | [Bridge](30.1.3.07-bridge.md) | Decouple abstraction from implementation | Multiple dimensions of variation (shape × color × renderer) | One dimension, stable axis | Important | Specialized |
| 8 | [Flyweight](30.1.3.08-flyweight.md) | Share state to support many fine-grained objects | Text rendering (chars), particle systems, glyph caches | Few objects, no memory pressure | Important | Specialized |

---

## Start with the boundary

Read Adapter and Facade first: one reconciles an interface, the other exposes a simpler subsystem entry point. Then compare Decorator and Proxy using the same wrapper shape but different intentions. Module establishes visibility boundaries; Composite, Bridge and Flyweight address trees, independent variation and shared state respectively.

The linked chapters each provide a concrete trace. Use the table above to choose a chapter rather than rereading eight definitions here.

---

## Decision flowchart

```
Need to combine / wrap / control access to objects?
│
├─ Make incompatible interfaces work together? ──→ Adapter
│
├─ Provide a simple API over a complex subsystem? ──→ Facade
│
├─ Add behavior to an object without subclassing? ──→ Decorator
│
├─ Control access (lazy, auth, cache, remote)? ──→ Proxy
│
├─ Recursive tree of part-whole objects? ──→ Composite
│
├─ Two independent dimensions of variation? ──→ Bridge
│
├─ Thousands of similar objects, memory matters? ──→ Flyweight
│
└─ Encapsulate code at the file/module level? ──→ Module
```

---

## Comparisons

### Adapter vs Decorator vs Proxy

These three look similar — they all wrap an object — but intent differs:

| Property | Adapter | Decorator | Proxy |
| -- | --------- | ----------- | -------- |
| **Intent** | Make incompatible interface work | Add new behavior | Control access |
| **Interface** | Translates the interface | Preserves the component contract | Preserves the subject contract |
| **Call-path decision** | Translate the required contract | Delegate or short-circuit under the component promise | Gate, delay, route, or reuse under the subject promise |
| **Knows about clients** | No | No | Usually not, but can (auth proxy) |
| **Example** | Wrap Stripe API in your `PaymentProvider` | Wrap a service with a logging object | Wrap a DB row for lazy loading |

A common interview trap: "What's the difference between Decorator and Proxy?" The answer is **intent** — Decorator wants to add behavior, Proxy wants to control access. In code they can be indistinguishable.

### Facade vs Adapter

- **Facade** simplifies common operations across a subsystem behind a higher-level entry point.
- **Adapter** translates an existing interface to a client's expected contract; mapping may include data, units, errors or optional values.

### Composite vs Decorator

- **Composite** is about **structure** (recursive tree, sum of parts behaves like a single).
- **Decorator** is about **behavior** (add responsibilities to a single object without affecting others).

Both use recursive composition, but Composite's recursion is structural, Decorator's is behavioral.

### Module vs Facade

- **Module** organizes code at the file/package level (language-level encapsulation).
- **Facade** is a client-facing entry point that coordinates subsystem behavior; it can be a class, function or module export.

Modern TS: a `module.ts` file often *contains* a Facade.

---

## When NOT to use structural patterns

- **Adapter** when directly changing both sides preserves compatibility more simply. A migration can still require an adapter even when both sides are owned.
- **Facade** when the subsystem is small and the client already knows it.
- **Decorator** when wrapper order and interactions make the contract harder to understand than explicit configuration.
- **Proxy** when the indirection adds no meaningful access or lifecycle boundary.
- **Composite** when the structure is flat and never recursive.
- **Bridge** when there is no independently varying implementation axis.
- **Flyweight** when measured state sharing does not justify lookup, lifetime and indirection costs.
- **Module** implemented with extra IIFE ceremony when ES modules already provide the required boundary.

---

## Reading Path and Completion Check

Compare Adapter, Facade, Decorator and Proxy as wrappers with different intentions. Then move to Module, Composite, Bridge and Flyweight as larger structural decisions.

Explain a wrapper by its contract and a shared/tree structure by the state it owns; avoid choosing by class shape alone. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [Foundations](../01-foundations/INDEX.md) — DIP and ISP make these patterns click.
- [Creational Patterns](../02-creational/INDEX.md) — Facade often hides a Factory.
- [Behavioral Patterns](../04-behavioral/INDEX.md) — Composite and Decorator both use recursive composition; Iterator works on Composite.

---

## Navigation

[← Creational Patterns](../02-creational/INDEX.md) · [↑ Design Patterns Home](../INDEX.md) · [Next: Behavioral Patterns →](../04-behavioral/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS (NestJS monorepo) — wraps and composes for real.

| Topic | Docita evidence |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Facade | `shared/modules/imports/ocr-facade.service.ts` hides the OCR pipeline; `shared/whatsapp/templates-facade.service.ts` hides template resolution — construction/delegation guard source: `scripts/checks/check-facade-delegation.mjs` |
| Adapter | India's ABDM government API wrapped by `domains/abdm/infrastructure/abdm-abha.client.ts`; Razorpay SDK behind `payments/infrastructure/adapters/razorpay/` |
| Decorator (framework-shaped) | NestJS interceptor/guard pipelines in `shared/common/interceptors/*` add logging, CSRF, tenant-context around handlers |
| Module | ES module scope and curated entry points; a barrel alone does not enforce every import boundary |
| Proxy / Flyweight / Composite / Bridge | No exhaustive implementation audit is implied by these pointers; confirm a claimed GoF mechanism in the actual source. |
