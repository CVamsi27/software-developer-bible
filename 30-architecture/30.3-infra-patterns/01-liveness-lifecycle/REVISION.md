<!-- section: Infra Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Infra%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Liveness Lifecycle — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Health Checks & Graceful Shutdown — Liveness, Readiness, SIGTERM

Source: [Health Checks & Graceful Shutdown — Liveness, Readiness, SIGTERM](30.3.1.01-health-checks-graceful-shutdown.md)

**Q:** Why should a dependency outage normally fail readiness before liveness?

**A:** Readiness withdraws traffic when the instance cannot serve. Restarting every instance for a shared dependency failure can create a restart storm without repairing that dependency.

**Q:** What is the shutdown order for a serving process?

**A:** Withdraw readiness, stop admitting work, drain accepted requests within a deadline, close resources and exit before forced termination.

**Q:** Why should liveness not depend on every downstream service?

**A:** A shared outage can restart every instance without repairing the dependency and can make recovery harder.

**Q:** What must a shutdown deadline reserve time for?

**A:** The slowest permitted in-flight work plus cleanup, with a forced-exit boundary shorter than the platform termination grace period.

**Q:** Why does a green probe not prove the business path works?

**A:** A probe checks a selected signal. Synthetic transactions or other end-to-end evidence are needed for important dependencies and workflows.

**Q:** Does closing a Node.js HTTP listener immediately reset every active response?

**A:** No. It stops new connections and allows ordinary active work to complete under its lifecycle contract. Await drain before closing required dependencies; upgraded sockets need separate handling.

**Q:** A preStop hook sleeps twenty seconds inside a thirty-second termination grace. How much application drain time remains?

**A:** The hook uses the same grace countdown, leaving roughly ten seconds before scheduling/cleanup margins. The sleep does not prove routing propagation completed.

**Q:** An optional cache is down but the service has a safe database path. Must every readiness check fail?

**A:** Not automatically. Decide readiness from actual serving/admission capability, degrade safely and observe downstream capacity. Removing the whole fleet can worsen a shared outage.

**Q:** What's the difference between liveness and readiness probes?

**A:** Liveness selects a restart action useful for local failure; readiness controls eligibility for new routed work. A selected health signal is not complete business-path evidence.

**Q:** How do you handle graceful shutdown in Node.js?

**A:** Use one shutdown owner, withdraw/stop admission, await accepted HTTP/work drain within a deadline, then close dependencies. Handle streams/workers separately and preserve abrupt-death recovery.

**Q:** What happens if you don't have graceful shutdown?

**A:** Accepted work may be interrupted and replies lost. Durable transactions can survive while callers remain uncertain; recovery/deduplication matters rather than assuming every interruption is a 500 or data corruption.

**Q:** Does a Kubernetes `preStop` hook add time before the termination grace period starts?

**A:** No. The hook runs inside the same termination budget. A twenty-second sleep in a thirty-second grace period leaves roughly ten seconds for signal handling and application cleanup, so measure the real drain instead. See [Pod termination lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/).

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
