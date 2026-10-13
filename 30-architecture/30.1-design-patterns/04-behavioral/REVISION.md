<!-- section: Design Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Design%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Behavioral — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Strategy Pattern

Source: [Strategy Pattern](30.1.4.01-strategy.md)

**Q:** Why can a Strategy be a function rather than a class?

**A:** The pattern needs an interchangeable behavioral contract; a function can satisfy it when no object lifecycle or additional methods are needed.

**Q:** Trace the standard quote for weight 2 and distance 100.

**A:** The client validates input, invokes standard, obtains 5 + 2 × 2 + 100 × 0.01 = 10, validates the result, and returns it. Pickup uses the same workflow and returns zero.

**Q:** What if the chosen policy returns NaN or begins calling a carrier API?

**A:** The current workflow rejects NaN, and an exception thrown by the selected policy propagates unchanged. An I/O-backed policy needs a compatible asynchronous contract with deadlines, failure, and cancellation rules; a shared function signature alone is insufficient.

## Observer Pattern

Source: [Observer Pattern](30.1.4.02-observer.md)

**Q:** Why should an Observer registration have a clear unsubscribe owner?

**A:** A retained subscriber can keep objects alive and receive events after its lifetime. Registration cleanup also prevents duplicated callbacks after remount or reconnect.

**Q:** Trace the once-listener that emits the price recursively.

**A:** The outer call runs display(100), then the once listener. That registration is removed before its callback, so the recursive emission runs only display(101). Later cleanup leaves no listeners.

**Q:** What if an ordinary listener throws or returns an unresolved promise?

**A:** A throw stops synchronous dispatch. `emit` does not await returned promises; `captureRejections` is opt-in and routes rejections asynchronously to the rejection hook or `'error'` event without making delivery awaitable. Observer alone does not choose a durable queued contract.

## Chain of Responsibility

Source: [Chain of Responsibility](30.1.4.03-chain-of-responsibility.md)

**Q:** What must a Chain of Responsibility define besides handler order?

**A:** Whether a handler stops or forwards the request, what happens when none handles it, and how errors propagate. Express 5 forwards rejected returned promises; Express 4 requires async failures to reach `next(err)`.

**Q:** Trace an urgent billing ticket and an ordinary unknown ticket.

**A:** Emergency handles the urgent ticket first and stops traversal. All handlers decline the ordinary unknown ticket, so the explicit triage fallback handles it.

**Q:** What if a generic billing handler moves ahead of emergency?

**A:** It can handle the urgent billing ticket first and bypass the emergency policy. Ordered routing is observable; handler order is part of correctness.

## State Pattern & State Machines

Source: [State Pattern & State Machines](30.1.4.04-state.md)

**Q:** When is a State pattern more appropriate than a Strategy?

**A:** When behavior follows an object's lifecycle state and transitions between states are part of its rules. A Strategy usually represents a chosen interchangeable policy.

**Q:** Does a union and `switch` implementation use the GoF State object structure?

**A:** No. It can model the same finite states and legal transitions, but GoF State specifically delegates behavior from a context to a replaceable state object. Choose the representation that keeps the lifecycle rules clear.

**Q:** Trace PAY then SHIP from pending.

**A:** PAY returns paid with the supplied timestamp; SHIP from paid returns shipped with tracking and timestamp. SHIP directly from pending throws because no legal transition accepts it.

**Q:** What if two requests validate against the same persisted version?

**A:** Both can be individually legal while racing. Use a conditional/versioned update or transaction lock, then reload and reevaluate conflicts. A pure function is not a shared-storage atomicity mechanism.

## Template Method Pattern

Source: [Template Method Pattern](30.1.4.05-template-method.md)

**Q:** Where is the variation point in Template Method?

**A:** A base algorithm fixes the overall sequence and delegates selected steps to overridable operations. Subclasses should not accidentally break that sequencing contract.

**Q:** Trace the JSON exporter from spaced records to output.

**A:** The base trims records, calls the subclass format, invokes its optional hook, and returns the JSON string. Subclass dispatch changes formatting without copying the sequence.

**Q:** What if formatting or the success hook throws?

**A:** A formatting failure skips the success hook. A hook failure makes the call fail even after output exists. Resource cleanup requires its own try/finally and error precedence policy.

## Iterator Pattern

Source: [Iterator Pattern](30.1.4.06-iterator.md)

**Q:** What happens if a collection changes while an iterator is in use?

**A:** The collection defines the rule. JavaScript Array iterators can visit appended elements; Map and Set iterators can visit new entries and skip entries deleted before visitation. Snapshot and fail-fast behavior are separate contracts a custom iterator may provide.

**Q:** Trace range(1,3) when the consumer breaks at 2.

**A:** The generator's `<=` condition makes 3 the inclusive endpoint. Creating it runs no body; requests yield 1 and 2, and `break` closes it before 3 is produced.

**Q:** What if an array appends items during live iteration?

**A:** Its standard iterator reads current length while advancing and may visit appended items. Repeated appending can prevent completion; custom iterators may instead promise snapshots or reject mutation.

**Q:** When does an iterator-helper pipeline allocate its result, and where can it run?

