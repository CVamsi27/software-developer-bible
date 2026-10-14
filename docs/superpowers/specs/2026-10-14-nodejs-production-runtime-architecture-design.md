# Node.js Production Runtime Architecture — Design

**Date:** 2026-10-14 · **Status:** Approved direction; awaiting review of this written spec
**User outcome:** Explain how Node.js applications are supervised and scaled in production, then choose a runtime boundary based on isolation, lifecycle and operational needs.

## Context and gap

The Node.js learning group already teaches the event loop, child processes, worker threads, clustering, process configuration, signals and graceful shutdown. Its clustering chapter briefly mentions PM2, but the group has no chapter that traces a process manager's architecture or compares it with an application runtime such as Watt. Readers therefore learn the primitives without seeing how production tooling coordinates them.

Other stacks already contain focused internals chapters for React/Fiber, PostgreSQL, Kafka, Docker, Nginx and Git. This first addition should extend the existing Node.js process path rather than introduce a generic architecture survey or repeat those chapters.

## Approaches considered

| Approach | Benefit | Trade-off |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Add only a short PM2 reference | Smallest change | Leaves Watt and the process/thread/runtime boundary unexplained |
| Add two connected Node.js chapters, then address other audited gaps in separate passes — **recommended** | Teaches the requested tools through the architecture they implement and keeps each pass reviewable | The cross-stack backlog needs separate specs and implementation passes |
| Write one broad “internals across stacks” survey | Exposes many topics quickly | Produces shallow coverage, duplicates existing chapters and weakens the learning flow |

## Design

Add two teaching chapters to `20-backend/20.1-node.js/03-processes-and-concurrency/` after the existing process, worker and cluster fundamentals:

1. **Node.js Process Supervision with PM2** — explain the manager daemon and process list, how the CLI controls managed applications, fork and cluster execution modes, restart policy, startup persistence, readiness, graceful reload, shutdown and logs. Trace one start, one crash/restart and one deployment reload. Distinguish a successful replacement from a successful request or a zero-downtime deployment. Compare the responsibility boundary with systemd and a container orchestrator without treating them as interchangeable.
2. **Watt Runtime Architecture** — explain `wattpm` as the CLI and Watt as the runtime. Trace the runtime main thread supervising applications in worker threads; make each thread's isolate, heap, module registry and event loop concrete. Follow dependency-aware startup, worker health and replacement, internal application calls through the `.plt.local` mesh, shared telemetry, and the single deployment unit. State the limits of thread-level isolation: process-wide crashes and resource limits remain shared, and applications in one runtime ship together.

The chapters will be connected by an explicit comparison: PM2 cluster mode uses multiple processes; Watt's documented application model uses worker threads in one process; both can run under a host or container orchestrator, whose boundary remains responsible for host/container placement and failure. The comparison will state that no option makes in-memory state shared or makes external side effects exactly-once. It will link to the existing Node.js clustering, child-process/worker-thread and process-lifecycle chapters for primitive details instead of repeating them.

### Reader flow and learning activity

Each chapter opens with a concrete production decision or failure. It then introduces a textbook definition alongside the practical definition, derives the mechanism from process and thread boundaries, walks one lifecycle/request trace, and ends at the trade-off that changes deployment design. Use one small topology diagram and one lifecycle table where they clarify ownership. Keep framework/vendor setup steps and exhaustive CLI flags in official references; teach the behavior needed to reason during an interview or incident.

The practice activity asks the reader to run a minimal HTTP service under standalone Node, PM2 fork/cluster mode, and Watt; expose readiness and a process-local counter; issue a slow request; then trigger a worker failure and graceful shutdown. The learner records which state survives, which requests can fail, what the supervisor replaces, and which boundary owns the next recovery action. The exercise must not claim zero downtime from process replacement alone or present benchmark numbers as general performance evidence.

### Curriculum integration

