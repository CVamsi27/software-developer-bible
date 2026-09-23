# Structural Patterns

> **Study time:** ≈ 3 h 30 m of reading (8 files, ~26 min average).
> **8 files.** Class and object composition. These patterns are about how to assemble larger structures from classes and objects while keeping the structure flexible and efficient.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Structural-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What structural patterns solve

Inheritance is rigid (compile-time, locked to a parent class) and often overused. Structural patterns let you compose objects at runtime to get new functionality, instead of baking it into a class hierarchy.

### Common signals you need one

- "I need to use a 3rd-party class but its interface doesn't match mine."
- "I want to add behavior to an object without affecting other instances of the same class."
- "I have a complex subsystem and want a single, simple entry point."
- "Loading this object is expensive — I want lazy / cached / proxied access."

---

## The 8 patterns

| # | Pattern | Intent | Use when | Avoid when |
| --: | --------- | -------- | ---------- | ------------ |
| 1 | [Adapter](30.1.3.01-adapter.md) | Bridge incompatible interfaces | 3rd-party SDK, legacy integration | You control both sides |
| 2 | [Facade](30.1.3.02-facade.md) | Simplified front for complex system | Library/SDK, multi-subsystem workflow | Single subsystem, already simple |
| 3 | [Decorator](30.1.3.03-decorator.md) | Add behavior dynamically | Cross-cutting concerns (logging, auth, caching) | Many independent dimensions → explosion |
| 4 | [Proxy](30.1.3.04-proxy.md) | Controlled access (lazy, protection, remote, caching) | Image/DB lazy loading, RBAC checks, network stubs | Direct access is fine |
| 5 | [Module](30.1.3.05-module-pattern.md) | Encapsulation at the file level | Always in modern JS/TS | N/A |
| 6 | [Composite](30.1.3.06-composite.md) | Tree structures, treat part-whole uniformly | File system, UI tree, org chart, AST | Flat structures, no recursion |
| 7 | [Bridge](30.1.3.07-bridge.md) | Decouple abstraction from implementation | Multiple dimensions of variation (shape × color × renderer) | One dimension, stable axis |
| 8 | [Flyweight](30.1.3.08-flyweight.md) | Share state to support many fine-grained objects | Text rendering (chars), particle systems, glyph caches | Few objects, no memory pressure |

---

## Pattern Index

### [Adapter](30.1.3.01-adapter.md)
Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

**When to use:**
- You want to use an existing class, but its interface doesn't match what you need
- You want to create a reusable class that cooperates with unrelated classes
- You need to integrate with a 3rd-party SDK or legacy system you can't change

**Real-world examples:** Wrapping a Stripe SDK in your own `PaymentProvider` interface, adapting a legacy XML API to your JSON-based code, converting `Promise` to callback APIs.

### [Facade](30.1.3.02-facade.md)
Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

**When to use:**
- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes
- You want to layer your subsystems (each facade is the entry point to its layer)

**Real-world examples:** `PrismaClient` (hides raw SQL + connection pool + migrations), `fetch` (hides HTTP socket details), Express `app` (hides routing, middleware chain, error handling).

### [Decorator](30.1.3.03-decorator.md)
Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

**When to use:**
- You want to add responsibilities to individual objects dynamically and transparently
- Responsibilities should be withdrawable
- Extension by subclassing is impractical (would cause class explosion)

**Real-world examples:** `@logged()`, `@retry(3)`, `@memoize()` decorators, `Response.json()` wrapping a `Response` with caching headers, NestJS guards/pipes/interceptors, React higher-order components.

### [Proxy](30.1.3.04-proxy.md)
Provide a surrogate or placeholder for another object to control access to it.

**When to use:**
- **Virtual proxy** — lazy loading (image, DB record loaded on first access)
- **Protection proxy** — access control (auth, RBAC checks before delegating)
- **Remote proxy** — local rep of remote object (gRPC client, REST SDK)
- **Caching proxy** — memoization layer
- **Logging/monitoring proxy** — wrap a real service to record calls

**Real-world examples:** `Object.defineProperty` getters as lazy access, React Suspense's resource loading, ORM lazy-loaded relations, Vue 3 reactivity (`Proxy` under the hood!).

### [Module Pattern](30.1.3.05-module-pattern.md)
Encapsulate a group of related classes, functions, and variables into a single unit. The original "module pattern" was an IIFE returning a public API. In modern JS/TS, this is the default (ES modules).

**When to use:**
- Always. In modern code, this is built into the language.
- Use IIFE / revealing module only when targeting pre-ES2015 environments.

