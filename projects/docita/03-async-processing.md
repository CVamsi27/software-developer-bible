# 03 — Async Processing

> PostgreSQL queue + transactional outbox — how we process jobs without Redis, Kafka, or any extra infrastructure.

---

## Context

Docita needs to process background jobs:

- **PDF generation** — prescriptions, invoices, OPD slips (2-3 seconds each)
- **WhatsApp messages** — appointment reminders, payment confirmations
- **Email notifications** — welcome emails, password resets
- **Analytics** — usage aggregation, overage calculation
- **Webhooks** — outgoing integrations with lab systems
- **Reconciliation** — WhatsApp message delivery status sync

**The constraint:** We're a small team (founding engineer + AI). Adding Redis, Kafka, or SQS means another managed service, another failure mode, another secret to rotate, another dashboard to monitor. At ~0.4 jobs/sec sustained, we need something simpler.

---

## Decision 1: PostgreSQL as Queue

### What We Chose

A `QueueJob` table in PostgreSQL. Jobs are enqueued in the same transaction as business writes. A worker process polls and executes.

```text
┌───────────────────────────────────────────────────────────────┐
│ Business Write + Job Enqueue (same transaction)              │ 
│                                                              │ 
│  prisma.$transaction(async (tx) => {                         │ 
│    await tx.appointment.create({ data: {...} });             │ 
│    await tx.queueJob.create({                                │ 
│      data: {                                                 │ 
│        name: 'prescription.pdf.generate',                    │ 
│        data: { prescriptionId: '...', clinicId: '...' },     │ 
│        status: 'WAITING',                                    │ 
│      },                                                      │ 
│    });                                                       │ 
│  });                                                         │ 
│  // Both succeed or both fail — atomic                        │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ Worker Process (separate NestJS process)                     │ 
│                                                              │ 
│  Polls every 2 seconds:                                      │ 
│  SELECT ... FROM "QueueJob"                                  │ 
│  WHERE status = 'WAITING' AND name = $1                     │ 
│  ORDER BY priority DESC, createdAt ASC                       │ 
│  FOR UPDATE SKIP LOCKED                                      │ 
│  LIMIT 1                                                     │ 
│                                                              │ 
│  → Execute handler                                           │ 
│  → Mark COMPLETED or DELAYED (retry) or DEAD_LETTERED       │ 
└───────────────────────────────────────────────────────────────┘
```

### Why Postgres (Not Redis)

| Factor | PostgreSQL | Redis + BullMQ |
|--------|-----------|----------------|
| **Already paying for** | Yes (AWS RDS HA) | No — extra $50-200/mo |
| **Transactional enqueue** | Yes — same `prisma.$transaction` | No — separate connection, dual-write risk |
| **Operational overhead** | Zero — same database | Another service to monitor, rotate secrets |
| **Durability** | WAL-backed, crash-safe | AOF/RDB — configurable, but separate |
| **Throughput ceiling** | ~1k jobs/sec | ~10k jobs/sec |
| **Our actual load** | ~0.4 jobs/sec | Overkill |

**The real reason:** Transactional enqueue. When a prescription is created, the PDF job must be enqueued in the *same transaction*. With Redis, you'd need: (1) write to Postgres, (2) write to Redis. If step 2 fails, the prescription exists but no PDF is generated. With Postgres, both writes are atomic.

### The Queue Service

