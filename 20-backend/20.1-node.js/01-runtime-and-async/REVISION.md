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

## Web Streams and Test Runner

Source: [Web Streams and Test Runner](20.1.1.02-web-streams-and-test-runner.md)

**Q:** Why can per-chunk Buffer.toString corrupt a response while TextDecoderStream preserves it?

**A:** A multi-byte UTF-8 sequence can span chunks. The streaming decoder retains incomplete bytes until the next chunk instead of replacing them separately.

**Q:** What makes a streamed export unbounded even when its cursor is lazy?

**A:** Ignoring writable backpressure or producing oversized records can queue data faster than the client drains. Bound records and let demand propagate upstream.

**Q:** Does running native TypeScript tests prove the project type-checks?

**A:** No. Native execution strips supported type syntax; run an actual TypeScript checker separately and account for unsupported transformations.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide the API documentation and further reading.
