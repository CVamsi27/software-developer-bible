<!-- section: Architecture | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Architecture-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Failure And Recovery — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Resilience Patterns — Circuit Breaker, Bulkhead, Retry, Idempotency

Source: [Resilience Patterns — Circuit Breaker, Bulkhead, Retry, Idempotency](30.3.2.01-resilience-patterns.md)

**Q:** What does a bulkhead bound that a circuit breaker does not?

**A:** Concurrent resource consumption for a workload or dependency. A breaker changes admission based on observed failures, but does not by itself bound all in-flight work.

**Q:** Does a circuit breaker outside retries observe the same failures as one around each attempt?

**A:** No. It can observe only the final operation outcome; attempt-level placement can count partial failures individually. Choose the signal/scope and separately bound admission, waiting and probes.

**Q:** Why must a late successful call not blindly close a newly opened breaker?

**A:** It was admitted under older state. Without a state-generation or equivalent synchronization policy, its result can override the newer recovery decision and admit another burst.

## Retry Patterns

Source: [Retry Patterns](30.3.2.02-retry-patterns.md)

**Q:** Why does exponential backoff also need jitter and a retry budget?

**A:** Backoff alone can synchronize clients. Jitter spreads attempts, while a budget limits amplification when many original requests fail together.

**Q:** How do you implement retry with exponential backoff?

**A:** Classify safe transient outcomes, share an overall deadline, and bound attempts plus additional-attempt tokens. A full-jitter example chooses from zero to the capped exponentially growing interval. Honor Retry-After when it fits; stop rather than shortening a required server wait. Caps and numbers come from the actual endpoint/workload contract.

**Q:** When should you NOT retry?

**A:** When the repeat can duplicate an unsupported effect, the same request is deterministically invalid, remaining time/capacity is insufficient, or policy refuses admission. 5xx, resets and timeouts are candidates, not an always-retry instruction; 429 can be retryable under its wait/safety contract.

**Q:** Can a response-header timeout bound body consumption too?

**A:** Only if the timer/signal remains active through consuming the body. Clearing it after fetch returns headers leaves a stalled body outside that bound.

## Idempotency Keys

Source: [Idempotency Keys](30.3.2.03-idempotency-keys.md)

**Q:** Which writes belong in one transaction for a replayable local mutation?

**A:** The operation claim, business mutation and stored response. External effects need receiver idempotency or reconciliation beyond that transaction.

**Q:** Can deleting an idempotency record re-enable a previously completed effect?

**A:** Yes, if the caller repeats the key after the service has forgotten it and the underlying operation lacks another uniqueness constraint. Define the supported retry horizon, retain records through it, and use durable business identifiers where duplicate effects must be prevented beyond that window.

**Q:** Why can a loser read the committed replay result after a conflicting insert at READ COMMITTED?

**A:** The conflict waits for the winner. Its subsequent SELECT is a new statement with a fresh snapshot; the committed effect/result are visible. Other isolation levels and serialization/deadlock failures need their own handling.

## Feature Flags & Kill Switches

Source: [Feature Flags & Kill Switches](30.3.2.04-feature-flags-kill-switches.md)

**Q:** Why is an unavailable flag service a product policy decision?

**A:** The safe default depends on what the flag controls. A kill switch needs tested stale/offline behavior; blindly using a cached value may keep a dangerous path enabled.

**Q:** How do you ship a feature to 1% of users safely?

**A:** Deploy compatible code with exposure disabled, assign a stable subject cohort, measure actual exposure and representative outcomes, and expand only on evidence. A percentage alone is not an experiment. Measure disabling across workers/instances and reconcile already committed work before removing the rollback path.

**Q:** What happens when your flag service goes down?

**A:** Existing local rules may remain available, but new/uninitialized or stale clients need an explicit default. The safe choice depends on the controlled capability. A failed refresh must not advance contact freshness; provider outage does not imply every user sees no effect.

**Q:** Does a 5% audience necessarily receive 5% of requests?

**A:** No. Deterministic subject buckets stabilize membership, but subjects generate unequal traffic and small populations vary. Measure actual exposure; increasing percentage preserves the old cohort only when subject identity, salt and algorithm remain fixed.

## Backup Strategy & Restore Drills

Source: [Backup Strategy & Restore Drills](30.3.2.05-backup-strategy-restore-drills.md)

**Q:** What proves a backup can meet recovery objectives?

**A:** A timed restore that checks the recovered data’s meaning and consistency, verifies application behavior, and demonstrates switching service to the restored system. Successful upload or a checksum alone does not establish recovery time or usable data.

**Q:** How would you design backups for a payments database?

**A:** Start from approved recovery/deletion/retention objectives and the failure model. Preserve verified base/history and independent restore access/keys, measure full restore capacity, fence writers and reconcile provider effects. Replicas protect some availability failures but also copy corrupt writes; retention years and “near-zero RPO” cannot be asserted without the actual contract/evidence.

**Q:** What does 'backup success' mean?

**A:** Record distinct evidence: protected artifact, verified bytes/load, correct recovered target state and measured service recovery. A successful upload alone proves neither RPO nor RTO. Alert on missing verified recovery points and drill the selected incident scenario.

**Q:** Why is a recent local file modification time not a recovery point?

**A:** Copying old bytes changes local metadata without adding newer source data. Use cataloged snapshot/log positions and complete verified history; an intentionally old PITR target also needs checks relative to that target rather than today.

## Idempotency & Retry Patterns — Deep Dive

Source: [Idempotency & Retry Patterns — Deep Dive](30.3.2.06-idempotency-retry-deep-dive.md)

**Q:** Why should exhausting a retry budget not automatically trip every circuit breaker?

**A:** The mechanisms use different scopes and signals. A budget caps amplification; a breaker decides whether a particular dependency is currently worth calling.

**Q:** Why can deduplicating all events by payment ID discard valid work?

**A:** Creation and refund are different logical events for the same payment. Deduplicate the intended event/operation identity and apply a separate ordering/version contract.

**Q:** Does a DLQ entry prove the remote effect failed?

**A:** No. A provider may have accepted the effect before the consumer timed out. Replay must preserve/reconcile the identity and consider provider deduplication retention, not create a new effect blindly.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