```typescript
// apps/api/src/shared/modules/queue/postgres-queue.service.ts
@Injectable()
export class PostgresQueueService implements IQueueProvider, OnModuleDestroy {
  private readonly handlers = new Map<string, QueueJobHandler>();
  private readonly pollers = new Map<string, ReturnType<typeof setInterval>>();
  private readonly activePolls = new Set<string>();

  async enqueue<T>(name: string, data: T, options?: QueueJobOptions): Promise<QueueJob<T>> {
    // Idempotency: skip if recent completed job with same key exists
    if (options?.idempotencyKey) {
      const recent = await this.findRecentCompletedByIdempotency(name, options.idempotencyKey);
      if (recent) return this.rowToJob(recent);
    }
    // RLS-BYPASS: workers run without per-request clinic session
    const row = await this.prisma.runUnrestricted(async () =>
      this.prisma.queueJob.create({ data: { name, data, status: 'WAITING', ... } })
    );
    return this.rowToJob(row);
  }

  async process<T>(name: string, handler: QueueJobHandler<T>): Promise<void> {
    this.handlers.set(name, bindQueueJobHandler(handler));
    if (!this.pollers.has(name)) {
      const interval = setInterval(() => this.pollIfIdle(name), POLL_INTERVAL_MS);
      interval.unref?.();  // Don't keep process alive for pollers
      this.pollers.set(name, interval);
    }
  }
}
```

### Key Design Decisions

**`FOR UPDATE SKIP LOCKED`:** Multiple worker replicas can poll simultaneously. `SKIP LOCKED` ensures each job is claimed by exactly one worker. No double-processing.

**Idempotency key:** External webhooks (Razorpay) can send the same event multiple times. The queue checks for recent completed jobs with the same key before enqueueing.

**`interval.unref()`:** Pollers don't keep the Node.js process alive. If all handlers are registered and the process needs to shut down, it can.

**`runUnrestricted()`:** Queue workers run without a request context — they need to access all clinics' data. This bypasses RLS with careful documentation.

### Retry with Exponential Backoff

```typescript
const computeBackoffMs = (attempt: number): number => {
  const exponential = RETRY_BASE_MS * Math.pow(2, attempt - 1);  // 1s, 2s, 4s, 8s, 16s
  return Math.min(exponential, RETRY_MAX_MS);  // Cap at 60s
};

// On failure:
if (nextAttemptsMade < row.maxAttempts) {
  await this.prisma.queueJob.update({
    where: { id: row.id },
    data: {
      status: 'DELAYED',
      attemptsMade: nextAttemptsMade,
      failedReason,
      delayedUntil: new Date(Date.now() + backoffMs),
    },
  });
} else {
  await this.prisma.queueJob.update({
    where: { id: row.id },
    data: {
      status: 'DEAD_LETTERED',
      attemptsMade: nextAttemptsMade,
      failedReason,
      deadLetteredAt: this.clock.now(),
    },
  });
}
```

**Default max attempts:** 5. After 5 failures, the job moves to dead-letter status for manual inspection.

**Stale job recovery:** If a worker crashes mid-job, the job stays in `ACTIVE` status forever. A recovery mechanism detects jobs stuck in `ACTIVE` for >10 minutes and moves them back to `DELAYED` or `FAILED`.

---

## Decision 2: Transactional Outbox

### What We Chose

Domain events are written to an `OutboxEvent` table in the same transaction as the business write. A relay scheduler polls and republishes to in-process EventEmitter2.

```text
┌───────────────────────────────────────────────────────────────┐
│ Business Write + Event Emission (same transaction)           │ 
│                                                              │ 
│  prisma.$transaction(async (tx) => {                         │ 
│    await tx.appointment.create({ data: {...} });             │ 
│    await outbox.append(tx, {                                 │ 
│      eventName: 'appointment.created',                       │ 
│      clinicId: appointment.clinicId,                         │ 
│      payload: { appointmentId, patientId, doctorId },        │ 
│      idempotencyKey: `apt-created-${appointment.id}`,       │  
│    });                                                       │ 
│  });                                                         │ 
│  // Both succeed or both fail — atomic                        │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ Outbox Relay Scheduler (cron, every 2 seconds)               │ 
│                                                              │ 
│  WITH claimed AS (                                           │ 
│    SELECT id FROM "OutboxEvent"                              │ 
│    WHERE "processedAt" IS NULL AND "attempts" < 8            │ 
│    ORDER BY "createdAt" ASC                                  │ 
│    FOR UPDATE SKIP LOCKED LIMIT 200                          │ 
│  )                                                           │ 
│  UPDATE "OutboxEvent" SET "attempts" = "attempts" + 1       │ 
│  FROM claimed WHERE o.id = claimed.id                        │ 
│  RETURNING ...                                               │ 
│                                                              │ 
│  → EventEmitter2.emit(eventName, payload)                    │ 
│  → Mark processedAt                                          │ 
└───────────────────────────────────────────────────────────────┘
```

