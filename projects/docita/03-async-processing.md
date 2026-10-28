# 03 — Background Jobs: Commit Intent, Claim Work and Handle Repeated Effects

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



Suppose a prescription must produce a PDF. Saving the prescription and then scheduling its PDF in a separate operation creates a gap: the first write can commit and the second can fail. Writing durable intent in the same database transaction closes that particular gap. It does not make the PDF generation or notification occur exactly once.

## Definition

A **job queue** stores work for a worker to execute. A **transactional outbox** stores an event alongside the business change that caused it, so a crash between database commit and notification does not erase the intent.

> **Textbook Definition:** A durable job queue persists work for later execution; a transactional outbox atomically persists publication intent with a local business change. Both require explicit claim, retry and effect-recovery protocols.

This case starts from source inspected on **2 October 2026**. A targeted **9 October 2026** recheck at local HEAD `dc5a97dc3` updated the relay acknowledgment; unrelated working-tree changes were present. A **15 October 2026** refresh inspected clean local HEAD `4e3032c2d0fd9d2ee74e7c74536fefef454d5a65` for queue claim fencing, outbox append and relay behavior, and ran the focused queue/outbox unit tests. The earlier dates remain historical inspections; this scoped refresh is not a production audit. Throughput, latency, cost and delivery outcomes were not measured.

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

The repository claims a due job, changes its state and records a fresh random `claimToken` in **one SQL statement**. This is the current source query structure; `${name}` and `${claimToken}` are bound Prisma tagged-template values, not string concatenation:

```sql
UPDATE "QueueJob"
SET status = 'ACTIVE', "processedAt" = NOW(),
    "claimToken" = ${claimToken}, "updatedAt" = NOW()
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

The inner query locks a candidate; competing claimers skip locked rows. The outer update records `ACTIVE` and its ownership token before the statement commits. A plain select followed later by an unrelated update would leave a competing-claim window.

The lock protects the claim while the database transaction holds it. It does not remain held throughout the external work after the claim commits. `SKIP LOCKED` is useful for work distribution, not a promise of exactly-once processing or strict global fairness. High-priority traffic can keep lower-priority work waiting.

### Trace a PDF Job Through Its States

| Step | State or action | Failure boundary |
| ---- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1 | Insert `WAITING`, or `DELAYED` with a due time | Intent must be durable before reporting reliable scheduling |
| 2 | Atomic claim changes a due row to `ACTIVE` with a fresh token | Another normal claimer skips the locked candidate |
| 3 | Await the registered handler | Provider may succeed even if its response is lost |
| 4 | Conditionally write `COMPLETED` after handler success | A lost claim cannot acknowledge; a crash after the effect permits repetition |
| 5 | Conditionally increment attempts and delay or dead-letter on failure | Retry does not undo an already-applied effect |

The source polls every **2 seconds**, prevents overlapping polls for the same job name within one service instance and claims one job per poll. A slow handler stretches effective processing capacity; a two-second interval is not a guaranteed two-second completion latency.

### The Queue's Duplicate Check Has Limits

`enqueue` looks for a matching **completed** job from the preceding **24 hours**. A similar check runs after claim. The current `QueueJob` schema has an indexed, nullable idempotency key, without a unique constraint on that key.

Two jobs with the same logical key can both find no completed predecessor and run concurrently. A completed-job lookup also does not protect the crash window before completion is recorded. Scope keys to the business operation and tenant where appropriate, then enforce idempotency at the actual effect boundary—for example, a database uniqueness constraint plus a transaction, or a provider-supported idempotency key with understood retention rules.

## How Retry and Stale Recovery Differ

The queue defaults to **5 attempts**. Its failure path uses a one-second exponential base with a sixty-second cap. Although the options interface accepts a backoff setting, this inspected failure path uses its own constants; do not assume every supplied delay is honored.

Jobs `ACTIVE` for more than **10 minutes** are candidates for recovery. The repository moves eligible rows to `DELAYED`, increments attempts and uses a **30-second** recovery delay; exhausted stale rows become `FAILED`. Ordinary handler failures can instead reach `DEAD_LETTERED`.

A long-running worker may still be alive when a timeout expires. Requeuing its job can permit another worker to begin while the first continues. The **15 October** source now fences acknowledgments: `QueueJobLifecycle.acknowledgeClaim` requires a token, and the repository updates only the matching `(id, claimToken)` row while its status is `ACTIVE`. Stale recovery clears the old token; a replacement claim receives a new one. Completion, retry, dead-letter and duplicate-skip acknowledgments use this same conditional path, so a late worker cannot overwrite its replacement's job state.

The focused queue unit tests passed for lost completion/retry acknowledgments, a missing token and the duplicate-skip path. These use repository mocks; they do not exercise competing PostgreSQL connections. Fencing a local acknowledgment also does not cancel the old handler or prevent it from repeating a provider effect. The inspected recovery protocol has a fixed stale threshold, not a renewable per-job lease.

`interval.unref()` lets a timer stop keeping the Node process alive. It does not cancel running handlers or drain them. A **28 October refresh at canonical source `f3fddffc0`** found a newer shutdown implementation: it marks the service as shutting down, clears polling timers and awaits the active poll promises before persistence closes. The focused `postgres-queue-shutdown.spec.ts` exercises those ownership/drain paths. The worker still applies an outer 15-second exit bound, so a long external effect can outlive that grace period; retain stale-claim recovery and effect idempotency rather than promising every shutdown completes every job.

## Separate a Default Retry Budget From the Caller’s Policy

The generic PostgreSQL queue defaults to five attempts. PDF enqueue explicitly requests three; a five-attempt headline would therefore misdescribe the PDF path. The generic retry loop derives delay from its own one-second exponential base and caps it at 60 seconds. A caller's requested backoff option is not evidence that this backend honors that option. Record the actual persisted attempt limit and observed retry timestamps for the selected job type.

The outbox has its own eight-attempt policy and five-second schedule. Its nominal batch cap is 200, but the enabled RLS path limits the batch to the production pool size minus two: 15 minus two gives 13. That reserves database slots; it does not guarantee that 13 slow subscribers finish within the dispatch timeout. See [connection and arrival budgets](23-hypothetical-clinic-metrics.md#put-a-connection-budget-around-autoscaling).

```text
business transaction -> durable outbox/queue row -> claimed by current owner
                                                     |
                                                external effect
                                                     |
                                      +--------------+---------------+
                                      |                              |
                                      v                              v
                                  acknowledge                 process dies first
                                      |                              |
                                  completed              stale recovery / new claim
                                                                     |
                                                  reconcile or repeat safely by key

