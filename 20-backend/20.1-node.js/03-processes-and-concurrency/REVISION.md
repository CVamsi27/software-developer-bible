<!-- section: Node.js | category: Reference | tags: revision | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Node.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
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

**Q:** With two workers listening on port 0, where do three requests on one keep-alive connection go?

**A:** Both workers share the selected random listening port, but all requests on that connection stay on its assigned worker. Killing that worker closes its connection; replacement restores capacity, not the lost response. The primary disables restart before graceful shutdown.

**Q:** What changes if each of four workers opens a ten-connection pool in each of three replicas?

**A:** The combined budget can reach 120 connections, alongside multiplied heaps/native resources. Per-connection round-robin does not control database demand or guarantee even request work; measure admission and total external capacity.

## Child Processes & Workers

Source: [Child Processes & Workers](20.1.3.02-child-processes-workers.md)

**Q:** How does moving work to a worker differ from transferring its input buffer?

**A:** A worker executes in another V8 isolate. Input is cloned by default; a transferred eligible ArrayBuffer changes ownership and detaches the sender view. SharedArrayBuffer instead exposes shared storage requiring synchronization.

**Q:** Why count outstanding work around a worker pool instead of relying only on queue settings?

**A:** Pool cancellation and scheduling paths can maintain internal queues differently. An application counter bounds accepted active plus pending tasks until their promises settle and makes overload rejection explicit.

**Q:** Can shell-free execFile make an arbitrary command safe?

**A:** It avoids shell interpretation, but the executable still interprets options and can read files or perform other privileged actions. Fix the command and validate allowed arguments, paths, output size and execution time.

**Q:** Trace runOne with iterations 4, then with invalid input, no result and a hung worker.

**A:** The compute fixture resolves its sum 4.146264369941973 after owned termination. Invalid iterations reject through the worker error; clean exit without a message rejects; no completion reaches the timer and rejects. Each terminal path settles once rather than sharing an uncorrelated message across tasks.

**Q:** What changes when new work arrives after closePool begins?

**A:** The example stops application admission before awaiting Piscina close. Later calls reject as closing; accepted work still follows the release's graceful/forced shutdown contract. An abort cannot undo an already completed external effect, and shared bytes require their own synchronization protocol.

## Process & Environment

Source: [Process & Environment](20.1.3.03-process-environment.md)

**Q:** Why is parseInt an unsafe validator for a port setting?

**A:** It accepts an integer prefix such as 10junk. Validate the entire string and the numeric range; distinguish an absent setting from the deliberately valid port zero.

**Q:** Why must cleanup share a deadline with draining requests?

**A:** A resource close can hang after server.close finishes. The deadline covers both stages; repeated signals reuse the same shutdown operation rather than starting parallel cleanup.

**Q:** What does process.exitCode provide that process.exit does not?

**A:** It sets the eventual status while allowing pending writes and owned cleanup to finish. process.exit terminates immediately and can truncate output; use it deliberately at the forced shutdown deadline.

**Q:** Why does PORT="0" remain 0 and DEBUG="false" remain false in the config fixture?

**A:** The parser distinguishes absent values, validates the entire string/range and compares an allowed boolean string. A truthiness fallback would replace zero or treat the string false as true. Empty or 10junk port values fail explicitly.

**Q:** What happens when shutdown is called twice while resource cleanup hangs?

**A:** Both calls return the same operation, admission is draining, and the deadline covers server drain plus resource close. If cleanup cannot finish, the forced failure path owns termination; process exitCode alone cannot release a leaked handle.

## PM2 Process Supervision

Source: [PM2 Process Supervision](20.1.3.04-pm2-process-supervision.md), [PM2 process management](https://pm2.io/docs/runtime/guide/process-management/) and [PM2 graceful startup and shutdown](https://pm2.io/docs/runtime/best-practices/graceful-shutdown/)

**Q:** What does `pm2 save` preserve, and what must be configured for a host reboot?

**A:** It saves the PM2 process list so it can be resurrected. A host startup integration must also invoke resurrection after reboot. Neither restores process memory, database state or an in-flight request.

**Q:** A worker has opened its port but cannot reach its database. Should a rolling reload treat it as ready?

**A:** No. Listening proves that the socket is open, not that the service can safely accept its required work. Use an application readiness signal after required initialization. Treat `listen_timeout` as a bound, not proof of health: PM2 may mark the worker ready when it expires, so the deployment must detect and reject an unhealthy release.

**Q:** A payment request times out while its worker is being replaced. What does restarting the worker tell the client?

**A:** Only that PM2 restored a process slot. It does not reveal whether the database commit happened before the connection closed. Resolve the outcome by idempotency key or reconciliation; blind retry can duplicate an effect.

## Watt Runtime Architecture

Source: [Watt Runtime Architecture](20.1.3.05-watt-runtime-architecture.md) and [Watt architecture](https://docs.platformatic.dev/docs/concepts/watt-architecture)

**Q:** Does a `.plt.local` fetch use the operating system's network stack?

**A:** In Watt's documented internal mesh, an Undici dispatcher routes the HTTP-shaped request over a `MessagePort` to the target worker. It avoids TCP and DNS, but request and response data still cross a thread boundary and consume resources.

**Q:** A Watt worker is replaced after a crash. Which state and failures should you inspect?

**A:** The replacement has a new isolate and does not recover the old worker's in-memory objects. Other workers may remain active, but a native crash, process-wide memory exhaustion or runtime exit can affect the whole Watt process.

**Q:** Two Watt applications share a runtime but need different release schedules. Does a worker boundary provide that independence?

**A:** No. Worker threads separate JavaScript heaps and event loops, but applications in one runtime share its process and deployment lifecycle. Move one to a separate runtime or service if release, scaling, compliance or process-failure boundaries must be independent.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md) — revisit bounded admission before comparing worker and process lifetimes

## References & Learn More

The linked source chapters provide the API documentation and further reading.