**Real-world examples:** ES `import`/`export`, `index.ts` barrel files, package.json's `main` field, `namespace` in TypeScript (legacy).

### [Composite](30.1.3.06-composite.md) *(new)*
Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions uniformly.

**When to use:**
- You want to represent part-whole hierarchies of objects
- You want clients to be able to ignore the difference between compositions of objects and individual objects
- The structure is recursive (a folder contains files and other folders)

**Real-world examples:** File system (files + folders), UI tree (Component → children), AST (Node + children), org chart (Employee + reports), React/Vue component trees.

### [Bridge](30.1.3.07-bridge.md) *(new)*
Decouple an abstraction from its implementation so that the two can vary independently.

**When to use:**
- You want to avoid a permanent binding between an abstraction and its implementation
- Both the abstraction and the implementation should be extensible by subclassing
- Changes in the implementation should not impact clients
- You have a "Cartesian product" of concerns (3 shapes × 4 renderers = 12 classes — Bridge reduces to 7)

**Real-world examples:** Cross-platform rendering (Shape × Renderer), JDBC (Abstraction × Driver), OS-specific file I/O (File × OS), input devices (Device × Driver).

### [Flyweight](30.1.3.08-flyweight.md) *(new)*
Use sharing to support large numbers of fine-grained objects efficiently.

**When to use:**
- An application uses a large number of objects
- Storage costs are high because of the sheer quantity of objects
- Most object state can be made extrinsic (moved out of the object)
- Many groups of objects can be replaced by relatively few shared objects once extrinsic state is removed

**Real-world examples:** Character glyphs in a text editor (share glyphs, store position + style externally), particle systems in games (share particle types, store position externally), database connection pools, JS engine string interning.

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

| Adapter | Decorator | Proxy |  |
| -- | --------- | ----------- | -------- |
| **Intent** | Make incompatible interface work | Add new behavior | Control access |
| **Interface** | Changes the interface | Keeps or extends the interface | Keeps the interface |
| **When it intercepts** | Always (it's the only way to call the adaptee) | On every call (to add behavior) | On every call (to gate / cache / lazy-load) |
| **Knows about clients** | No | No | Usually not, but can (auth proxy) |
| **Example** | Wrap Stripe API in your `PaymentProvider` | Wrap a service with `@logged()` | Wrap a DB row for lazy loading |

A common interview trap: "What's the difference between Decorator and Proxy?" The answer is **intent** — Decorator wants to add behavior, Proxy wants to control access. In code they can be indistinguishable.

### Facade vs Adapter

- **Facade** simplifies a complex subsystem (one-way: subsystem → simple API). Often introduces a new interface.
- **Adapter** reconciles two existing incompatible interfaces (two-way: existing A ↔ existing B). Doesn't add behavior, just translates.

### Composite vs Decorator

- **Composite** is about **structure** (recursive tree, sum of parts behaves like a single).
- **Decorator** is about **behavior** (add responsibilities to a single object without affecting others).

Both use recursive composition, but Composite's recursion is structural, Decorator's is behavioral.

### Module vs Facade

- **Module** organizes code at the file/package level (language-level encapsulation).
- **Facade** is a runtime object that provides a simpler interface to a set of objects.

Modern TS: a `module.ts` file often *contains* a Facade.

---

## When NOT to use structural patterns

- **Adapter** when you control both sides — just refactor the interface.
- **Facade** when the subsystem is small and the client already knows it.
- **Decorator** for more than 2-3 dimensions of behavior (use a config object or strategy instead — explosion of classes).
- **Proxy** for a 1-line property access — just inline the check.
- **Composite** when the structure is flat and never recursive.
- **Bridge** when you have one stable axis (you'd just use inheritance).
- **Flyweight** when you have < 1000 objects — the bookkeeping isn't worth it.
- **Module** in modern code — just use ES modules.

---

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
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Facade | `shared/modules/imports/ocr-facade.service.ts` hides the OCR pipeline; `shared/whatsapp/templates-facade.service.ts` hides template resolution — delegation enforced by `scripts/checks/check-facade-delegation.mjs` |
| Adapter | India's ABDM government API wrapped by `domains/abdm/infrastructure/abdm-abha.client.ts`; Razorpay SDK behind `payments/infrastructure/adapters/razorpay/` |
| Decorator (framework-shaped) | NestJS interceptor/guard pipelines in `shared/common/interceptors/*` add logging, CSRF, tenant-context around handlers |
| Module | ES modules + barrel `index.ts` files at every module boundary |
| Proxy / Flyweight / Composite / Bridge | _No direct docita implementation yet._ |
