# Behavioral Patterns

> **Study time:** ≈ 1 h 2 m of reading (13 files, ~5 min average).
> **13 files.** Object collaboration. These patterns are about algorithms and the assignment of responsibilities between objects. They characterize complex control flow that's harder to follow at runtime.

[![Files](https://img.shields.io/badge/files-13-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Behavioral-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What behavioral patterns solve

Creational and structural patterns are about "what" (objects) and "how" (composition). Behavioral patterns are about "who does what" — they manage algorithms, responsibilities, and the flow of communication between objects.

### Common signals you need one

- "I have a `switch` on type to decide which algorithm to run."
- "My objects are tightly coupled — every one knows about every other."
- "I need to undo/redo operations."
- "I have a complex state machine, and `if/else` is unmaintainable."
- "I need to traverse a collection without exposing its internals."

---

## The 12 patterns

| # | Pattern | Intent | Use when | Avoid when | Role priority | General importance |
| --: | --------- | -------- | ---------- | ------------ | --- | --- |
| 1 | [Strategy](30.1.4.01-strategy.md) | Delegate to selected interchangeable policies | Multiple ways to do the same thing | Only one algorithm ever | Important | Foundational |
| 2 | [Observer](30.1.4.02-observer.md) | One-to-many change notification | A local subject has multiple subscribers | Durable cross-process delivery is required without a broker | Important | Foundational |
| 3 | [Chain of Responsibility](30.1.4.03-chain-of-responsibility.md) | Route through ordered potential receivers | Several handlers may claim or forward a request | The receiver is already known and order adds no policy | Important | Specialized |
| 4 | [State](30.1.4.04-state.md) | Keep legal lifecycle transitions explicit | Orders, requests, protocol states | One state-dependent branch with no evolving lifecycle | Important | Specialized |
| 5 | [Template Method](30.1.4.05-template-method.md) | Skeleton + customizable steps | Algorithm with varying steps | Algorithm is fully fixed | Important | Specialized |
| 6 | [Iterator](30.1.4.06-iterator.md) | Sequential access without exposing internals | Collections, lazy sequences | Existing iteration already satisfies the traversal contract | Important | Specialized |
| 7 | [Mediator](30.1.4.07-mediator.md) | Central authority for object communication | Many-to-many object interactions, dialog boxes | Few objects, direct refs are fine | Important | Specialized |
| 8 | [Memento](30.1.4.08-memento.md) | Capture/restore internal state | Undo and recoverable snapshots | No history needed | Important | Specialized |
| 9 | [Command](30.1.4.09-command.md) | Encapsulate a request as an object | Undo/redo, queueing, macro recording, transactional ops | Simple one-shot operations | Important | Specialized |
| 10 | [Visitor](30.1.4.10-visitor.md) | Add operations without modifying classes | ASTs, compilers, complex object structures | Class hierarchy is unstable | Important | Specialized |
| 11 | [Interpreter](30.1.4.11-interpreter.md) | Grammar + interpreter for a DSL | DSLs, config formats, regex-like languages | A standard language implementation is already suitable | Important | Specialized |
| 12 | [Null Object](30.1.4.12-null-object.md) | Encapsulated no-op behavior instead of null | Sensible neutral defaults (no-op loggers), branch-free chains | Absence must surface (silence hides bugs) | Important | Specialized |

---

## Follow responsibility through the system

Start with Strategy and State: one chooses a policy, the other constrains lifecycle behavior. Observer introduces delivery and cleanup; Chain and Mediator show where routing and coordination live. Template Method owns a fixed sequence. Command and Memento separate requested actions from recoverable state. Iterator, Visitor and Interpreter then separate traversal, operations and meaning.

The table is a map to the relevant chapter. Read a chapter's execution trace before comparing it with its neighbor.

---

## Decision flowchart

```
Need to manage object interaction / control flow?
│
├─ Select an interchangeable policy (at startup or per operation)? ──→ Strategy
│
├─ Notify many objects of state changes? ──→ Observer
│
├─ Pass a request along a chain of handlers? ──→ Chain of Responsibility
│
├─ Behavior changes with internal state? ──→ State
│
├─ Same algorithm skeleton, varying steps? ──→ Template Method
│
├─ Sequentially access elements without exposing internals? ──→ Iterator
│
├─ Centralize complex object interactions? ──→ Mediator
│
├─ Save / restore state (undo)? ──→ Memento
│
├─ Encapsulate a request (queue, undo, log)? ──→ Command
│
├─ Add operations without modifying class structure? ──→ Visitor
│
├─ Interpret a grammar / DSL? ──→ Interpreter
│
└─ Need a harmless default instead of null? ──→ Null Object
```

---

## Comparisons

### Strategy vs State

| Property | Strategy | State |
| -- | ---------- | ------- |
| **Who chooses** | Client / context picks strategy | Defined lifecycle transitions govern state |
| **Selection lifetime** | Per operation or retained by the caller | Often a state machine with transitions |
| **Awareness of each other** | Strategies usually don't know about each other | States often trigger transitions to other states |
| **Intent** | "How to do this" | "What am I currently doing" |

Use intent: selected policy versus lifecycle-dependent behavior. References between objects alone do not identify either pattern.

### Observer vs Mediator

- **Observer** is a **one-to-many** notification system. The subject retains registrations without depending on concrete observer classes.
- **Mediator** is a **many-to-many** coordinator. Colleagues know the mediator, not each other.

Use Observer when one thing changes and many react. Use Mediator when many things collaborate and you want to centralize the rules.

### Command vs Memento

- **Command** stores the **action** to perform (do/undo).
- **Memento** stores the **state** to restore to.

Use Command for "do this later" / "undo what I did". Use Memento for "go back to this snapshot".

### Iterator vs Visitor

- **Iterator** traverses a structure (reads elements).
- **Visitor** performs operations on a structure's elements (transforms / inspects).

Both work on composite structures. Iterator is about *movement*, Visitor is about *work*.

### Chain of Responsibility vs Decorator

- **CoR** defines forwarding and termination across handlers; middleware variants may run several.
- **Decorator** adds behavior around a wrapped interface; its contract determines delegation.

Both chain-call. Explain the handling or wrapping intention and the actual stopping rule.

### Null Object vs Optional

- **Null Object** encodes *what to do* when absent — the neutral response lives inside the object.
- **`Optional<T>`** encodes *that* something may be absent — callers use its explicit value/absence API; the type system does not prove they handle every case correctly.

They compose: resolve `Optional` to a real-or-null-object at the boundary, then keep the domain branch-free. Choose whether absence is an outcome the caller must see or an agreed neutral capability; the representation follows that meaning.

---

## When NOT to use behavioral patterns

- **Strategy** for a single algorithm — just write the function.
- **Observer** when one stable direct collaboration already expresses the delivery and lifetime contract.
- **CoR** when there's exactly one handler — just call it.
- **State objects** when a small explicit union and transition function expresses the rules clearly.
- **Template Method** when the inheritance contract is unstable; consider injected steps.
- **Custom iterator classes** when existing `for...of` or generators already express the traversal.
- **Mediator** when interaction is already simple and direct references are clear.
- **Memento** if undo isn't a requirement.
- **Command** for one-shot operations with no queue/undo.
- **Visitor** if the object structure changes often (you'll rewrite all visitors).
- Do not make a tiny **Interpreter** example stand in for complex parsing. A parser generator can help syntax processing; evaluation still needs semantic rules.
- **Null Object** where silence would hide a bug (money, auth, load failures) — let absence throw or return `Optional` instead.

---

## Reading Path and Completion Check

Start with Strategy, State and Observer to separate policy, lifecycle and notifications. Then follow request routing and coordination before undo, traversal and language patterns.

Trace one request or transition across collaborators and identify who owns ordering, failure and cleanup. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [Foundations](../01-foundations/INDEX.md) — OOP concepts and SOLID are prerequisites.
- [Structural Patterns](../03-structural/INDEX.md) — Iterator often traverses a Composite; Visitor does too.
- [Architectural Patterns](../05-architectural/INDEX.md) — CQRS separates writes from reads; Command can represent write requests, while Event Sourcing chooses an authoritative history.

---

## Navigation

[← Structural Patterns](../03-structural/INDEX.md) · [↑ Design Patterns Home](../INDEX.md) · [Next: Architectural Patterns →](../05-architectural/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS (NestJS monorepo) — collaborates for real.

| Topic | Docita evidence |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strategy | Import strategies (`apps/api/src/shared/modules/imports/strategies/patient-import.strategy.ts`…) and search strategies (`search/strategies/*-search.strategy.ts`) behind registries |
| Template Method | `apps/api/src/shared/modules/document-generation/pdf/base-pdf.service.ts`, `websockets/base-websocket.gateway.ts`, `apps/api/src/shared/modules/queue/base-pdf.processor.ts`, `search-strategy.base.ts` |
| Observer / domain events | `shared/common/events/{domain-events,event.service}.ts`, `ops-alert.listener.ts`, transactional outbox (`outbox-relay.scheduler.ts`, ADR 0010) |
| Command (CQRS-lite) | `appointment-command.service.ts` vs `appointment-query.service.ts` (+ queue/follow-up twins); queue jobs as command objects |
| Chain of Responsibility | Nest guard→interceptor→pipe request pipeline (tenant-context, CSRF, rate-limit) |
| Null Object | These pointers do not constitute an exhaustive implementation audit or prove absence of a neutral implementation. |
