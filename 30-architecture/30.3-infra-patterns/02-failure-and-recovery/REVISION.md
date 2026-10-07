<!-- section: Architecture | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Architecture-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Failure And Recovery — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Resilience Patterns — Circuit Breaker, Bulkhead, Retry, Idempotency

Source: [Resilience Patterns — Circuit Breaker, Bulkhead, Retry, Idempotency](30.3.2.01-resilience-patterns.md)

**Q:** What does a bulkhead bound that a circuit breaker does not?

**A:** Concurrent resource consumption for a workload or dependency. A breaker changes admission based on observed failures, but does not by itself bound all in-flight work.

## Retry Patterns

Source: [Retry Patterns](30.3.2.02-retry-patterns.md)

**Q:** Why does exponential backoff also need jitter and a retry budget?

**A:** Backoff alone can synchronize clients. Jitter spreads attempts, while a budget limits amplification when many original requests fail together.

## Idempotency Keys

Source: [Idempotency Keys](30.3.2.03-idempotency-keys.md)

**Q:** Which writes belong in one transaction for a replayable local mutation?

**A:** The operation claim, business mutation and stored response. External effects need receiver idempotency or reconciliation beyond that transaction.

**Q:** Can deleting an idempotency record re-enable a previously completed effect?

**A:** Yes, if the caller repeats the key after the service has forgotten it and the underlying operation lacks another uniqueness constraint. Define the supported retry horizon, retain records through it, and use durable business identifiers where duplicate effects must be prevented beyond that window.

## Feature Flags & Kill Switches

Source: [Feature Flags & Kill Switches](30.3.2.04-feature-flags-kill-switches.md)

**Q:** Why is an unavailable flag service a product policy decision?

**A:** The safe default depends on what the flag controls. A kill switch needs tested stale/offline behavior; blindly using a cached value may keep a dangerous path enabled.

## Backup Strategy & Restore Drills

Source: [Backup Strategy & Restore Drills](30.3.2.05-backup-strategy-restore-drills.md)

**Q:** What proves a backup can meet recovery objectives?

**A:** A timed restore that checks the recovered data’s meaning and consistency, verifies application behavior, and demonstrates switching service to the restored system. Successful upload or a checksum alone does not establish recovery time or usable data.

## Idempotency & Retry Patterns — Deep Dive

Source: [Idempotency & Retry Patterns — Deep Dive](30.3.2.06-idempotency-retry-deep-dive.md)

**Q:** Why should exhausting a retry budget not automatically trip every circuit breaker?

**A:** The mechanisms use different scopes and signals. A budget caps amplification; a breaker decides whether a particular dependency is currently worth calling.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
