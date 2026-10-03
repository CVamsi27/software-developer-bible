<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice| general-importance: specialized| general-importance: foundational | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Behavioral — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Strategy Pattern

Source: [Strategy Pattern](30.1.4.01-strategy.md)

**Q:** Why can a Strategy be a function rather than a class?

**A:** The pattern needs an interchangeable behavioral contract; a function can satisfy it when no object lifecycle or additional methods are needed.

## Observer Pattern

Source: [Observer Pattern](30.1.4.02-observer.md)

**Q:** Why should an Observer registration have a clear unsubscribe owner?

**A:** A retained subscriber can keep objects alive and receive events after its lifetime. Registration cleanup also prevents duplicated callbacks after remount or reconnect.

## Chain of Responsibility

Source: [Chain of Responsibility](30.1.4.03-chain-of-responsibility.md)

**Q:** What must a Chain of Responsibility define besides handler order?

**A:** Whether a handler stops or forwards the request, what happens when none handles it, and how errors propagate. Middleware chains may deliberately run multiple handlers.

## State Pattern & State Machines

Source: [State Pattern & State Machines](30.1.4.04-state.md)

**Q:** When is a State pattern more appropriate than a Strategy?

**A:** When behavior follows an object's lifecycle state and transitions between states are part of its rules. A Strategy usually represents a chosen interchangeable policy.

## Template Method Pattern

Source: [Template Method Pattern](30.1.4.05-template-method.md)

**Q:** Where is the variation point in Template Method?

**A:** A base algorithm fixes the overall sequence and delegates selected steps to overridable operations. Subclasses should not accidentally break that sequencing contract.

## Iterator Pattern

Source: [Iterator Pattern](30.1.4.06-iterator.md)

**Q:** What happens if a collection changes while an iterator is in use?

**A:** It depends on the collection's contract: snapshot, fail-fast or live iteration. The Iterator pattern alone does not choose or guarantee mutation semantics.

## Mediator Pattern

Source: [Mediator Pattern](30.1.4.07-mediator.md)

**Q:** How can a Mediator become the next coupling problem?

**A:** If it absorbs every collaborator's domain rules, it becomes a large central dependency. Keep its responsibility focused on coordination and preserve cohesive participant behavior.

## Memento Pattern

Source: [Memento Pattern](30.1.4.08-memento.md)

**Q:** Why does storing a reference to the current state fail as a Memento for mutable data?

**A:** Later mutation changes the supposedly saved state. Capture a snapshot or persistent immutable version with a defined restoration boundary.

## Command Pattern

Source: [Command Pattern](30.1.4.09-command.md)

**Q:** Does turning a request into a Command automatically make undo possible?

**A:** No. Undo requires captured prior state or a valid inverse operation, and remote or irreversible effects may need compensation instead.

## Visitor Pattern

Source: [Visitor Pattern](30.1.4.10-visitor.md)

**Q:** Why is Visitor attractive for a stable object structure with changing operations?

**A:** New visitors can add operations without editing every element. Adding a new element type instead requires changing the visitor contract and its implementations.

## Interpreter Pattern

Source: [Interpreter Pattern](30.1.4.11-interpreter.md)

**Q:** When should a handwritten Interpreter give way to a parser or language toolkit?

**A:** When grammar complexity, diagnostics, performance or security exceeds the small expression language's needs. The pattern is not a substitute for a full language implementation.

## Null Object Pattern

Source: [Null Object Pattern](30.1.4.12-null-object.md)

**Q:** When can a Null Object hide a serious bug?

**A:** When absence should be an error or requires caller attention. Use a benign default only where the domain explicitly allows doing nothing.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
