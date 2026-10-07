# 03 — Background Jobs: Commit Intent, Claim Work and Handle Repeated Effects

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



## Definition

A **job queue** stores work for a worker to execute. A **transactional outbox** stores an event alongside the business change that caused it, so a crash between database commit and notification does not erase the intent.

> **Textbook Definition:** A durable job queue persists work for later execution; a transactional outbox atomically persists publication intent with a local business change. Both require explicit claim, retry and effect-recovery protocols.

Suppose a prescription must produce a PDF. Saving the prescription and then scheduling its PDF in a separate operation creates a gap: the first write can commit and the second can fail. Writing durable intent in the same database transaction closes that particular gap. It does not make the PDF generation or notification occur exactly once.

This case describes source inspected on **2 October 2026**, with limitations distinguished from the intended design. Production throughput, latency, cost and delivery outcomes were not measured in this review.

## First Principles

A database transaction can commit related database writes atomically: all of those writes succeed together or none takes effect. It cannot generally include an external provider's action, such as sending a message, in that same commit. A worker can crash after completing the action but before recording completion, so recovery must allow repeated attempts and consumers must account for duplicates.

There are therefore three separate responsibilities:

```text
producer: commit business state + durable intent
worker/relay: claim pending intent and attempt delivery
consumer: apply the effect safely, including repeated attempts
```

## Why Use PostgreSQL for Durable Intent?

PostgreSQL can store business data and pending work in one transaction without introducing another queue service. That reduces a particular dual-write problem and reuses an existing operational system.

It still adds database load, indexes, cleanup, recovery and monitoring work. Queue contention can affect interactive queries. A broker can improve specialized routing, buffering or throughput, but a broker alone also does not make a separate database write atomic: an outbox or another coordination protocol may still be required.

Choose from measured workload, acceptable delay, failure recovery and operational capacity. Fixed comparisons such as “Postgres supports 1k jobs/sec” or “Kafka costs $100” are not portable design limits.

## How the Queue Claims One Job

The inspected repository claims a due job and changes its state in **one SQL statement**. This is the source query structure; `${name}` is a bound Prisma tagged-template value, not string concatenation:

```sql
UPDATE "QueueJob"
SET status = 'ACTIVE', "processedAt" = NOW(), "updatedAt" = NOW()
WHERE id = (
  SELECT id FROM "QueueJob"
  WHERE name = ${name}
    AND status IN ('WAITING', 'DELAYED')
    AND ("delayedUntil" IS NULL OR "delayedUntil" <= NOW())
  ORDER BY priority DESC, "createdAt" ASC
  LIMIT 1
  FOR UPDATE SKIP LOCKED
)
RETURNING *;
```

The inner query locks a candidate; competing claimers skip locked rows. The outer update records `ACTIVE` before the statement commits. A plain select followed later by an unrelated update would leave a competing-claim window.

The lock protects the claim while the database transaction holds it. It does not remain held throughout the external work after the claim commits. `SKIP LOCKED` is useful for work distribution, not a promise of exactly-once processing or strict global fairness. High-priority traffic can keep lower-priority work waiting.

### Trace a PDF Job Through Its States

| Step | State or action | Failure boundary |
| ---- | ---------------------------------------------------------------- | ----------------------------------------------------------- |
| 1 | Insert `WAITING`, or `DELAYED` with a due time | Intent must be durable before reporting reliable scheduling |
| 2 | Atomic claim changes a due row to `ACTIVE` | Another normal claimer skips the locked candidate |
| 3 | Await the registered handler | Provider may succeed even if its response is lost |
| 4 | Write `COMPLETED` after handler success | A crash between effect and completion permits repetition |
| 5 | On observed failure, increment attempts and delay or dead-letter | Retry does not undo an already-applied effect |

The source polls every **2 seconds**, prevents overlapping polls for the same job name within one service instance and claims one job per poll. A slow handler stretches effective processing capacity; a two-second interval is not a guaranteed two-second completion latency.