**A:** `Iterator.from(iterable).map(...).filter(...).take(3)` pulls values lazily; `toArray()` consumes the pipeline and materializes the result. Helpers are methods on iterators, not arbitrary iterables, and older runtimes may lack ES2025 support.

**Q:** Does breaking from `for await...of` cancel a page request?

**A:** Early exit calls and awaits the iterator's `return()` method when present, allowing cleanup. That does not automatically abort the request; pass an `AbortSignal` and define who owns cancellation.

## Mediator Pattern

Source: [Mediator Pattern](30.1.4.07-mediator.md)

**Q:** How can a Mediator become the next coupling problem?

**A:** If it absorbs every collaborator's domain rules, it becomes a large central dependency. Keep its responsibility focused on coordination and preserve cohesive participant behavior.

**Q:** Trace title then body edits through the form coordinator.

**A:** Initial and title-only state leave submission disabled. The body edit makes both trimmed fields nonempty, and the mediator enables the button without one widget reaching into another.

**Q:** What if updating a widget automatically emits the identical change back?

**A:** It can create a feedback loop. Compare before writing or distinguish event origin/version. UI enablement still does not establish server validation or permission.

**Q:** Does routing field events through a message bus make it a Mediator?

**A:** Not by itself. A mediator owns the interaction policy and chooses the resulting collaborator actions; a generic bus transports messages. A broker may define persistence, retries or cross-process delivery; the example only coordinates synchronous in-process calls.

## Memento Pattern

Source: [Memento Pattern](30.1.4.08-memento.md)

**Q:** Why does storing a reference to the current state fail as a Memento for mutable data?

**A:** Later mutation changes the supposedly saved state. Capture a snapshot or persistent immutable version with a defined restoration boundary.

**Q:** Trace save first, edit second, then restore the token.

**A:** The editor privately associates the token with the string `first`. The caretaker retains that token; restoration asks the editor to resolve it, and history never inspects the saved value.

**Q:** What if another editor restores that token or an external payment already occurred?

**A:** The other editor rejects an unknown token. Local restoration cannot reverse external effects; define a separate compensation and concurrency boundary.

**Q:** What must change before an in-memory snapshot token can cross a process or version boundary?

**A:** This example's `WeakMap` token is identity-based and process-local. A portable snapshot needs an explicit serializable schema, runtime validation and version migration; it also needs an authenticity boundary if untrusted writers can supply it.

## Command Pattern

Source: [Command Pattern](30.1.4.09-command.md)

**Q:** Does turning a request into a Command automatically make undo possible?

**A:** No. Undo requires captured prior state or a valid inverse operation, and remote or irreversible effects may need compensation instead.

**Q:** Trace turn-on execution and undo when the light began off.

**A:** The command captures false, changes the receiver to true, then restores false and clears its execution guard during undo. It can execute again after that undo.

**Q:** What if another actor changes the light before undo, or a job worker redelivers the request?

**A:** Blindly restoring prior state can erase the other actor's change; use conflict rules or compensation. Durable redelivery needs operation identity and idempotency beyond the Command pattern.

## Visitor Pattern

Source: [Visitor Pattern](30.1.4.10-visitor.md)

**Q:** Why is Visitor attractive for a stable object structure with changing operations?

**A:** New visitors can add operations without editing every element. Adding a new element type instead requires changing the visitor contract and its implementations.

**Q:** Trace one heading through plain-text and outline visitors.

**A:** The heading accept method chooses visitor.heading; the selected visitor supplies the operation. Plain text and outline are different operations over the same node contract.

**Q:** What if an image node type is added?

**A:** The visitor contract and relevant implementations need another node-specific operation. Classic Visitor favors adding operations while node types stay stable; traversal remains separately owned.

## Interpreter Pattern

Source: [Interpreter Pattern](30.1.4.11-interpreter.md)

**Q:** When should a handwritten Interpreter give way to a parser or language toolkit?

**A:** Parsing and evaluation are separate jobs. Complex grammar or diagnostics can justify parser tooling, while an evaluator still supplies meaning. Exposed languages also need validation and capability/work limits; a small Interpreter example is not a full language implementation.

**Q:** Trace the directly built multiplication/addition tree with x=3.

**A:** Multiplication evaluates its left addition, which resolves x and adds 5 to get 8; its right literal is 2, giving 16. No string parsing occurred.

**Q:** What if x is missing, or an incoming tree has unsupported/deep nodes?

**A:** Missing x throws. External trees require shape/operator/finite-value checks and size/depth/work limits; the typed recursive example alone does not enforce those boundaries.

## Null Object Pattern

Source: [Null Object Pattern](30.1.4.12-null-object.md)

**Q:** When can a Null Object hide a serious bug?

**A:** When absence should be an error or requires caller attention. Use a benign default only where the domain explicitly allows doing nothing.

**Q:** Trace the two logger choices through processOrder.

**A:** The chosen logger is invoked in both cases. The no-op deliberately emits nothing; consoleLogging writes the second order message. The order operation returns normally in both.

**Q:** What if the logger is absent because required initialization failed?

**A:** Do not silently treat that as configured absence. Required failure must remain an explicit failure; neutral behavior is valid only where the complete contract allows it.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
