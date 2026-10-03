<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practi | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Creational — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Singleton Pattern

Source: [Singleton Pattern](30.1.2.01-singleton.md)

**Q:** Does a JavaScript singleton guarantee one instance across workers or application replicas?

**A:** No. Its scope is the module/runtime instance. Separate processes or module copies can have separate instances; distributed coordination needs another mechanism.

## Factory Pattern

Source: [Factory Pattern](30.1.2.02-factory-method.md)

**Q:** What distinguishes Factory Method from a switch that chooses a constructor?

**A:** Factory Method lets subclasses vary creation through an overridable method. A central conditional creator is commonly a Simple Factory, though both hide construction from clients.

## Builder Pattern

Source: [Builder Pattern](30.1.2.03-builder.md)

**Q:** Where should a builder enforce that required values form a valid product?

**A:** At the construction boundary, usually build(), with earlier feedback where useful. A fluent API alone does not guarantee an immutable or valid result.

## Abstract Factory Pattern

Source: [Abstract Factory Pattern](30.1.2.04-abstract-factory.md)

**Q:** Why does adding a new product type cost more with Abstract Factory?

**A:** Each concrete family factory must supply that product type. The pattern favors adding whole compatible families over adding new kinds of product.

## Prototype Pattern

Source: [Prototype Pattern](30.1.2.05-prototype.md)

**Q:** Why can spreading a prototype object fail as a clone strategy?

**A:** Spread is shallow and does not preserve arbitrary class behavior. Nested mutable objects may remain shared; choose cloning semantics for the actual data and identity rules.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
