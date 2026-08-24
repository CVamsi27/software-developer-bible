# Behavioral Patterns

> **11 files.** Object collaboration. These patterns are about algorithms and the assignment of responsibilities between objects. They characterize complex control flow that's harder to follow at runtime.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
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

## The 11 patterns

| # | Pattern | Intent | Use when | Avoid when |
|--:|---------|--------|----------|------------|
| 1 | [Strategy](30.1.31-strategy.md) | Swap algorithms at runtime | Multiple ways to do the same thing | Only one algorithm ever |
| 2 | [Observer](30.1.32-observer.md) | Event-driven notification | UI events, pub/sub, reactive streams | Tight coupling is acceptable |
| 3 | [Chain of Responsibility](30.1.33-chain-of-responsibility.md) | Pass request along a chain | Middleware, validation pipelines, exception handling | Single handler always |
| 4 | [State](30.1.34-state.md) | Behavior depends on state | State machines, workflow engines | Few states, no transitions |
| 5 | [Template Method](30.1.35-template-method.md) | Skeleton + customizable steps | Algorithm with varying steps | Algorithm is fully fixed |
| 6 | [Iterator](30.1.36-iterator.md) | Sequential access without exposing internals | Collections, lazy sequences | Trivial arrays |
| 7 | [Mediator](30.1.37-mediator.md) | Central authority for object communication | Many-to-many object interactions, dialog boxes | Few objects, direct refs are fine |
| 8 | [Memento](30.1.38-memento.md) | Capture/restore internal state | Undo, snapshots, transactions | No history needed |
| 9 | [Command](30.1.39-command.md) | Encapsulate a request as an object | Undo/redo, queueing, macro recording, transactional ops | Simple one-shot operations |
| 10 | [Visitor](30.1.40-visitor.md) | Add operations without modifying classes | ASTs, compilers, complex object structures | Class hierarchy is unstable |
| 11 | [Interpreter](30.1.41-interpreter.md) | Grammar + interpreter for a DSL | DSLs, config formats, regex-like languages | Performance-critical parsing |

---

## Pattern Index

### [Strategy](30.1.31-strategy.md)
Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**When to use:**
- Many related classes differ only in their behavior
- You need different variants of an algorithm
- An algorithm uses data that clients shouldn't know about
- A class defines many behaviors via conditional statements

**Real-world examples:** Payment processing (Stripe / PayPal / Braintree), sorting algorithms selectable at runtime, compression strategies (gzip / brotli / snappy), auth strategies (JWT / OAuth / API key), form validation rules.

### [Observer](30.1.32-observer.md)
Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**When to use:**
- An abstraction has two aspects, one dependent on the other
- Changing one object requires changing others, and you don't know how many
- An object should notify other objects without making assumptions about who they are
- You need event-driven / reactive behavior

**Real-world examples:** DOM event listeners, RxJS observables, Node `EventEmitter`, Vue 3 reactivity, Kafka pub/sub, WebSocket message handlers, database CDC (change data capture).

### [Chain of Responsibility](30.1.33-chain-of-responsibility.md)
Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.

**When to use:**
- More than one object can handle a request, and the handler isn't known a priori
- You want to issue a request to one of several objects without specifying the receiver explicitly
- The set of handlers should be configurable at runtime
- You want to send a request to one of several objects without knowing which one

**Real-world examples:** Express/Koa middleware, NestJS interceptors/pipes/guards, Spring Filter chain, OAuth scope validation, event bubbling in the DOM, customer support escalation.

### [State](30.1.34-state.md)
Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

**When to use:**
- An object's behavior depends on its state, and it must change behavior at runtime based on that state
- Operations have large, multipart conditional statements that depend on the object's state
- State-specific behavior is scattered across many methods

**Real-world examples:** TCP connection (LISTEN, SYN_SENT, ESTABLISHED, FIN_WAIT, CLOSED), vending machine, document workflow (DRAFT → REVIEW → APPROVED → PUBLISHED), order state, Promise lifecycle, Redux store.

### [Template Method](30.1.35-template-method.md) *(new)*
Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.

**When to use:**
- You want to implement the invariant parts of an algorithm once and leave the variant parts to subclasses
- Common behavior among subclasses should be factored and localized to avoid duplication
- Subclasses extend behavior by overriding certain steps, not the whole algorithm

**Real-world examples:** Jest/Vitest test runners (lifecycle: beforeAll → beforeEach → test → afterEach → afterAll), Express middleware execution, React class component lifecycle, build pipeline phases, NestJS request lifecycle, baking a cake (recipe with overridable steps).

### [Iterator](30.1.36-iterator.md) *(new)*
Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

