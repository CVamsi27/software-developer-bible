# Node.js Production Runtime Architecture — Design

**Date:** 2026-10-14 · **Status:** Approved direction; awaiting review of this written spec
**User outcome:** Explain how Node.js applications are supervised and scaled in production, then choose a runtime boundary based on isolation, lifecycle, and operational needs.

## Context and gap

The Node.js learning group already teaches the event loop, child processes, worker threads, clustering, process configuration, signals, and graceful shutdown. Its clustering chapter briefly mentions PM2, yet has no chapter tracing a process manager's architecture or comparing it with an application runtime such as Watt. Readers therefore learn primitives without seeing how production tooling coordinates them.

Other stacks already contain focused internals chapters for React Fiber, PostgreSQL, Kafka, Docker, Nginx, and Git. This addition extends the existing Node.js process path rather than introducing a generic architecture survey or repeating those chapters.

## Approaches considered

| Approach | Benefit | Trade-off |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Add only a short PM2 reference | Smallest change | Leaves Watt and the process, thread, and runtime boundary unexplained |
| Add two connected Node.js chapters, then address other audited gaps in separate passes — **recommended** | Teaches requested tools through the architecture they implement and keeps each pass reviewable | The cross-stack backlog needs separate specs and implementation passes |
| Write one broad "internals across stacks" survey | Exposes many topics quickly | Produces shallow coverage, duplicates existing chapters, and weakens the learning flow |

## Design

Add two teaching chapters to `20-backend/20.1-node.js/03-processes-and-concurrency/` after the existing process, worker, and cluster fundamentals:

1. **Node.js Process Supervision with PM2** — explain the manager daemon and process list, how the command-line interface (CLI) controls managed applications, and how fork and cluster execution modes differ from restart policy, startup persistence, readiness, graceful reload, shutdown, and logs. Trace one start, one crash and restart, and one deployment reload, distinguishing successful replacement from a successful request or zero-downtime deployment. Compare responsibility boundaries against `systemd` and container orchestrators without treating them as interchangeable.
2. **Watt Runtime Architecture** — explain `wattpm` as the CLI and Watt as the runtime, tracing how the main thread supervises applications in worker threads with isolated heaps, module registries, and event loops. Follow dependency-aware startup, worker health and replacement, internal calls through the `.plt.local` mesh, shared telemetry, and single-unit deployment. State the limits of thread-level isolation: process-wide crashes and resource limits remain shared, and applications in one runtime ship together.

The chapters connect through an explicit comparison: PM2 cluster mode uses multiple processes, while Watt's documented application model uses worker threads in one process. Both can run under a host or container orchestrator, which remains responsible for host placement and container failure.

The comparison makes clear that neither option shares in-memory state across boundaries or makes external side effects exactly-once. It links to existing Node.js clustering, child-process and worker-thread, and process-lifecycle chapters for primitive details instead of repeating them.

### Reader flow and learning activity

Each chapter opens with a concrete production decision or failure. It introduces a textbook definition alongside the practical definition, derives the mechanism from process and thread boundaries, walks one lifecycle and request trace, and ends at the trade-off that changes deployment design.

Use one small topology diagram and one lifecycle table where they clarify ownership. Keep framework and vendor setup steps plus exhaustive CLI flags in official references while teaching the behavior needed during an interview or incident.

The practice activity asks the reader to run a minimal HTTP service under standalone Node, PM2 fork and cluster modes, and Watt. The learner exposes readiness and a process-local counter, issues a slow request, and triggers a worker failure and graceful shutdown. They record which state survives, which requests can fail, what the supervisor replaces, and which boundary owns recovery — without claiming zero downtime from process replacement alone or presenting local benchmark numbers as general performance evidence.

### Curriculum integration

