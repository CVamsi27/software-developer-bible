# Creational Patterns

> **Study time:** ≈ 1 h 4 m of reading (6 files, ~11 min average).
> **6 files.** Object creation mechanisms. These patterns decouple "how to construct an object" from "what to do with the constructed thing." The goal: make a system independent of how its objects are created, composed, and represented.

[![Files](https://img.shields.io/badge/files-6-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Creational-orange)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What creational patterns solve

Direct construction is adequate when its choices are local and stable. A creation boundary helps when several clients repeat provider selection, assembly rules, template copying, or resource-lifetime decisions. Adding a factory around every `new` adds indirection without necessarily solving any of those problems.

The client receives a product contract; setup and its construction owner retain the concrete choice. Read the patterns by that responsibility, then trace what is copied, reused, or validated.

### Common signals you need one

- "I have a `switch` on type to decide which class to instantiate."
- "Every time I add a new subclass, I have to edit 5 files."
- "My test setup involves mocking 10 concrete classes."
- "I need different instances for different environments (dev / staging / prod)."

---

## The 5 patterns

| # | Pattern | Intent | Use when | Avoid when | Role priority | General importance |
| --: | --------- | -------- | ---------- | ------------ | --- | --- |
| 1 | [Singleton](30.1.2.01-singleton.md) | One instance in a defined runtime scope | Logger, config, connection pool | Global lookup hides scope or request state | Important | Specialized |
| 2 | [Factory Method](30.1.2.02-factory-method.md) | Defer instantiation to subclass | Plugin system, multiple implementations | Only one type, simple `new` works | Important | Foundational |
| 3 | [Builder](30.1.2.03-builder.md) | Step-by-step construction | Ordered assembly or reusable recipes | Named options already suffice | Important | Specialized |
| 4 | [Abstract Factory](30.1.2.04-abstract-factory.md) | Families of related objects | Cross-platform UI, theme systems, OS-specific bundles | No compatibility requirement | Important | Specialized |
| 5 | [Prototype](30.1.2.05-prototype.md) | Clone instead of construct | Object creation is expensive, "shape then customize" | Copy semantics add more cost than direct construction | Important | Specialized |

---

## Pattern Index

### [Singleton](30.1.2.01-singleton.md)
Shares one instance within a defined runtime scope. A module export or dependency-injection container may provide the required lifetime without a global class accessor. Neither mechanism coordinates separate processes.

**When to use:**
- Logger (one place, all writes go there)
- Configuration / settings (read once, read everywhere)
- Thread pool / connection pool manager
- Cache registry

**When NOT to use:**
- A shared mutable owner would retain per-request or tenant identity
- Callers need separately scoped owners or independently isolated test state
- An explicit injected shared instance already makes its lifetime clearer

### [Factory Method](30.1.2.02-factory-method.md)
Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

**When to use:**
- A class can't anticipate the class of objects it must create
- A class wants its subclasses to specify the objects it creates
- Classes delegate responsibility to one of several helper subclasses

**Real-world examples:** A creator subclass implements the creation operation used by the base workflow. Conditional constructor selectors are simple factories.

### [Builder](30.1.2.03-builder.md)
Separate the construction of a complex object from its representation so that the same construction process can create different representations.

**When to use:**
- The object needs meaningful staged assembly or a reusable construction recipe
- An object needs many steps to construct (validate, transform, normalize)
- You want a clear build boundary and a deliberate copying/immutability policy (`new UserBuilder().name('x').age(30).build()`)
- You want different representations of the same construction process

**Real-world examples:** `new RequestBuilder().url('...').method('POST').header(...).body(...).build()`, SQL query builders, test data builders.

### [Abstract Factory](30.1.2.04-abstract-factory.md) *(new)*
Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**When to use:**
- A system must be configured with one of multiple families of products
- A family of related product objects is designed to be used together
- You want to enforce that certain products are always used together (e.g., Mac UI: MacButton + MacCheckbox + MacScrollbar)

**Illustrative applications:** matching UI components, themed component families, or provider capabilities that require the same protocol/account context. Confirm the actual factory mechanism before naming a framework as an implementation.

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
├─ One owner within a defined scope? ──→ Explicit shared lifetime; Singleton is one option
│
├─ Base workflow delegates creation to subclasses? ──→ Factory Method
├─ Configuration centrally selects a constructor? ──→ Simple factory/registry
│
├─ Need a whole family of related objects? ──→ Abstract Factory
│
├─ Staged assembly needs one construction owner? ──→ Builder or named options
│
└─ Configured template plus defined copy semantics? ──→ Prototype
```

---

## Comparisons

### Factory Method vs Abstract Factory

- **Factory Method** creates **one** product; subclasses decide the concrete type.
- **Abstract Factory** creates a **family** of related products; the factory itself is the abstraction, and concrete factories (e.g., `MacUIFactory`) return a matching set.

The signal is a coherent family of related products, not a fixed minimum number of methods.

### Builder vs Factory

- **Factory** creates an object in **one step** (often eagerly, with no params or a few).
- **Builder** constructs the object **step-by-step**, with many optional parts, and the build is the final step.

Many optional construction steps can justify a Builder; a named options object may be simpler.

### Prototype vs Factory

- **Factory** creates from a class (re-runs the constructor + init).
- **Prototype** delegates to an instance's clone contract; it may still call a constructor while reusing configured data.

If construction is expensive and most new objects look like existing ones, Prototype may be appropriate after comparing copy semantics and cost.

---

## When NOT to use creational patterns

- A global Singleton accessor can hide dependencies and retain unscoped mutable state. Explicit injection can preserve a shared owner while exposing the dependency.
- **Factory Method** for a single concrete class is over-engineering.
- **Abstract Factory** when you have 1-2 products with no family relationships is overkill.
- **Builder** for a 2-field DTO is noise. Use a plain object literal.
- **Prototype** when your classes are simple value objects — just use `new`.

---

## Reading Path and Completion Check

Compare the creation decision in Factory Method and Abstract Factory. Then study Builder for valid assembly, Prototype for cloning semantics and Singleton for lifecycle scope.

Choose a creation pattern from a concrete variation axis and name the extra coupling or lifecycle cost it introduces. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

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
| Factory techniques | FHIR resource factories (`shared/modules/fhir/factories/fhir-patient.factory.ts`…), analytics factories (`domains/analytics/core/factories/*`), compliance factories (`anonymization.factory.ts`, `data-export.factory.ts`) |
| Factory families | `apps/api/src/domains/payments/infrastructure/factories/payment-gateway.factory.ts`, `apps/api/src/shared/modules/monitoring/monitoring/factories/monitoring.factory.ts` |
| Builder | FHIR observation builders: `fhir/factories/observations/builders/*.builder.ts` (blood pressure, heart rate, SpO₂…) behind a shared port |
| Construction ownership guard | Construction/value-import restricted to one source file by `scripts/checks/check-openai-client-singleton.mjs` over `shared/modules/ai/openai.service.ts` |
| Abstract Factory / Prototype | Do not infer these GoF mechanisms from a filename; the cited factories and builders are implementation pointers, not an exhaustive architecture audit. |
