<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Creational — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Singleton Pattern

Source: [Singleton Pattern](30.1.2.01-singleton.md)

**Q:** Does a JavaScript singleton guarantee one instance across workers or application replicas?

**A:** No. Its scope is the module/runtime instance. Separate processes or module copies can have separate instances; distributed coordination needs another mechanism.

**Q:** Trace two concurrent calls to `sharedAsyncResource`. Which operation is shared, and when can a retry start?

**A:** The first call stores a promise before its loader runs; the second returns that same promise. A rejected load clears the cached promise, allowing a later call to start a fresh attempt. Success keeps the result shared until an explicit lifecycle policy changes it.

**Q:** What changes when another process imports the same registry file?

**A:** It has a separate runtime and module instance, hence a separate static field or module object. A fleet-wide ownership rule needs a shared coordination contract, not another local accessor.

## Factory Method and Simple Factories

Source: [Factory Method and Simple Factories](30.1.2.02-factory-method.md)

**Q:** What distinguishes Factory Method from a switch that chooses a constructor?

**A:** Factory Method lets subclasses vary creation through an overridable method. A central conditional creator is commonly a Simple Factory, though both hide construction from clients.

**Q:** Trace `CarFactory.describeVehicle()`. Where is construction selected and where is the product used?

**A:** The inherited workflow calls `this.createVehicle`; dispatch reaches `CarFactory`, which constructs a car. The base workflow then reads the product through `Vehicle`. The client did not choose that constructor inside the workflow.

**Q:** A new notification channel must be chosen by configuration. Does the simple factory's switch violate the intended design?

**A:** Not automatically. A small central switch can own a closed configuration choice. A plugin-registration requirement may justify a registry; subclass-supplied creation inside a base workflow is the distinct Factory Method mechanism.

## Builder Pattern

Source: [Builder Pattern](30.1.2.03-builder.md)

**Q:** Where should a builder enforce that required values form a valid product?

**A:** At the construction boundary, usually build(), with earlier feedback where useful. A fluent API alone does not guarantee an immutable or valid result.

**Q:** Trace the simple-house director followed by the full-house director on the same builder. Why does the first result remain separate?

**A:** The first sequence builds foundation, structure, and roof. `getResult` returns that house and resets the builder to a new house before the second sequence. It is separate but still mutable, and this assembly example does not validate a complete physical house.

**Q:** What if the HTTP builder builds a POST, then changes only its URL before building again?

**A:** Its `build` does not reset, so the second description retains the POST method, headers, body, timeout, and retry settings. Use `reset` or a new builder for an unrelated request. The consumer still implements timeout and retry safety.

## Abstract Factory Pattern

Source: [Abstract Factory Pattern](30.1.2.04-abstract-factory.md)

**Q:** Why does adding a new product type cost more with Abstract Factory?

**A:** Each concrete family factory must supply that product type. The pattern favors adding whole compatible families over adding new kinds of product.

**Q:** Trace `Application.render` with `MacFactory`. Which two creation decisions are linked?

**A:** Setup chooses one factory; the client asks that factory for a button and checkbox, then renders both. Their coherent family is an implementation promise of the factory, not proved merely by two structurally compatible return interfaces.

**Q:** What changes if all supported platforms now need a scrollbar?

**A:** The shared creation contract adds that product kind, every concrete family must implement it, and clients that use it need its product contract. Adding a whole new family instead preserves the existing product-kind interface while adding implementations and setup selection.

## Prototype Pattern

Source: [Prototype Pattern](30.1.2.05-prototype.md)

**Q:** Why can spreading a prototype object fail as a clone strategy?

**A:** Spread is shallow and does not preserve arbitrary class behavior. Nested mutable objects may remain shared; choose cloning semantics for the actual data and identity rules.

**Q:** Trace the enemy shallow clone's `inventory.push('shield')`. Which other object changes?

**A:** The shallow clone shares the base inventory reference, so the base also sees `shield`. The deep clone copies the known position object and string array, so mutations of those owned children remain independent.

**Q:** What if a staging override supplies only `{features: {newDashboard: true}}`?

**A:** `withOverrides` replaces the entire top-level feature section; it does not preserve `darkMode` through a nested merge. Its copies prevent cross-config mutation. A deep-merge contract would require explicit rules for arrays, removals, and conflicts.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