- Add both chapters to the process and concurrency category `INDEX` in learning order, with short descriptions and reading times; update its reading flow from Node primitives to external supervision and then an in-process application runtime.
- Add them to the root Node.js `INDEX` through the repository count generator. Update the process `REVISION.md` with source-linked question groups for PM2 and Watt plus at least five fresh questions across the new concepts, and add a small senior-level process and runtime set to the Node interview bank where it adds distinct practice.
- Add See Also links from the new chapters to the existing clustering, worker, lifecycle, and Docker material while preserving existing chapter IDs, URLs, authored examples, and category order.
- Keep the remaining audited gaps as separate follow-on candidates rather than part of this implementation: Java Virtual Machine (JVM) runtime internals, Kubernetes control-plane request and reconciliation flow, the TypeScript compiler and module-resolution pipeline, Redis persistence, replication, and server architecture, and a connected V8 optimization and deoptimization path. Each receives its own gap check before a separate spec.

## Source-of-truth and accuracy rules

Use the official Node.js API docs for Node primitives, PM2 Runtime docs for PM2 behavior and configuration, and Platformatic's Watt architecture and runtime references for Watt-specific claims. Verify each linked behavior at authoring time, distinguish documented behavior from an inference or local demonstration, and avoid unstable defaults or version-specific claims unless the cited source is current and versioned; explain that graceful reload depends on application readiness and drain behavior, not only a PM2 command.

Initial references:

- [Node.js Cluster API](https://nodejs.org/api/cluster.html)
- [Node.js Worker Threads API](https://nodejs.org/api/worker_threads.html)
- [PM2 process management](https://pm2.io/docs/runtime/guide/process-management/)
- [PM2 load balancing](https://pm2.io/docs/runtime/guide/load-balancing/)
- [PM2 graceful startup and shutdown](https://pm2.io/docs/runtime/best-practices/graceful-shutdown/)
- [Watt architecture](https://docs.platformatic.dev/docs/concepts/watt-architecture)
- [Platformatic runtime multithread architecture](https://docs.platformatic.dev/docs/reference/runtime/multithread-architecture)

PM2 documentation describes a background daemon, a registered process list, cluster reload, and readiness and shutdown behavior. Platformatic's architecture guide describes one worker thread per application, a supervising runtime, an internal mesh, and process-level isolation limits.

These are product descriptions, not guarantees that a reader's workload will meet a particular throughput or availability target. Those claims were checked against [PM2 process management](https://pm2.io/docs/runtime/guide/process-management/), [PM2 graceful startup and shutdown](https://pm2.io/docs/runtime/best-practices/graceful-shutdown/), and [Watt architecture](https://docs.platformatic.dev/docs/concepts/watt-architecture).

## Acceptance criteria

- A senior Node.js developer can explain the process, thread, and runtime boundary and trace start, readiness, request routing, failure, replacement, and shutdown for both tools without conflating their models.
- Readers can identify what state is local, what survives a worker restart, and what fails at a shared process or deployment boundary.
- Content includes practical and textbook definitions, a distinct First Principles derivation, one final Summary, See Also, and References, following the repository's organic reading-flow rules.
- The `INDEX` and revision companion preserve the category's authored order and link to the new source chapters, while the interview bank adds only non-duplicative senior-level prompts.
- Authored practice can be completed from the chapter and official links and tests observable behavior rather than unsubstantiated performance claims.
- New citations are live and included in `scripts/external-links-baseline.json`, and counts are regenerated with `python3 scripts/check_counts.py --write`.
- Before the implementation commit or push, `bash scripts/verify.sh` and `python3 scripts/check_links.py` pass, and changed index, chapters, questions, and generated counts align.

## Risks and boundaries

PM2 and Watt are independently evolving products whose defaults and internals can drift. Keep the learning goal on architecture and observable contracts, date version claims that cannot be made version-neutral, and point setup details to official docs.

Thread isolation is easy to overstate: distinguish an isolated JavaScript heap and event loop from a separate process, container, or failure domain. This spec does not add or modify topics in the five follow-on areas.
