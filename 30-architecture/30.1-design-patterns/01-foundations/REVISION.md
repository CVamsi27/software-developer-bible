<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Foundations — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## SOLID Principles

Source: [SOLID Principles](30.1.1.01-solid-principles.md)

**Q:** What makes two interfaces preferable to one large interface in an ISP example?

**A:** Clients depend only on the operations they need, so unrelated changes do not impose implementation or coupling costs. Splitting is useful when it follows actual client responsibilities.

**Q:** When should a design principle yield to a concrete requirement?

**A:** Principles are heuristics. Compare their coupling, complexity and change costs against the actual constraints; explain the tradeoff rather than claiming a slogan proves the design.

## DRY, KISS, YAGNI & Other Design Principles

Source: [DRY, KISS, YAGNI & Other Design Principles](30.1.1.02-dry-kiss-yagni.md)

**Q:** Two functions look similar but serve different business rules. Should DRY merge them?

**A:** Only when they express the same knowledge that should change together. Prematurely sharing coincidental structure can couple independent rules; duplication can be cheaper until that relationship is clear.

## OOP Concepts — Encapsulation, Inheritance, Polymorphism, Abstraction

Source: [OOP Concepts — Encapsulation, Inheritance, Polymorphism, Abstraction](30.1.1.03-oop-concepts.md)

**Q:** Why can inheritance violate substitutability even when the code type-checks?

**A:** A subtype may demand stricter inputs, offer weaker guarantees, or break rules that callers rely on. A compatible type signature alone does not prove that replacing the original type preserves its behavior.

## UML Basics — Class & Sequence Diagrams

Source: [UML Basics — Class & Sequence Diagrams](30.1.1.04-uml-basics.md)

**Q:** Which UML view helps diagnose a request that calls the right classes in the wrong order?

**A:** A sequence diagram shows messages and their order over time. A class diagram describes structural relationships but does not establish that runtime sequence.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