**When to use:**
- Access an aggregate's contents without exposing its internal structure
- Support multiple traversals of aggregate objects
- Provide a uniform interface for traversing different aggregate structures
- You need lazy iteration (don't materialize the whole sequence)

**Real-world examples:** `for...of` in JS, generator functions (`yield`), JavaScript `Symbol.iterator`, Java `Iterable`, Python iterators, SQL cursor, file system traversal, tree traversal.

### [Mediator](30.1.37-mediator.md) *(new)*
Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly.

**When to use:**
- A set of objects communicate in well-defined but complex ways (many-to-many)
- Reusing an object is difficult because it refers to and communicates with many other objects
- A behavior that's distributed between several classes should be customizable without a lot of subclassing
- You want to centralize complex communication logic

**Real-world examples:** Air traffic control tower, chat room, dialog boxes in GUIs (the dialog coordinates widget interactions), Redux/Zustand store (mediates between components and state), event bus, MediatR library in C#, NestJS event bus.

### [Memento](30.1.38-memento.md) *(new)*
Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

**When to use:**
- A snapshot of an object's state must be saved so it can be restored later
- A direct interface to obtaining the state would expose implementation details and break encapsulation
- You need undo/redo functionality

**Real-world examples:** Undo/redo in editors, database transaction rollback, snapshot testing (`expect(state).toMatchSnapshot()`), Redux DevTools time-travel debugging, git (commits as mementos), game save files.

### [Command](30.1.39-command.md) *(new)*
Encapsulate a request as an object, thereby allowing parameterization of clients with different requests, queue or log requests, and support undo.

**When to use:**
- Parameterize objects by the action to perform
- Specify, queue, and execute requests at different times
- Support undo/redo
- Support logging changes so they can be reapplied after a crash
- Structure a system around high-level operations built on primitive operations

**Real-world examples:** Job queues (BullMQ, Sidekiq), `git` commands (each commit is a command with apply/revert), Redux actions, CQRS command objects, macro recording, transaction scripts, "run this later" features.

### [Visitor](30.1.40-visitor.md) *(new)*
Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

**When to use:**
- An object structure contains many classes with differing interfaces, and you want to perform operations on these objects that depend on their concrete classes
- Many distinct and unrelated operations need to be performed on objects in a structure
- The classes defining the object structure rarely change, but you often want to define new operations over the structure

**Real-world examples:** AST traversal in compilers, file system operations (visit File, Directory, Symlink with different logic), XML/JSON serializers, schema validation, bill of materials calculator, linter rules.

### [Interpreter](30.1.41-interpreter.md) *(new)*
Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.

**When to use:**
- The grammar of the language is simple (otherwise a parser generator is better)
- Efficiency is not a critical concern (interpreters are usually slower than compiled parsers)
- You want to express domain-specific language rules in your code

**Real-world examples:** SQL parsers, regex engines, math expression evaluators, search query languages (Lucene), boolean expression trees, configuration formats (HCL, TOML), workflow rules engines.

---

## Decision flowchart

```
Need to manage object interaction / control flow?
│
├─ Pick an algorithm at runtime? ──→ Strategy
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
└─ Interpret a grammar / DSL? ──→ Interpreter
```

---

## Comparisons

### Strategy vs State

| | Strategy | State |
|--|----------|-------|
| **Who chooses** | Client / context picks strategy | Object transitions state on its own |
| **Number of states** | Many, often set once at init | Often a state machine with transitions |
| **Awareness of each other** | Strategies usually don't know about each other | States often trigger transitions to other states |
| **Intent** | "How to do this" | "What am I currently doing" |

A common rule of thumb: if the strategies don't reference each other, it's Strategy. If they do (e.g., `context.setState(new NextState())`), it's State.

### Observer vs Mediator

- **Observer** is a **one-to-many** notification system. Subject doesn't know its observers.
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

- **CoR** picks **one** handler from a chain; the request is consumed.
- **Decorator** adds behavior at **every** layer; the call passes through all.

Both chain-call. The difference is whether the chain short-circuits (CoR) or composes (Decorator).

---

## When NOT to use behavioral patterns

- **Strategy** for a single algorithm — just write the function.
- **Observer** when you have 2 components that should call each other directly.
- **CoR** when there's exactly one handler — just call it.
- **State** for 2-3 simple states — a plain enum + switch is fine.
- **Template Method** in TypeScript — composition is usually cleaner; reach for higher-order functions.
- **Iterator** in modern JS — just use `for...of` / generators, the language has you covered.
- **Mediator** for 3-4 simple objects — direct refs are clearer.
- **Memento** if undo isn't a requirement.
- **Command** for one-shot operations with no queue/undo.
- **Visitor** if the object structure changes often (you'll rewrite all visitors).
- **Interpreter** for complex grammars — use a parser generator (PEG, ANTLR).

---

## Cross-References

- [Foundations](../30.1.0-foundations/INDEX.md) — OOP concepts and SOLID are prerequisites.
- [Structural Patterns](../30.1.2-structural/INDEX.md) — Iterator often traverses a Composite; Visitor does too.
- [Architectural Patterns](../30.1.4-architectural/INDEX.md) — Command is the basis of CQRS, Observer is the basis of Event Sourcing.

---

## Navigation

[← Structural Patterns](../30.1.2-structural/INDEX.md) · [↑ Design Patterns Home](../INDEX.md) · [Next: Architectural Patterns →](../30.1.4-architectural/INDEX.md)
