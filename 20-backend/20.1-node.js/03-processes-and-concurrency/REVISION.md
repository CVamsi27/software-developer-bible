<!-- section: Node.js | category: Reference | tags: revision | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Node.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Node.js — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Clustering

Source: [Clustering](20.1.3.01-clustering.md)

**Q:** Why can four cluster workers increase database pressure even when HTTP throughput stays constant?

**A:** Each process owns its heap, connection pool and libuv worker pool. A ten-connection database pool per worker permits forty connections; capacity must be budgeted across the deployment.

**Q:** Does round-robin cluster scheduling give each worker an equal number of HTTP requests?

**A:** The primary distributes new connections. Keep-alive requests and an established WebSocket stay on their connection, so request load can remain uneven.

**Q:** What must happen before the primary starts draining workers?

**A:** Disable replacement and cancel pending restart timers. Track workers until actual exit; send shutdown, wait for in-flight work and impose a final termination deadline.

## Child Processes & Workers

Source: [Child Processes & Workers](20.1.3.02-child-processes-workers.md)

**Q:** How does moving work to a worker differ from transferring its input buffer?

**A:** A worker executes in another V8 isolate. Input is cloned by default; a transferred eligible ArrayBuffer changes ownership and detaches the sender view. SharedArrayBuffer instead exposes shared storage requiring synchronization.

**Q:** Why count outstanding work around a worker pool instead of relying only on queue settings?

**A:** Pool cancellation and scheduling paths can maintain internal queues differently. An application counter bounds accepted active plus pending tasks until their promises settle and makes overload rejection explicit.

**Q:** Can shell-free execFile make an arbitrary command safe?

**A:** It avoids shell interpretation, but the executable still interprets options and can read files or perform other privileged actions. Fix the command and validate allowed arguments, paths, output size and execution time.

## Process & Environment

Source: [Process & Environment](20.1.3.03-process-environment.md)

**Q:** Why is parseInt an unsafe validator for a port setting?

**A:** It accepts an integer prefix such as 10junk. Validate the entire string and the numeric range; distinguish an absent setting from the deliberately valid port zero.

**Q:** Why must cleanup share a deadline with draining requests?

**A:** A resource close can hang after server.close finishes. The deadline covers both stages; repeated signals reuse the same shutdown operation rather than starting parallel cleanup.

**Q:** What does process.exitCode provide that process.exit does not?

**A:** It sets the eventual status while allowing pending writes and owned cleanup to finish. process.exit terminates immediately and can truncate output; use it deliberately at the forced shutdown deadline.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide the API documentation and further reading.