Graceful stop: stop new claims -> await active polls -> close persistence
Forced exit: bounded grace ends -> later recovery; remote effect may be uncertain
```

A claim token fences a stale worker's local acknowledgment. It cannot retract an email, payment-provider action or uploaded object that already happened. Define a stable logical-effect key and reconciliation behavior at that external boundary.

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

The outbox schema gives its optional idempotency key a unique constraint. The **15 October** append service uses `createMany` with `skipDuplicates: true` for keyed events; it no longer catches `P2002` inside the business transaction. A duplicate produces no new intent row without relying on recovery from an aborted PostgreSQL statement. This is producer-side deduplication, not effect-level idempotency. Verify the complete business transaction and actual database behavior for the chosen producer; the focused tests here did not exercise duplicate append against PostgreSQL.

## What the Current Relay Actually Acknowledges

The relay schedule is **every 5 seconds** in `CRON_SCHEDULES.OUTBOX_RELAY`. It selects up to **200** eligible rows, with a lower pool-aware batch size when RLS is enabled, increments attempts and dispatches each through the process-local EventEmitter2. It rejects a payload clinic that differs from the persisted clinic, restores tenant context and, when enabled, opens a fresh RLS-scoped transaction for clinic subscribers. It adds outbox, aggregate and clinic identifiers to the payload, awaits `emitAsync` with a **30-second dispatch timeout**, then records `processedAt` after fulfillment. These mechanisms still need real subscriber and database-role integration checks.

A local running flag avoids overlapping drains in one instance. A transaction-scoped PostgreSQL advisory lock coordinates instances that use the same lock convention. The helper holds that lock while awaiting its callback, but passes no transaction client to the callback; the relay uses the Prisma service. Do not assume the advisory lock proves all callback queries use the lock transaction or that external work becomes transactional.

### Acknowledgment Depends on the Listener Contract

The 2 October probe of **EventEmitter2 6.4.9** showed synchronous `emit` returning before an async listener completed. The rechecked relay now awaits `emitAsync`: promises returned by registered listeners must fulfill before the success path writes `processedAt`. An extracted-source check with the actual installed emitter confirmed both delayed fulfillment and rejection-driven retry.

Trace one event whose listener returns a promise for PDF creation:

| Outcome | Relay behavior | Remaining boundary |
| -------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------- |
| PDF promise fulfills before 30 seconds | Write `processedAt` | Fulfillment must represent the required effect, not detached work |
| Listener promise rejects | Leave the row unprocessed and schedule retry | Other listeners may already have succeeded and can run again |
| Dispatch reaches the timeout | Record failure and schedule retry | The original work keeps running unless separately cancelled |
| No listener is registered | The current `hasListeners` guard throws; retain retryable intent | One registered listener does not prove every required consumer is present |

Awaiting the emitter is an improvement, but the listener must return the promise for its required work and propagate its failure. [Nest's event listener options](https://docs.nestjs.com/techniques/events) default to `suppressErrors: true`: a listener error can be logged rather than rethrown. Required consumers therefore need an explicit error-propagation contract, verified through the actual Nest wiring. The extracted-source check did not exercise that wiring.

EventEmitter2 combines listener promises with `Promise.all`, which rejects on the first rejection; it does not cancel or wait for all remaining work on that failure path. The relay's timeout also rejects without cancelling the underlying promise. A slow first attempt can still complete after a retry starts, so consumers need effect-level idempotency. An in-process emitter reaches listeners in that process; it does not broadcast to every replica.

On a caught dispatch error, the relay records the error and schedules exponential retry with a **5-second base**, **5-minute cap** and **8-attempt ceiling**. The outer `Promise.allSettled` lets separate **row tasks** finish independently; it does not change a row's listener semantics. Exhausted retries, missing handlers, swallowed errors and replay still require operational recovery. A processed marker establishes only the completion promised by the listener contract, not automatically an external provider's durable receipt.

Manual queue dead-letter replay remains the recovery path in `DlqController` and `PostgresQueueService.replayDeadLettered`; the automatic replay policy helper is inert without worker wiring. Some appointment command events still have allowed direct emits. Do not generalize the outbox's durable intent to every application event or describe automatic dead-letter recovery as active.

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
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Atomic job claiming, token-fenced acknowledgments, delayed retries and an outbox provide useful building blocks. |
| Current limitations | Fixed stale recovery, producer transaction boundaries, direct-emission exceptions, consumer completeness/error propagation and non-cancelled effects leave failure gaps; automatic DLQ replay is not wired. |
| Recommended design | Verify producer transactions and current fencing with real database concurrency; consider bounded lease renewal where needed; make consumer effects idempotent under stable operation keys. |
| Evidence needed | Fault injection at claim/effect/ack boundaries preserves required work; duplicate delivery produces one business effect; competing database connections confirm an expired claimant cannot acknowledge a replacement claim. |

Token fencing above is implemented and covered by focused local unit tests. Further design changes remain proposals, and their production behavior is unverified. Apply them incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

PostgreSQL can atomically retain work intent and coordinate claims. Reliable execution additionally needs verified producer transactions, explicit ownership and recovery, effect-level idempotency and meaningful consumer acknowledgments. The inspected implementation has useful building blocks and limitations that must remain visible when describing its guarantees.

## See Also

- [Category revision](REVISION.md) — source-linked questions after the case studies.
- [Architecture decisions](01-architecture-decisions.md) — API and worker lifecycles.
- [Tenant isolation](02-multi-tenancy-rls.md) — scope and database enforcement.
- [Payment flows](04-payment-flows.md) — duplicate and ambiguous payment outcomes.
- [Case-study index](INDEX.md) — learning order.

## References

Source paths refer to the 2 October inspection, the 9 October relay recheck and the scoped 15 October refresh described above:

- `apps/api/src/shared/modules/queue/postgres-queue.service.ts`
- `apps/api/src/shared/modules/queue/infrastructure/prisma-queue-job.repository.ts`
- `apps/api/src/shared/modules/queue/queue-job-lifecycle.ts` — conditional acknowledgments and stale recovery.
- `apps/api/src/shared/modules/queue/postgres-queue.service.spec.ts` — focused local regression tests, including lost claims.
- `apps/api/src/shared/modules/queue/dlq-replay.scheduler.ts` — inert automatic replay policy.
- `apps/api/src/shared/modules/queue/pdf-job.service.ts`
- `apps/api/src/shared/modules/outbox/outbox.service.ts`
- `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts`
- `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.spec.ts` — asynchronous acknowledgment and retry tests.
- `apps/api/src/shared/common/utils/postgres-advisory-lock.ts`
- `apps/api/src/shared/schedule/cron-schedules.ts`
- `packages/db/prisma/schema.prisma` — `QueueJob` and `OutboxEvent` models.
- [NestJS events](https://docs.nestjs.com/techniques/events) — listener registration lifecycle and default error-suppression behavior.