### The Queue's Duplicate Check Has Limits

`enqueue` looks for a matching **completed** job from the preceding **24 hours**. A similar check runs after claim. The current `QueueJob` schema has an indexed, nullable idempotency key, without a unique constraint on that key.

Two jobs with the same logical key can both find no completed predecessor and run concurrently. A completed-job lookup also does not protect the crash window before completion is recorded. Scope keys to the business operation and tenant where appropriate, then enforce idempotency at the actual effect boundary—for example, a database uniqueness constraint plus a transaction, or a provider-supported idempotency key with understood retention rules.

## How Retry and Stale Recovery Differ

The queue defaults to **5 attempts**. Its failure path uses a one-second exponential base with a sixty-second cap. Although the options interface accepts a backoff setting, this inspected failure path uses its own constants; do not assume every supplied delay is honored.

Jobs `ACTIVE` for more than **10 minutes** are candidates for recovery. The repository moves eligible rows to `DELAYED`, increments attempts and uses a **30-second** recovery delay; exhausted stale rows become `FAILED`. Ordinary handler failures can instead reach `DEAD_LETTERED`.

A long-running worker may still be alive when a timeout expires. Requeuing its job can permit another worker to begin while the first continues. The inspected completion write identifies the job by ID, rather than a claim generation. Heartbeats, leases and fencing or conditional state updates are possible ways to control this risk; a timeout alone does not establish ownership.

`interval.unref()` lets a timer stop keeping the Node process alive. It does not cancel running handlers or drain them. The queue's destruction hook clears pollers; safe shutdown additionally needs to stop new claims and decide how to finish or recover in-flight work.

## How the Outbox Couples an Event to a Business Write

`OutboxService.append(tx, event)` writes through the caller's transaction client. Its atomicity depends on the business write using that **same** transaction and committing successfully.

```text
transaction begins
  write business change using tx
  append OutboxEvent using tx
transaction commits both, or rolls back both

later: relay attempts dispatch → records result
```

The inspected generic queue `enqueue` does not take a transaction client parameter. Likewise, `PdfJobService.enqueue` creates its PDF status row and subsequently calls the queue; those two calls are not explicitly enclosed in one transaction there. Do not claim every producer is transactional merely because the queue uses PostgreSQL. Trace the actual call path and ambient transaction routing when evaluating each producer.

The outbox schema gives its optional idempotency key a unique constraint. The append service catches a Prisma `P2002` and treats a keyed duplicate as a no-op. That is intended duplicate handling; inside PostgreSQL transactions, a statement failure can leave the transaction aborted. Verify the caller's complete transaction behavior, or use a conflict-safe insert protocol rather than assuming catching the exception restores it.

## What the Current Relay Actually Acknowledges

The relay schedule is **every 5 seconds** in `CRON_SCHEDULES.OUTBOX_RELAY`. It selects up to **200** eligible rows, increments attempts and dispatches each through the process-local EventEmitter2. It adds outbox, aggregate and clinic identifiers to the payload, then records `processedAt`.

A local running flag avoids overlapping drains in one instance. A transaction-scoped PostgreSQL advisory lock coordinates instances that use the same lock convention. The helper holds that lock while awaiting its callback, but passes no transaction client to the callback; the relay uses the Prisma service. Do not assume the advisory lock proves all callback queries use the lock transaction or that external work becomes transactional.

### Dispatch Is Not Consumer Completion

The relay calls `events.emit`, not an awaited asynchronous-listener acknowledgment. A local probe of the installed **EventEmitter2 6.4.9** showed `emit` returning while an async listener was still waiting. The relay can therefore record `processedAt` before that listener completes.

This establishes an API behavior and a source-level acknowledgment boundary, not a claim that a particular production listener failed. It means “processed” here cannot be assumed to mean every downstream side effect completed durably. Also, an in-process emitter reaches listeners in that process; an outbox does not automatically broadcast the event to every replica.

