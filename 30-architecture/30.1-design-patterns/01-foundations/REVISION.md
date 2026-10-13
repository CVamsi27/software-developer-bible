<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Foundations — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## SOLID Principles

Source: [SOLID Principles](30.1.1.01-solid-principles.md)

**Q:** What makes two interfaces preferable to one large interface in an ISP example?

**A:** Clients depend only on the operations they need, so unrelated changes do not impose implementation or coupling costs. Splitting is useful when it follows actual client responsibilities.

**Q:** The `Developer` throws for `manage()` and `design()`. What shows the ISP problem in this example?

**A:** `startShift` is typed against `Worker` even though it calls only `work`, so its contract exposes unrelated operations and forces irrelevant implementations. Give the scheduler a `Workable` contract; split only where a real client benefits.

**Q:** When should a design principle yield to a concrete requirement?

**A:** Principles are heuristics. Compare their coupling, complexity and change costs against the actual constraints; explain the tradeoff rather than claiming a slogan proves the design.

**Q:** Trace `test(new Square(1, 1))` through the width and height assignments. Which promised behavior breaks?

**A:** `setWidth(5)` sets both dimensions to 5; `setHeight(4)` then sets both to 4. The area is 16, while the caller relied on width remaining 5 and expected 20. Independent dimension mutation is the violated rectangle contract.

**Q:** The discount policy now needs purchase history. Does adding another strategy leave the interface unchanged?

**A:** Not necessarily. `apply(amount)` lacks that input. OCP protects the anticipated variation inside the current contract; a different requirement can require redesigning that contract and its callers.

**Q:** An account class has deposit, withdrawal and balance methods. Does that alone violate SRP?

**A:** No. Those methods may jointly preserve one coherent account rule. Identify independent stakeholder-driven changes and accidental coupling before splitting. An actor is a group with aligned requirements, not a method count; scattering an invariant across classes can make changes less safe.

**Q:** A switch handles three stable variants. Does OCP require replacing it with strategies?

**A:** No. First establish recurring variation whose changes should spare stable callers. A strategy boundary can help then; registration and genuinely changed contracts can still need edits. Compare that benefit with extra indirection.

### Preserved SOLID interview prompts

**Q:** "What's the difference between SRP and OCP?"

**A:** SRP isolates coherent sources of change; OCP exposes a boundary for extending known variation without editing stable policy. They address different change costs and can work together.

**Q:** "When should I NOT use SOLID?"

**A:** Avoid abstractions whose cost exceeds the change they isolate, such as unnecessary interfaces in a one-off script or speculative extension points in a prototype. Simple CRUD and performance-sensitive code still need clear contracts; compare a concrete benefit and cost rather than exempting an entire application type.

**Q:** "Does SOLID apply to functional programming?"

**A:** Responsibility, extension, client boundaries, and dependency direction also matter outside OOP. Functional programs can use parametric and ad-hoc polymorphism; behavioral substitution matters wherever callers rely on a contract.

## DRY, KISS, YAGNI & Other Design Principles

Source: [DRY, KISS, YAGNI & Other Design Principles](30.1.1.02-dry-kiss-yagni.md)

**Q:** Two functions look similar but serve different business rules. Should DRY merge them?

**A:** Only when they express the same knowledge that should change together. Prematurely sharing coincidental structure can couple independent rules; duplication can be cheaper until that relationship is clear.

**Q:** Trace registration from the HTTP controller to the public response. Where does the stored password hash disappear?

**A:** The service hashes the password, sends the hash to the repository, then returns a public projection such as `{ id, email }`. The HTTP response uses that projection, never the persistence record or password hash.

**Q:** Two clients already use one mandated validation rule. Must they wait for a third client before sharing it?

**A:** No. The Rule of Three gathers evidence when the shared knowledge is uncertain; it is not an admission threshold. Conversely, three similar validators can remain separate when their rules change independently.

**Q:** A CSV export may be requested later. What does YAGNI suggest, and which future conditions should still shape today's design?

**A:** Defer the unused export behavior and its generic framework. Preserve constraints that already exist, such as a required retention period, security boundary, or committed data migration; those are current requirements, not imagined features.

**Q:** A report currently meets its latency target with an in-memory sort. What would justify adding a cache or query framework?

**A:** A measured volume or latency constraint could justify more machinery if the mechanism addresses it. A vague scale estimate does not; keep the adequate implementation until evidence shows which limit it reaches.

**Q:** How should a senior engineer decide between a small function and a Strategy abstraction?

