<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practi | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Structural — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Adapter Pattern

Source: [Adapter Pattern](30.1.3.01-adapter.md)

**Q:** When does a wrapper qualify as an Adapter rather than merely a forwarding helper?

**A:** It translates an existing interface into the interface the client expects, including any required data or semantic conversion.

## Facade Pattern

Source: [Facade Pattern](30.1.3.02-facade.md)

**Q:** Does a Facade prevent callers from using the underlying subsystem directly?

**A:** Not necessarily. It offers a simpler entry point; access restrictions require a separate encapsulation or permission boundary.

## Decorator Pattern

Source: [Decorator Pattern](30.1.3.03-decorator.md)

**Q:** What invariant lets multiple decorators compose around one component?

**A:** Each exposes the component's expected interface while delegating and adding behavior. Ordering can still change semantics and should be explicit.

## Proxy Pattern

Source: [Proxy Pattern](30.1.3.04-proxy.md)

**Q:** What distinguishes a Proxy's intent from a Decorator's intent?

**A:** A Proxy controls access, identity, location or lifecycle of a subject. A Decorator adds responsibilities through composition; similar wrapper structures can serve different intentions.

## Module Pattern

Source: [Module Pattern](30.1.3.05-module-pattern.md)

**Q:** What does module privacy fail to provide in an application that serves many tenants?

**A:** It hides implementation bindings, but does not create per-tenant data isolation. Shared mutable module state can still mix requests unless scoped correctly.

## Composite Pattern

Source: [Composite Pattern](30.1.3.06-composite.md)

**Q:** What advantage does Composite provide to a tree-processing client?

**A:** The client can use a shared component contract for leaves and containers. The design still must decide how to expose operations that only containers support.

## Bridge Pattern

Source: [Bridge Pattern](30.1.3.07-bridge.md)

**Q:** How does Bridge avoid a hierarchy growing for every combination of two dimensions?

**A:** It separates the abstraction hierarchy from its implementation hierarchy and connects them through composition, so each dimension can vary independently.

## Flyweight Pattern

Source: [Flyweight Pattern](30.1.3.08-flyweight.md)

**Q:** Which state belongs outside a shared Flyweight?

**A:** Keep usage-specific state, called extrinsic state, outside the shared object—for example, a glyph’s position. State shared by every use, called intrinsic state, must be safely reusable and is usually immutable.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
