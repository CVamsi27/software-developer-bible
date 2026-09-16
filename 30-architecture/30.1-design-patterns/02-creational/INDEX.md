# Creational Patterns

> **Study time:** ≈ 2 h 5 m of reading (5 files, ~25 min average).
> **5 files.** Object creation mechanisms. These patterns decouple "how to construct an object" from "what to do with the constructed thing." The goal: make a system independent of how its objects are created, composed, and represented.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Creational-orange)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What creational patterns solve

Without creational patterns, code that creates objects directly with `new` is hard to extend (every `new` is a coupling point), hard to test (you can't substitute a fake), and rigid (adding a new product class means editing every constructor call site).

Creational patterns encapsulate knowledge about which concrete classes the system uses, but hide how instances of these classes are created and put together.

### Common signals you need one

- "I have a `switch` on type to decide which class to instantiate."
- "Every time I add a new subclass, I have to edit 5 files."
- "My test setup involves mocking 10 concrete classes."
- "I need different instances for different environments (dev / staging / prod)."

---

## The 5 patterns

| # | Pattern | Intent | Use when | Avoid when |
| --: | --------- | -------- | ---------- | ------------ |
| 1 | [Singleton](30.1.2.01-singleton.md) | One global instance | Logger, config, connection pool | Testability matters, multiple environments |
| 2 | [Factory Method](30.1.2.02-factory-method.md) | Defer instantiation to subclass | Plugin system, multiple implementations | Only one type, simple `new` works |
| 3 | [Builder](30.1.2.03-builder.md) | Step-by-step construction | 5+ optional fields, immutable objects | Simple objects with 2-3 fields |
| 4 | [Abstract Factory](30.1.2.04-abstract-factory.md) | Families of related objects | Cross-platform UI, theme systems, OS-specific bundles | Few object types, no "family" concept |
| 5 | [Prototype](30.1.2.05-prototype.md) | Clone instead of construct | Object creation is expensive, "shape then customize" | Class hierarchy is simple and flat |

---

## Pattern Index

### [Singleton](30.1.2.01-singleton.md)
Guarantees a class has exactly one instance and provides a global point of access to it. In modern TypeScript, mostly replaced by DI containers and module-scoped state.

**When to use:**
- Logger (one place, all writes go there)
- Configuration / settings (read once, read everywhere)
- Thread pool / connection pool manager
- Cache registry

**When NOT to use:**
- Anything that needs to be different in tests
- Anything that should differ between dev/staging/prod
- Modern TS/JS code (use `import { logger } from "./logger"` instead)

### [Factory Method](30.1.2.02-factory-method.md)
Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

**When to use:**
- A class can't anticipate the class of objects it must create
- A class wants its subclasses to specify the objects it creates
- Classes delegate responsibility to one of several helper subclasses

**Real-world examples:** `LoggerFactory.getLogger('http')` returns Winston or Pino based on env, `HttpClientFactory.create()` returns axios or fetch.

### [Builder](30.1.2.03-builder.md)
Separate the construction of a complex object from its representation so that the same construction process can create different representations.

**When to use:**
- An object has 5+ optional fields
- An object needs many steps to construct (validate, transform, normalize)
- You want immutability + readability (`new UserBuilder().name('x').age(30).build()`)
- You want different representations of the same construction process

**Real-world examples:** `new RequestBuilder().url('...').method('POST').header(...).body(...).build()`, SQL query builders, test data builders.

### [Abstract Factory](30.1.2.04-abstract-factory.md) *(new)*
Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**When to use:**
- A system must be configured with one of multiple families of products
- A family of related product objects is designed to be used together
- You want to enforce that certain products are always used together (e.g., Mac UI: MacButton + MacCheckbox + MacScrollbar)

**Real-world examples:** Cross-platform UI toolkits (Qt, JavaFX), theme systems (light/dark + matching dialog/button), OS-specific file dialogs.

### [Prototype](30.1.2.05-prototype.md) *(new)*
Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

**When to use:**
- Object creation is expensive (DB lookup, network call, complex init)
- You need many similar objects that differ only in a few fields
- Classes to instantiate are specified at runtime (e.g., dynamic loading)
- You want to avoid building a class hierarchy of factories

**Real-world examples:** Cloning a default config and overriding 2 fields, spawning enemies in a game that share base stats, document templates (clone the template, fill in blanks).

---

## Decision flowchart

```
Need to create objects?
│
├─ Need exactly one instance? ─── YES ──→ Singleton
│
├─ One product type, but creation logic varies? ──→ Factory Method
│
├─ Need a whole family of related objects? ──→ Abstract Factory
│
├─ Object has many optional fields, want immutability? ──→ Builder
│
└─ Object creation is expensive, just want a copy? ──→ Prototype
```

---

## Comparisons

### Factory Method vs Abstract Factory

- **Factory Method** creates **one** product; subclasses decide the concrete type.
- **Abstract Factory** creates a **family** of related products; the factory itself is the abstraction, and concrete factories (e.g., `MacUIFactory`) return a matching set.

If you find yourself with 3+ Factory Methods that get used together, that's an Abstract Factory.

### Builder vs Factory

- **Factory** creates an object in **one step** (often eagerly, with no params or a few).
- **Builder** constructs the object **step-by-step**, with many optional parts, and the build is the final step.

If your constructor takes 5+ params or you have 3+ overloads, that's a Builder.

### Prototype vs Factory

- **Factory** creates from a class (re-runs the constructor + init).
- **Prototype** copies an existing instance (skips constructor + init).

If construction is expensive and most new objects look like existing ones, Prototype wins.

---

## When NOT to use creational patterns

- **Singleton** is an anti-pattern in most modern code (testability, hidden coupling, hidden global state). Reach for DI instead.
- **Factory Method** for a single concrete class is over-engineering.
- **Abstract Factory** when you have 1-2 products with no family relationships is overkill.
- **Builder** for a 2-field DTO is noise. Use a plain object literal.
- **Prototype** when your classes are simple value objects — just use `new`.

---

## Cross-References

- [Foundations](../01-foundations/INDEX.md) — DIP and OOP concepts are prerequisites.
- [Structural Patterns](../03-structural/INDEX.md) — Facade often wraps a Factory.
- [Architectural Patterns](../05-architectural/INDEX.md) — Repository and DI containers are creational patterns at scale.

---

## Navigation

[← Foundations](../01-foundations/INDEX.md) · [↑ Design Patterns Home](../INDEX.md) · [Next: Structural Patterns →](../03-structural/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS (NestJS monorepo) — builds objects for real.

| Topic | Docita evidence |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Factory Method | FHIR resource factories (`shared/modules/fhir/factories/fhir-patient.factory.ts`…), analytics factories (`domains/analytics/core/factories/*`), compliance factories (`anonymization.factory.ts`, `data-export.factory.ts`) |
| Factory families | `payments/infrastructure/factories/payment-gateway.factory.ts`, `monitoring/factories/monitoring.factory.ts` |
| Builder | FHIR observation builders: `fhir/factories/observations/builders/*.builder.ts` (blood pressure, heart rate, SpO₂…) behind a shared port |
| Singleton (enforced, not accidental) | One OpenAI client guaranteed by a CI gate: `scripts/checks/check-openai-client-singleton.mjs` over `shared/modules/ai/openai.service.ts` |
| Abstract Factory / Prototype | _No direct docita implementation yet._ |