- Add both chapters to the process/concurrency category INDEX in learning order, with short descriptions and reading times; update its reading flow to lead from Node primitives to external supervision and then to an in-process application runtime.
- Add them to the root Node.js INDEX through the repository's count generator. Update the process `REVISION.md` with source-linked question groups for PM2 and Watt and at least five fresh questions across the new concepts. Add a small senior-level process/runtime set to the existing Node interview bank if it adds distinct practice rather than copying revision prompts.
- Add See Also links from the new chapters to the existing clustering, worker, lifecycle and Docker material. Preserve existing chapter IDs, URLs, authored examples and category order.
- Keep the remaining audited gaps as separate follow-on candidates, not part of this implementation: JVM runtime internals; Kubernetes control-plane request/reconciliation flow; TypeScript compiler and module-resolution pipeline; Redis persistence/replication/server architecture; and a connected V8 optimization/deoptimization path. Each receives its own gap check before a separate spec.

## Source-of-truth and accuracy rules

Use the current official Node.js API docs for Node primitives, PM2 Runtime docs for PM2 behavior and configuration, and Platformatic's Watt architecture and runtime references for Watt-specific claims. Verify each linked behavior at authoring time; distinguish documented behavior from an inference or a local demonstration. Avoid unstable defaults and version-specific statements unless the cited source is current and the version is named. In particular, explain that graceful reload depends on application readiness and drain behavior, not only a PM2 command.

Initial references:

- [Node.js Cluster API](https://nodejs.org/api/cluster.html)
- [Node.js Worker Threads API](https://nodejs.org/api/worker_threads.html)
- [PM2 process management](https://pm2.io/docs/runtime/guide/process-management/)
- [PM2 load balancing](https://pm2.io/docs/runtime/guide/load-balancing/)
- [PM2 graceful startup and shutdown](https://pm2.io/docs/runtime/best-practices/graceful-shutdown/)
- [Watt architecture](https://docs.platformatic.dev/docs/concepts/watt-architecture)
- [Platformatic runtime multithread architecture](https://docs.platformatic.dev/docs/reference/runtime/multithread-architecture)

The PM2 documentation describes a background daemon and registered process list, and documents cluster reload and readiness/shutdown behavior. Platformatic's architecture guide describes one worker thread per application, a supervising runtime, an internal mesh and the process-level limits of that boundary. These are product descriptions, not guarantees that a reader's workload will meet a particular throughput or availability target. [PM2 process management](https://pm2.io/docs/runtime/guide/process-management/), [PM2 graceful startup and shutdown](https://pm2.io/docs/runtime/best-practices/graceful-shutdown/), [Watt architecture](https://docs.platformatic.dev/docs/concepts/watt-architecture)

## Acceptance criteria

- A senior Node.js developer can explain the process/thread/runtime boundary and trace start, readiness, request routing, failure, replacement and shutdown for both tools without conflating their models.
- Readers can identify what state is local, what survives a worker restart, and what fails at a shared process or deployment boundary.
- The content includes practical and textbook definitions, a distinct First Principles derivation, one final Summary, See Also and References, while following the repository's organic reading-flow rules.
- The INDEX and revision companion preserve the category's authored order and link to the new source chapters; the interview bank adds only non-duplicative senior-level prompts.
- The authored practice can be completed from the chapter and official links. It tests observable behavior, not unsubstantiated performance claims.
- New citations are live and included in `scripts/external-links-baseline.json`; counts are regenerated with `python3 scripts/check_counts.py --write`.
- Before the implementation commit or push, `bash scripts/verify.sh` and `python3 scripts/check_links.py` pass, and the changed index, chapters, questions and generated counts align.

## Risks and boundaries

PM2 and Watt are independently evolving products, so defaults and internal implementation details can drift. Keep the learning goal on architecture and observable contracts, date/version claims that cannot be made version-neutral, and point setup details to official docs. Thread isolation is easy to overstate: explicitly distinguish an isolated JavaScript heap/event loop from a separate process, container or failure domain. This spec does not add or modify topics in the five follow-on areas.