On a caught dispatch error, the relay records the error and schedules exponential retry with a **5-second base**, **5-minute cap** and **8-attempt ceiling**. `Promise.allSettled` lets separate row tasks finish independently. None of these mechanisms guarantees eventual success: exhausted rows, absent listeners, asynchronous failures, downtime and operational replay all matter.

## Real-World Decisions

| Requirement | Mechanism to evaluate | Remaining boundary |
| ----------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| Business change must retain work intent | Same-transaction enqueue or outbox append | Verify every producer uses the transaction |
| Multiple workers should claim different rows | Atomic state transition with row locks | Recovery can still repeat work |
| Repeated provider calls must not charge or send twice | Effect-level idempotency | Provider retention and ambiguous outcomes |
| Long jobs must survive restarts safely | Lease/heartbeat and claim ownership protocol | An expired worker may still perform an effect |
| Relay completion must mean consumer completion | Awaited, failure-reporting handoff to a durable consumer | Successful handoff is not necessarily final effect completion |
| Sensitive events need asynchronous processing | Store minimal identifiers; validate worker scope | IDs and metadata can still be sensitive |

Do not put plaintext health information into generic event payloads or error messages. Fetch protected data through authorized, tenant-aware access. The current `runUnrestricted` helper changes application bypass context; as the [tenant-isolation case](02-multi-tenancy-rls.md) explains, it is not itself a database-role change or an automatic RLS disable operation.

## Mistakes

- Equating row-locking with exactly-once external effects.
- Assuming a completed-job lookup blocks concurrent duplicate jobs.
- Claiming every PostgreSQL enqueue shares the business transaction.
- Treating a synchronous emitter return as an async consumer acknowledgment.
- Describing a polling interval as an end-to-end latency guarantee.
- Advertising zero operational cost, zero lost events or harmless duplicates without measured evidence.

## Best Practices

Test the crash boundaries: before commit, after commit, after claim, after the external effect and before completion. Include concurrent duplicate jobs, a long handler crossing the stale timeout, exhausted retries, shutdown and tenant scope. Observe backlog age, active duration, retry/dead-letter rates and recovery behavior. Before replaying a failed item, establish whether its effect already occurred.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Current strengths | Atomic job claiming, delayed retries and an outbox provide useful building blocks. |
| Current limitations | Claim ownership, completion fencing, local asynchronous listeners and enqueue transaction boundaries leave failure gaps. |
| Recommended design | Commit required work with business state; claim with an ownership token, renew bounded leases, fence completion, and make consumer effects idempotent under stable operation keys. |
| Evidence needed | Fault injection at claim/effect/ack boundaries preserves required work; duplicate delivery produces one business effect; an expired claimant cannot acknowledge a replacement claim. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

PostgreSQL can atomically retain work intent and coordinate claims. Reliable execution additionally needs verified producer transactions, explicit ownership and recovery, effect-level idempotency and meaningful consumer acknowledgments. The inspected implementation has useful building blocks and limitations that must remain visible when describing its guarantees.

## See Also

- [Category revision](REVISION.md) — source-linked questions after the case studies.
- [Architecture decisions](01-architecture-decisions.md) — API and worker lifecycles.
- [Tenant isolation](02-multi-tenancy-rls.md) — scope and database enforcement.
- [Payment flows](04-payment-flows.md) — duplicate and ambiguous payment outcomes.
- [Case-study index](INDEX.md) — learning order.

## References

Source paths refer to the Docita repository inspected on 2 October 2026:

- `apps/api/src/shared/modules/queue/postgres-queue.service.ts`
- `apps/api/src/shared/modules/queue/infrastructure/prisma-queue-job.repository.ts`
- `apps/api/src/shared/modules/queue/pdf-job.service.ts`
- `apps/api/src/shared/modules/outbox/outbox.service.ts`
- `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts`
- `apps/api/src/shared/common/utils/postgres-advisory-lock.ts`
- `apps/api/src/shared/schedule/cron-schedules.ts`
- `packages/db/prisma/schema.prisma` — `QueueJob` and `OutboxEvent` models.
