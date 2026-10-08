<!-- section: Node.js | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Node.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Node.js — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Event Loop

Source: [Event Loop](20.1.1.01-event-loop.md)

**Q:** Why does awaiting a database call not prevent subsequent JSON parsing from delaying other requests?

**A:** Await suspends during the external wait. When the continuation resumes, JSON parsing executes synchronously on this JavaScript thread.

**Q:** Which resource usually handles a database socket, and which handles fs operations?

**A:** Socket readiness generally comes from the kernel event mechanism. Many asynchronous file operations use the libuv worker pool; increasing that pool does not parallelize arbitrary JavaScript.

**Q:** Why should a top-level timer/immediate test avoid asserting one fixed order?

**A:** Their relative eligibility depends on runtime context and timing. Inside an I/O callback, a newly scheduled immediate precedes its newly scheduled zero-delay timer; top-level ordering has no such general guarantee.

**Q:** Trace the CommonJS example from start through its file callback. Which order is promised?

**A:** Initial synchronous start/end precede nextTick then the promise continuation. Inside the successful file callback, its immediate precedes its newly scheduled zero-delay timer. Moving those two registrations to top level loses that portable relative-order guarantee; moving initial code to ES module evaluation also changes the microtask context.

**Q:** What changes if each slice's processItem performs one second of synchronous CPU work?

**A:** The five-millisecond budget is checked between items and cannot preempt one item. That callback still blocks the loop for the item duration. Reduce individual work or use a bounded worker/process protocol; awaiting database I/O does not move that CPU work off-thread.

## Web Streams and Test Runner

Source: [Web Streams and Test Runner](20.1.1.02-web-streams-and-test-runner.md)

**Q:** Why can per-chunk Buffer.toString corrupt a response while TextDecoderStream preserves it?

**A:** A multi-byte UTF-8 sequence can span chunks. The streaming decoder retains incomplete bytes until the next chunk instead of replacing them separately.

**Q:** What makes a streamed export unbounded even when its cursor is lazy?

**A:** Ignoring writable backpressure or producing oversized records can queue data faster than the client drains. Bound records and let demand propagate upstream.

**Q:** Does running native TypeScript tests prove the project type-checks?

**A:** No. Native execution strips supported type syntax; run an actual TypeScript checker separately and account for unsupported transformations.

**Q:** In the two-chunk Web Stream fixture, what happens before the returned pipeTo promise completes?

**A:** hello/world are transformed, sink writes are awaited in order, and the started generator reaches finally. The output is HELLO/WORLD with closed=true. A production sink still needs its own durable acknowledgment; an in-memory fixture is not a storage guarantee.

**Q:** What changes when the sink rejects or a UTF-8 euro character crosses chunks?

**A:** Default piping rejects and propagates cancellation upstream so owned resources must clean up. A streaming decoder retains the incomplete multibyte sequence and emits the correct character; independent per-chunk decoding can introduce replacement characters. Custom prevent-cancel/abort options change responsibility and need explicit cleanup.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md) — revisit callback scheduling before reasoning about cancellation and rejected work

## References & Learn More

The linked source chapters provide the API documentation and further reading.
