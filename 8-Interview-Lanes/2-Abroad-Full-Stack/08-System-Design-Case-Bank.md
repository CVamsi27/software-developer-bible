<!-- section: Abroad Full-Stack Lane | category: Reference | tags: system-design, cases, practice, eu -->
[![Section](https://img.shields.io/badge/section-Abroad%20Full-Stack%20Lane-blue)](.)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](.)
[![Tags](https://img.shields.io/badge/tags-system-design%20%C2%B7%20cases%20%C2%B7%20practice%20%C2%B7%20eu-lightgrey)](.)

# System Design Case Bank — 5 EU Cases to Practice

> **5 cases hand-picked for EU mid-stage interviews.** Each one has the framework, sample answer, and the 2-3 trade-offs the company will want to discuss. Practice each one with a 45-min timer + recording.

## TL;DR

- **5 cases:** workflow engine, payment gateway, multi-tenant SaaS, real-time booking, event-driven microservices
- **Each:** framework + sample answer + trade-off discussion + what gets you rejected
- **Practice order:** start with URL shortener (universal), then your target company's most-likely case
- **For 17 more cases (canonical set):** see [../../3-Architecture-Stack/11-System-Design/](../../3-Architecture-Stack/11-System-Design/)

The bible's [3-Architecture-Stack/](../../3-Architecture-Stack/) has the full case library. This file is the **5 must-practice for this lane** subset.

---

## The 4-Phase Framework (use every time)

Before diving into cases, internalize the framework:

1. **Clarify (5 min):** Ask 3-5 questions. Functional scope, scale, in/out, non-functional.
2. **Estimate (2 min):** QPS, storage, bandwidth (rough).
3. **High-level (10 min):** Boxes and arrows. Client → CDN → API → Service → DB.
4. **Deep-dive (20 min):** Pick 2-3 critical components. Schema, indexes, queue, cache, consistency.

Don't start drawing before Phase 1. Don't go wide before Phase 3. Don't skip trade-offs in Phase 4.

---

## Case 1: Workflow Engine (n8n, sennder, Hostaway, GoGlobal)

**The most common case at EU mid-stage.** Building a node-based workflow execution platform.

### Clarifying questions to ask

- What kind of triggers? HTTP only or also scheduled, webhook, email?
- What step types? HTTP request, transform, conditional, parallel?
- Retries on failure? DLQ?
- Concurrency limits? Can multiple executions of the same workflow run in parallel?
- How long should execution history be kept?
- Multi-tenancy? Each user/team has their own workflows?

### Estimates

- 100K executions/day at scale
- 1KB per execution record (state + metadata)
- 100MB/day storage
- Peak: 100 executions/sec, p99 500

### High-level design

```
[HTTP trigger] → [API gateway] → [Workflow Service] → [Queue (Kafka/SQS)]
                                                       ↓
                                              [Worker pool] → [Step executor]
                                                       ↓
                                              [State DB] (Postgres)
                                                       ↓
                                       [Webhook on completion]
```

**Critical components:**
1. **Queue** for executions (decouples trigger from execution, retries, scaling)
2. **Worker pool** that picks up executions and runs steps
3. **State DB** for execution history (Postgres with `executions` and `step_executions` tables)
4. **Webhook service** for completion notifications

### Deep-dive (pick 2-3)

**Database schema:**
```sql
CREATE TABLE workflows (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  name TEXT,
  trigger JSONB,         -- HTTP path, schedule, etc.
  steps JSONB,           -- array of step definitions
  created_at TIMESTAMPTZ
);

CREATE TABLE executions (
  id UUID PRIMARY KEY,
  workflow_id UUID REFERENCES workflows(id),
  tenant_id UUID NOT NULL,
  status TEXT,           -- queued / running / completed / failed / retry
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  trigger_payload JSONB,
  result JSONB
);

CREATE TABLE step_executions (
  id UUID PRIMARY KEY,
  execution_id UUID REFERENCES executions(id),
  step_index INT,
  step_type TEXT,
  status TEXT,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  input JSONB,
  output JSONB,
  error TEXT
);

CREATE INDEX idx_executions_workflow ON executions(workflow_id, started_at DESC);
CREATE INDEX idx_executions_tenant ON executions(tenant_id, started_at DESC);
CREATE INDEX idx_step_executions_execution ON step_executions(execution_id, step_index);
```

**Trade-offs to discuss:**
- **At-least-once vs exactly-once execution:** at-least-once is simpler but requires idempotency. Exactly-once is hard and usually means "effectively once" via dedup.
- **Synchronous vs async trigger:** sync gives immediate feedback but blocks on the first step. Async is more flexible but adds latency.
- **Persistent state vs in-memory:** persistent state survives worker crashes but adds DB load. In-memory is faster but loses state on crash.
- **Per-workflow vs global queue:** per-workflow guarantees ordering but limits throughput. Global queue scales better but loses ordering.
- **Concurrency limits:** limit parallel executions per workflow (fairness) vs unlimited (throughput).

### What gets you rejected

- "I'll just use a queue" without specifying Kafka, SQS, BullMQ, etc.
- No mention of state recovery on worker crash
- No idempotency strategy
- "How do you handle a step that takes 24 hours?" — long-running steps need special handling (checkpoints, resume)
- "What if the same workflow is triggered twice in 1 second?" — idempotency, rate limiting

---

## Case 2: Payment Gateway (SumUp, Scalable Capital, any fintech)

### Clarifying questions to ask

- Online + in-person? Multi-currency? Fraud detection? Idempotency?
- What PSP? Stripe, Adyen, internal? Or are we the PSP?
- Refunds, chargebacks, disputes? Full lifecycle or just authorize + capture?
- Webhook reliability?

### Estimates

- 1K TPS at scale
- 1KB per transaction record
- 30GB/year storage
- p99 latency target: 200ms (card-not-present), 2s (card-present)

### High-level design

```
[Client] → [API] → [Payment Service] → [PSP (Stripe/Adyen)]
                       ↓
                  [Ledger DB] (Postgres)
                       ↓
                  [Webhook handler] ← PSP webhook
                       ↓
                  [Reconciliation service] (daily batch)
```

### Deep-dive

**Idempotency:** every API request has an `Idempotency-Key` header. Server stores the key + result for 24h. Duplicate requests return the same result. This is the single most important thing in payments.

**Two-phase write (Saga):**
1. Hold funds (pre-auth) → write to ledger
2. Confirm with PSP → update ledger
3. If step 2 fails, refund step 1 (compensating action)

**Reconciliation:** daily batch compares internal ledger with PSP records. Discrepancies alert on-call.

**PCI compliance:** never store card numbers. Tokenize via PSP. Use their hosted fields or SDK.

**Fraud:** rule engine (velocity, amount, geo) in request path, ML model async.

### Trade-offs

- **Strong consistency vs eventual:** payments need strong consistency for the ledger. Use Postgres + transactions.
- **Synchronous PSP call vs async:** sync gives immediate feedback (good UX) but blocks the user. Async is faster but requires webhook handling.
- **Pre-auth vs post-auth flow:** pre-auth (hold funds) is safer for high-risk. Post-auth (charge immediately) is faster but harder to reverse.

### What gets you rejected

- No idempotency story
- "I'll use a queue" without saying how you handle webhook ordering
- No mention of reconciliation
- "What if the PSP is down for 4 hours?" — circuit breaker, retry, queue, eventually reconcile
- No PCI compliance mention

---

## Case 3: Multi-Tenant SaaS (Hostaway, Scalable, Docita-style)

### Clarifying questions

- How many tenants? 100? 100K? 1M?
- Data isolation: shared DB with tenant_id, schema-per-tenant, DB-per-tenant?
- Per-tenant customization (themes, workflows, custom fields)?
- Cross-tenant analytics?
- Tenant onboarding flow?

### Estimates

- 1K tenants, 100 users each, 10M records total
- 1KB per record, 10GB total
- p99 query latency: 100ms

### High-level

```
[Client] → [Auth] (extract tenant from JWT)
                ↓
            [API Gateway] (tenant context)
                ↓
            [Service] (all queries filter by tenant_id)
                ↓
            [Postgres with RLS]
                ↓
            [Analytics DB] (no tenant filter, separate)
```

### Deep-dive

**Row-level security (RLS):**
```sql
ALTER TABLE records ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON records
  USING (tenant_id = current_setting('app.tenant_id')::UUID);
```

Every query automatically filters by `tenant_id` from the session variable. Application sets it on connect.

**Tenant isolation trade-offs:**
- **Shared DB + tenant_id:** cheapest, but loud neighbor risk, hard to scale
- **Schema-per-tenant:** better isolation, more overhead, harder migrations
- **DB-per-tenant:** strongest isolation, most expensive, hardest ops

**RBAC:** roles per tenant, audit logging. Roles are tenant-scoped, not global.

**Migrations:** backwards-compatible. Never drop a column in the same release that adds the replacement. Use expand-contract pattern.

### Trade-offs

- **Customization via config vs code:** config is faster, code is more flexible. Use config for fields/themes, code for workflows.
- **Cross-tenant analytics:** separate analytics DB (ClickHouse, BigQuery) without tenant_id filter, fed via CDC from operational DB.
- **Per-tenant rate limiting:** Redis-based, key by tenant_id, returns 429 with retry-after.

### What gets you rejected

- "I'll add tenant_id to every query" without RLS or middleware
- No mention of loud neighbor
- "What if tenant A sees tenant B's data?" — silent failure is the worst
- No migration strategy
- "What if a tenant has 100x more data than average?" — partitioning by tenant_id

---

## Case 4: Real-Time Booking (Peter Park, Booking.com, GetYourGuide)

### Clarifying questions

- Single resource (one slot) or multi-resource (many slots)?
- Hold timeout (10 min during payment)?
- Payment integration?
- Cancellation flow?
- Multi-region, multi-currency?

### Estimates

- 10K searches/sec, 100 bookings/sec peak
- 1M bookings/day
- 1KB per booking, 1GB/day
- p99 search: 50ms, p99 booking: 500ms

### High-level

```
[Client] → [Search Service] (Elasticsearch) → [Results]
                ↓
[Client] → [Booking Service] (Postgres + row-level locks)
                ↓
            [Payment Service] (PSP)
                ↓
            [Confirmation]
                ↓
            [Webhook + Email]
```

### Deep-dive

**Concurrency: "two users grab the last seat"**

Option 1: **Pessimistic locking**
```sql
BEGIN;
SELECT * FROM slots WHERE id = ? FOR UPDATE;
-- check if available
UPDATE slots SET status = 'held' WHERE id = ? AND status = 'available';
COMMIT;
```

Option 2: **Optimistic locking with version**
```sql
UPDATE slots SET status = 'held', version = version + 1
WHERE id = ? AND version = ? AND status = 'available';
-- if 0 rows affected, retry
```

**Hold/release pattern:**
1. Booking creates a "hold" with 10-min TTL
2. Background job releases expired holds every minute
3. Payment confirms hold → status = "booked"
4. If payment fails, hold expires → released

**Idempotency:** booking ID is the idempotency key. Same booking ID won't double-book.

**Saga for hold → charge → confirm:**
- Hold slot (compensating: release)
- Charge payment (compensating: refund)
- Confirm booking (compensating: cancel + refund)
- Send confirmation (no compensation needed)

### Trade-offs

- **Pessimistic vs optimistic locking:** pessimistic is simpler but blocks. Optimistic is more scalable but requires retry.
- **Hold vs immediate charge:** hold is safer but more complex. Immediate charge is simpler but harder to undo.
- **Single-region vs multi-region:** single-region is simpler, multi-region needs geo-routing and conflict resolution.

### What gets you rejected

- No concurrency strategy
- "I'll use a transaction" without specifying the lock type
- "What if the user closes the browser during payment?" — hold + TTL
- "What if payment succeeds but confirmation fails?" — outbox pattern, retry

---

## Case 5: Event-Driven Microservices (sennder, THRYVE, any data platform)

### Clarifying questions

- What events? Throughput? Ordering requirements? Schema evolution?
- At-least-once vs exactly-once?
- How long to retain events?
- Cross-region?

### Estimates

- 10K events/sec, 1KB per event, 1TB/day
- 7-day retention typical
- 3-5 consumer services

### High-level

```
[Producer services]
    ↓
[Kafka topic per event type]
    ↓
[Consumer services] (multiple, partitioned by aggregate ID)
    ↓
[Storage / Downstream services]
```

### Deep-dive

**Topic design:** one topic per domain event type (`order.created`, `order.updated`, `order.cancelled`). Not one topic for "orders".

**Schema evolution:** Avro or Protobuf with schema registry (Confluent, Apicurio). Backwards-compatibility:
- Add optional field with default
- Never remove required field
- Never change field type

**Ordering:** partition by aggregate ID (e.g., `customer_id`). All events for one customer go to one partition, processed by one consumer, in order. Different customers can be in parallel.

**Idempotency:** consumer-side dedup by event ID. Store processed event IDs in Redis (TTL 7 days) or DB.

**DLQ (dead letter queue):** poison message handling. After 5 retries, send to DLQ for manual investigation.

**Replay:** keep topics for 7 days, support re-processing. Useful for bug fixes and new consumer onboarding.

### Trade-offs

- **Kafka vs RabbitMQ vs SQS:** Kafka for high throughput + replay, RabbitMQ for complex routing, SQS for managed simplicity.
- **At-least-once vs exactly-once:** at-least-once is the default. Exactly-once is hard and usually means "effectively once" via idempotency + dedup.
- **Push vs pull consumers:** push is lower latency, pull gives more control over throughput. Kafka uses pull.

### What gets you rejected

- "I'll use Kafka" without mentioning partitioning, retention, schema registry
- No idempotency strategy on the consumer side
- "What if the consumer crashes mid-processing?" — offset commit after processing, or use a transactional outbox
- No DLQ story
- "What if event ordering matters?" — partitioning by aggregate ID

---

## How to practice these 5 cases

1. **Pick case 1** (workflow engine, the most common). Set a 45-min timer.
2. **Record yourself** (Loom or Zoom). Practice out loud, not in your head.
3. **Use the 4-phase framework.** Ask 3-5 questions first, then estimate, then high-level, then deep-dive.
4. **Watch the recording.** Note where you got stuck, where you skipped trade-offs, where you missed failure modes.
5. **Repeat 3-4 times** until the case flows naturally. Then move to case 2.
6. **Total time:** 5 cases × 4 reps × 45 min = 15 hours. Spread over 2-3 weeks.

That's enough to be sharp on system design for this lane.

For 17 more cases (URL shortener, WhatsApp, Uber, Netflix, etc.), see [../../3-Architecture-Stack/11-System-Design/](../../3-Architecture-Stack/11-System-Design/).

---

## TL;DR

- **5 cases to practice:** workflow engine, payment gateway, multi-tenant SaaS, real-time booking, event-driven microservices
- **Each case:** framework + sample answer + trade-offs + what gets you rejected
- **Practice 4 reps per case with 45-min timer + recording.** 15 hours total.
- **For 17 more cases:** see [../../3-Architecture-Stack/11-System-Design/](../../3-Architecture-Stack/11-System-Design/)
