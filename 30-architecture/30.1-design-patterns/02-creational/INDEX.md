# Creational Patterns

> **Study time:** ≈ 46 min of reading (6 files, ~8 min average).
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
| 5 | [Prototype](30.1.2.05-prototype.md) | Copy through an existing instance | Object creation is expensive, "shape then customize" | Copy semantics add more cost than direct construction | Important | Specialized |

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
An overridable creation operation lets a base workflow use a product contract without choosing its concrete type. A configuration switch is a simple factory, not this GoF mechanism.

**When to use:**
- A class can't anticipate the class of objects it must create
- A class wants its subclasses to specify the objects it creates
- Classes delegate responsibility to one of several helper subclasses

**Real-world examples:** A creator subclass implements the creation operation used by the base workflow. Conditional constructor selectors are simple factories.

### [Builder](30.1.2.03-builder.md)
Keeps partial choices behind named steps and returns the product at a final construction boundary. Use it for ordered assembly, reusable recipes, or cross-field rules; an options object is simpler when callers can provide and validate all values together.

**When to use:**
- The object needs meaningful staged assembly or a reusable construction recipe
- An object needs many steps to construct (validate, transform, normalize)
- You want a clear build boundary and a deliberate copying/immutability policy (`new UserBuilder().name('x').age(30).build()`)
- You want different representations of the same construction process

**Real-world examples:** `new RequestBuilder().url('...').method('POST').header(...).body(...).build()`, SQL query builders, test data builders.

### [Abstract Factory](30.1.2.04-abstract-factory.md)
Selects a compatible family once and exposes one creation operation per product kind. Use it when related products must vary together; two products can be enough.

**Use when:** Several related product kinds must come from one configured platform, provider, or dialect. The factory implementation and tests establish the family promise; the interface alone does not.

**Illustrative applications:** matching UI components, themed component families, or provider capabilities that require the same protocol/account context. Confirm the actual factory mechanism before naming a framework as an implementation.

### [Prototype](30.1.2.05-prototype.md)
Copies a configured instance through an explicit `clone()` contract, so callers can request a similar object without choosing its constructor. The contract must define mutable state, shared resources, and identity; cloning is not automatically cheaper than construction.

**When to use:**
- A configured template is selected at runtime and must produce independent variants
- Repeating setup is costly or error-prone, and the clone policy is explicit

**Example:** Derive worker-specific request settings from validated defaults while copying mutable headers and retry policy.

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

- **Factory Method** lets subclasses determine the product returned by an overridable creation operation used by a creator workflow.
- **Abstract Factory** creates a **family** of related products; the factory itself is the abstraction, and concrete factories (e.g., `MacUIFactory`) return a matching set.

The signal is a coherent family of related products, not a fixed minimum number of methods.

### Builder vs Factory

- **Factory** exposes a creation operation; its implementation can have multiple internal steps or asynchronous initialization.
- **Builder** constructs the object **step-by-step**, with many optional parts, and the build is the final step.

Many optional construction steps can justify a Builder; a named options object may be simpler.

### Prototype vs Factory

- **Factory** owns a creation choice; it can construct, reuse a cached result, invoke a builder, or copy a prototype.
- **Prototype** delegates to an instance's clone contract; it may still call a constructor while reusing configured data.

If construction is expensive and most new objects look like existing ones, Prototype may be appropriate after comparing copy semantics and cost.

---

## When NOT to use creational patterns

- A global Singleton accessor can hide dependencies and retain unscoped mutable state. Explicit injection can preserve a shared owner while exposing the dependency.
- **Factory Method** for a single concrete class is over-engineering.
- **Abstract Factory** when there is no compatibility invariant across product kinds is overkill.
- **Builder** for a 2-field DTO is noise. Use a plain object literal.
- **Prototype** when your classes are simple value objects — just use `new`.

---

## Reading Path and Completion Check

Compare the creation decision in Factory Method and Abstract Factory. Then study Builder for valid assembly, Prototype for cloning semantics and Singleton for lifecycle scope.

Choose a creation pattern from a concrete variation axis and name the extra coupling or lifecycle cost it introduces. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [Foundations](../01-foundations/INDEX.md) — DIP and OOP concepts are prerequisites.
- [Structural Patterns](../03-structural/INDEX.md) — Facade often wraps a Factory.
- [Architectural Patterns](../05-architectural/INDEX.md) — Repository abstracts domain collection access; DI supplies dependencies and their lifetimes.

---

## Navigation

[← Foundations](../01-foundations/INDEX.md) · [↑ Design Patterns Home](../INDEX.md) · [Next: Structural Patterns →](../03-structural/INDEX.md)

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic | Docita evidence |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Factory techniques | FHIR resource factories (`shared/modules/fhir/factories/fhir-patient.factory.ts`…), analytics factories (`domains/analytics/core/factories/*`), compliance factories (`anonymization.factory.ts`, `data-export.factory.ts`) |
| Factory families | `apps/api/src/domains/payments/infrastructure/factories/payment-gateway.factory.ts`, `apps/api/src/shared/modules/monitoring/monitoring/factories/monitoring.factory.ts` |
| Builder | FHIR observation builders: `fhir/factories/observations/builders/*.builder.ts` (blood pressure, heart rate, SpO₂…) behind a shared port |
| Construction ownership guard | Construction/value-import restricted to one source file by `scripts/checks/check-openai-client-singleton.mjs` over `shared/modules/ai/openai.service.ts` |
| Abstract Factory / Prototype | Do not infer these GoF mechanisms from a filename; the cited factories and builders are implementation pointers, not an exhaustive architecture audit. |