### Why Outbox (Not Direct EventEmitter2)

**The problem with direct emission:**

```typescript
// BEFORE (broken)
async createAppointment(command) {
  const appointment = await this.repository.save(new Appointment(command));
  this.eventEmitter.emit('appointment.created', appointment);  // ← What if this fails?
  return appointment;
}
```

If the `emit` fails (or the process crashes after commit), the appointment exists but no reminder is sent, no WhatsApp notification goes out, no analytics event is recorded. The outbox solves this:

```typescript
// AFTER (reliable)
async createAppointment(command) {
  return this.prisma.$transaction(async (tx) => {
    const appointment = await this.repository.save(new Appointment(command), tx);
    await this.outbox.append(tx, {
      eventName: 'appointment.created',
      clinicId: appointment.clinicId,
      payload: appointment,
      idempotencyKey: `apt-created-${appointment.id}`,
    });
    return appointment;
  });
  // If commit succeeds, the event WILL be delivered (eventually)
}
```

### Why Not Kafka/NATS

| Factor | Outbox (chosen) | Kafka | NATS |
|--------|----------------|-------|------|
| **Infrastructure** | Zero — same Postgres | Extra cluster | Extra server |
| **Operational cost** | $0 | $100+/mo | $50+/mo |
| **Latency** | ~2 seconds (poll interval) | ~10ms | ~1ms |
| **Throughput** | ~100 events/sec | ~100k events/sec | ~1M events/sec |
| **Our actual load** | ~0.4 events/sec | Overkill | Overkill |

**The trade-off we accepted:** 2-second relay lag. For appointment reminders, prescription PDFs, and analytics — this is fine. For real-time payment notifications, we use WebSocket directly (not through the outbox).

### Outbox Relay Details

```typescript
// apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts
@Cron(CRON_SCHEDULES.OUTBOX_RELAY)
@TrackHeartbeat('outbox.relay')
async drain(): Promise<void> {
  if (this.running) return;  // Prevent concurrent drains
  this.running = true;

  try {
    const acquired = await withAdvisoryLock(this.prisma, 'outbox-relay-drain', async () => {
      // Advisory lock prevents multiple replicas from draining simultaneously
      const rows = await this.prisma.$queryRaw`
        WITH claimed AS (
          SELECT id FROM "OutboxEvent"
          WHERE "processedAt" IS NULL AND "attempts" < ${MAX_ATTEMPTS}
            AND ("nextAttemptAt" IS NULL OR "nextAttemptAt" <= ${now})
          ORDER BY "createdAt" ASC
          FOR UPDATE SKIP LOCKED LIMIT ${BATCH_SIZE}
        )
        UPDATE "OutboxEvent" o
        SET "attempts" = o."attempts" + 1, "lastAttemptAt" = ${now}
        FROM claimed WHERE o.id = claimed.id
        RETURNING o.id, o."eventName", o."payload", o."aggregateId", o."clinicId"
      `;

      await Promise.allSettled(rows.map(async (row) => {
        try {
          this.events.emit(row.event_name, { ...toPayloadRecord(row.payload), __outboxId: row.id });
          await this.prisma.outboxEvent.update({
            where: { id: row.id },
            data: { processedAt: new Date(), nextAttemptAt: null, lastError: null },
          });
        } catch (error) {
          // Exponential backoff for retries
          const delay = Math.min(BACKOFF_CAP_MS, BACKOFF_BASE_MS * Math.pow(2, attempts - 1));
          await this.prisma.outboxEvent.update({
            where: { id: row.id },
            data: { lastError: message.slice(0, 1000), nextAttemptAt: new Date(Date.now() + delay) },
          });
        }
      }));
    });

    if (acquired === null) {
      this.logger.warn('[outbox-relay] skipping tick — another replica holds the advisory lock');
    }
  } finally {
    this.running = false;
  }
}
```