**A:** Start with real variation and callers. A small function is simpler when one rule is stable; Strategy can isolate independently changing policies, but adds contracts and wiring that need a concrete benefit.

**Q:** An implementation invokes Postel's Law to accept malformed protocol messages. What should you check?

**A:** Check the protocol's defined acceptance rules and known compatibility needs. [RFC 9413](https://www.rfc-editor.org/rfc/rfc9413.html) warns that broad tolerance can entrench ambiguous behavior and security flaws; emit canonical output and reject unspecified input.

**Q:** Why ask an account object to withdraw money, and what does that fail to guarantee across two processes?

**A:** The account operation can keep validation and the balance invariant together. Separate processes still need a transaction or concurrency control that serializes the shared persisted balance; a method call alone is not atomic.

**Q:** Does separation of concerns require one class for every operation?

**A:** No. Separate decisions that change independently and keep each invariant with its owner. Additional classes are useful only when they reduce coupling or make a meaningful boundary easier to test and understand.

## OOP Concepts — Encapsulation, Inheritance, Polymorphism, Abstraction

Source: [OOP Concepts — Encapsulation, Inheritance, Polymorphism, Abstraction](30.1.1.03-oop-concepts.md)

**Q:** Why can inheritance violate substitutability even when the code type-checks?

**A:** A subtype may demand stricter inputs, offer weaker guarantees, or break rules that callers rely on. A compatible type signature alone does not prove that replacing the original type preserves its behavior.

**Q:** Starting at 100, trace deposit 50, withdrawal 40, and attempted withdrawal 200. What state survives the rejection?

**A:** The balance becomes 150 then 110. The final withdrawal fails before mutation, so it remains 110. Amount validation also rejects non-finite, fractional, or unsafe integer values.

**Q:** What changes if two processes withdraw from the same persisted account through separate object instances?

**A:** A private field in each instance does not serialize shared writes. The implementation needs a transaction or concurrency mechanism that enforces the invariant across those instances.

**Q:** Two implementations have the same interface. Does that establish low coupling?

**A:** It can hide representation differences, but callers still depend on behavior, errors, timing and availability. Evaluate the actual change or failure that can propagate across the interface.

### Preserved OOP interview prompts

**Q:** "What's the difference between abstraction and encapsulation?"

**A:** Abstraction gives callers the essential operation contract while hiding implementation detail. Encapsulation keeps state changes behind paths that maintain the object's invariants. A small interface can still expose unsafe mutation, so one does not prove the other.

**Q:** "What's the difference between inheritance and composition?"

**A:** Inheritance supplies a subtype relationship and potentially shared implementation. Composition delegates to a collaborator or models owned parts. Choose inheritance when substitution is valid, and delegation when reuse does not require that promise.

**Q:** "What's polymorphism and why is it useful?"

**A:** One call can work across different implementations of a shared contract. In the shape loop, runtime dispatch selects the circle or rectangle method without a caller-side type branch. Generic identity preserves a type relationship with one implementation; Java overloads select an operation from compile-time argument types.

**Q:** "When would you use an abstract class vs an interface?"

**A:** Use an abstract class for a justified shared runtime implementation and inheritance contract. A TypeScript interface is an erased type contract with no default method bodies. Java classes have one direct superclass and can implement multiple interfaces; Java interfaces can define default methods, so the details depend on the language.

**Q:** "Explain aggregation vs composition."

**A:** Aggregation is shared whole-part grouping. Composition models exclusive ownership and lifecycle responsibility. Runtime references, storage cleanup, and removal rules still need implementation; a diamond does not perform garbage collection or cascade database deletion.

## UML Basics — Class & Sequence Diagrams

Source: [UML Basics — Class & Sequence Diagrams](30.1.1.04-uml-basics.md)

**Q:** Which UML view helps diagnose a request that calls the right classes in the wrong order?

**A:** A sequence diagram shows messages and their order over time. A class diagram describes structural relationships but does not establish that runtime sequence.

**Q:** Read the library diagram's borrowing association. How many current borrowers can one copy have, and can one member borrow several copies?

**A:** A copy has zero or one current borrower, while a member can borrow zero or more copies. Multiplicity beside an end counts that end's instances per instance at the opposite end. These labels do not preserve loan history.

**Q:** The lot reserved a spot but ticket creation failed. Why does the class diagram alone not settle the outcome?

**A:** It describes allowed relationships, not the operation's recovery policy. The sequence exposes the failure point; the implementation must release the reservation or recover the same operation, and serialize competing reservations through the appropriate shared mechanism.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