**Key details:**

- **Advisory lock:** Prevents multiple API replicas from draining the same events
- **`FOR UPDATE SKIP LOCKED`:** Concurrent-safe batch processing
- **`Promise.allSettled`:** One failed event doesn't block others
- **Exponential backoff:** Failed events retry with increasing delays (5s → 10s → 20s → ... → 5min cap)
- **Max 8 attempts:** After 8 failures, the event stays in the table for DLQ alerting

### Outbox Schema

```typescript
// apps/api/src/shared/modules/outbox/outbox.interface.ts
export interface OutboxAppend {
  eventName: string;           // e.g., "appointment.created"
  clinicId: string | null;     // Tenant context for relay
  aggregateType?: string;      // e.g., "Appointment"
  aggregateId?: string;        // e.g., appointment.id
  payload: Prisma.JsonValue;   // Must NOT contain PHI in plaintext
  idempotencyKey?: string;     // For duplicate-emit detection
}
```

**PHI rule:** Outbox payloads must not contain PHI in plaintext. Only IDs and metadata. Consumers fetch full data from the database (through RLS).

---

## What Worked

- **Zero lost events** — outbox ensures every domain event is delivered (eventually)
- **Zero infrastructure cost** — no Redis, no Kafka, no extra services
- **Idempotent consumers** — duplicate deliveries are harmlessly ignored
- **Dead letter queue** — failed jobs are inspectable and replayable

## What Failed

- **Cross-pod event loss (before outbox)** — in-process EventEmitter2 dropped events when considering multi-pod deployment. Fixed by outbox.

- **Poll interval too long** — initially 5-second poll interval. WhatsApp responses felt laggy. Reduced to 2 seconds.

- **Stale job recovery** — a worker crash left jobs in `ACTIVE` status forever. Fixed with 10-minute timeout + recovery mechanism.

## What Could Be Better

- **CDC (Change Data Capture)** — instead of polling, use PostgreSQL logical replication to stream outbox events. Lower latency, less DB load. Debezium would work but adds operational complexity.

- **Event schema versioning** — outbox events don't have version numbers. A breaking change in event payload requires coordinated consumer updates. Adding a `schemaVersion` field would help.

- **Consumer monitoring** — we don't have a dashboard showing outbox event delivery rates, lag, or dead-letter counts. Adding Prometheus metrics would improve observability.

---

## Code Evidence

| Claim | File |
|-------|------|
| Postgres queue service | `apps/api/src/shared/modules/queue/postgres-queue.service.ts` |
| Queue job repository | `apps/api/src/shared/modules/queue/infrastructure/prisma-queue-job.repository.ts` |
| Queue interface | `apps/api/src/shared/modules/queue/queue.interface.ts` |
| Outbox service | `apps/api/src/shared/modules/outbox/outbox.service.ts` |
| Outbox relay | `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts` |
| Outbox interface | `apps/api/src/shared/modules/outbox/outbox.interface.ts` |
| Worker module | `apps/api/src/worker.module.ts` |
| PDF job service | `apps/api/src/shared/modules/queue/pdf-job.service.ts` |
| Worker metrics | `apps/api/src/shared/modules/queue/worker-metrics.service.ts` |

---

## Interview Script (60 seconds)

> "I built a PostgreSQL-backed job queue using `SELECT ... FOR UPDATE SKIP LOCKED`. The key advantage over Redis: transactional enqueue. A `prisma.$transaction` covers both the business write AND the job emission — no dual-write problem. For domain events, I implemented the transactional outbox pattern. Events are written to an `OutboxEvent` table in the same transaction as the business write. A relay scheduler polls every 2 seconds, republishes to in-process EventEmitter2, and marks events as processed. Failed events retry with exponential backoff up to 8 attempts, then go to a dead-letter queue. The trade-off is 2-second relay lag — acceptable for our scale of ~0.4 jobs/sec. We chose this over Kafka/NATS because we're single-region single-pod and don't need the infrastructure overhead."
