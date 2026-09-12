# 11 — What I'd Do Differently

> Honest retrospective — what's not perfect, what's tech debt, and what I'd change with hindsight.

---

## Context

Docita was built by a founding engineer (solo + AI-assisted) under startup pressure. Many decisions were "good enough for now" — not "best practice forever." This file documents what I'd change with hindsight, what's tech debt, and what I'd prioritize next.

---

## 1. Event-Driven Cross-Domain Communication

### Current State

Cross-domain queries use port interfaces:

```typescript
// Billing needs patient data → uses PatientPersistencePort
@Inject(PATIENT_PERSISTENCE_PORT)
private readonly patientPort: PatientPersistencePort;
```

### What I'd Do Differently

Use domain events for cross-domain communication:

```typescript
// Instead of billing querying patient directly
// Patient domain emits: patient.created, patient.updated
// Billing subscribes and maintains a local read model
```

**Why:** Ports create implicit coupling — billing "knows" about patient's internal structure. Events decouple domains completely. The trade-off is eventual consistency, but for billing (not real-time), this is fine.

**Priority:** Medium. Current approach works but doesn't scale to 50+ domains.

---

## 2. Event Schema Versioning

### Current State

Outbox events don't have version numbers:

```typescript
await this.outbox.append(tx, {
  eventName: 'appointment.created',
  payload: appointment,  // No version field
});
```

### What I'd Do Differently

Add a `schemaVersion` field to every event:

```typescript
await this.outbox.append(tx, {
  eventName: 'appointment.created',
  schemaVersion: 2,
  payload: appointment,
});
```

**Why:** A breaking change in event payload requires coordinated consumer updates. Without versioning, consumers can't handle old and new formats simultaneously. During migration, old events in the outbox would break new consumers.

**Priority:** High. This is a ticking time bomb.

---

## 3. Automated RLS Policy Testing

### Current State

RLS policies are tested manually. We rely on the 7-layer defense and CI boundary checks.

### What I'd Do Differently

Add `pgTAP` tests that verify RLS policies:

```sql
-- Test: Clinic A cannot see Clinic B's patients
SELECT set_config('app.current_clinic_id', 'clinic-a', true);
SELECT * FROM "Patient" WHERE "clinicId" = 'clinic-b';
-- Should return 0 rows
```

**Why:** Manual testing is incomplete. A `pgTAP` test suite would catch policy regressions automatically.

**Priority:** High. RLS is the last line of defense — it must be tested.

---

## 4. Build Caching with Turborepo

### Current State

Full rebuild takes ~3 minutes. No incremental builds.

### What I'd Do Differently

Add Turborepo for build caching and parallelization:

```json
// turbo.json
{
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "test": { "dependsOn": ["build"] }
  }
}
```

**Why:** Turborepo caches build outputs. If `packages/types` hasn't changed, apps that depend on it skip the rebuild. Estimated build time reduction: 3 minutes → ~30 seconds.

**Priority:** Medium. Developer experience improvement, not a product feature.

---

## 5. Payment Provider Abstraction

### Current State

Tightly coupled to Razorpay:

```typescript
// Direct Razorpay adapter usage
@Inject(RAZORPAY_CLIENT)
private readonly razorpay: RazorpayClient;
```

### What I'd Do Differently

Abstract behind a `PaymentProvider` interface:

```typescript
interface PaymentProvider {
  createOrder(amount, currency): Promise<Order>;
  capturePayment(orderId): Promise<Payment>;
  createRefund(paymentId, amount): Promise<Refund>;
}
```

**Why:** If Razorpay raises fees or has an outage, switching providers requires rewriting every payment call. An abstraction allows swapping providers with minimal code changes.

**Priority:** Low. Razorpay is dominant in India. Switching is unlikely in the near term.

---

## 6. Structured Logging with Correlation IDs

### Current State

Logging uses `nestjs-pino` but without consistent correlation IDs:

```typescript
this.logger.log({ action: 'appointment.create', clinicId, patientId });
```

### What I'd Do Differently

Add correlation IDs to every log entry:

```typescript
this.logger.log({ 
  action: 'appointment.create', 
  clinicId, patientId,
  correlationId: getCurrentCorrelationId(),  // From request context
  traceId: getCurrentTraceId(),              // For distributed tracing
});
```

**Why:** When debugging a production issue, you need to trace a request across API → queue → worker → external API. Correlation IDs make this possible.

**Priority:** Medium. Current logging works for single-service debugging but fails for cross-service issues.

---

## 7. Frontend Form Generation from Zod Schemas

### Current State

Zod schemas define validation, but form fields are manually written in React:

```tsx
// Manual form field
<Input label="First Name" {...register('firstName', { required: true })} />
```

### What I'd Do Differently

Generate form fields from Zod schemas:

```typescript
// Given a Zod schema, auto-generate form fields
const formConfig = zodToForm(createPatientSchema);
// → [{ name: 'firstName', label: 'First Name', type: 'text', required: true }, ...]
```

**Why:** Currently, adding a field requires updating 3 places: Zod schema, TypeScript type, and React form. Auto-generation reduces this to 1 place.

**Priority:** Low. Works but verbose.

---

## 8. Database Connection Pool Tuning

### Current State

Prisma uses default connection pool settings.

### What I'd Do Differently

Tune the pool based on actual usage:

```typescript
// packages/db/prisma/index.ts
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: DATABASE_URL,
      // Tune based on RDS instance type
    },
  },
  // connection_limit: calculated based on RDS max_connections / number of pods
});
```

**Why:** Default pool size might be too small (causing connection starvation) or too large (overwhelming RDS). Tuning based on actual usage improves reliability.

**Priority:** Medium. Currently works but might fail under load.

---

## 9. Health Check Endpoints

### Current State

Basic health check that returns 200.

### What I'd Do Differently

Comprehensive health checks:

```typescript
// Check: database connectivity
// Check: outbox relay lag
// Check: queue job count
// Check: external API connectivity (Razorpay, WhatsApp)
// Check: memory usage
// Check: event loop lag
```

**Why:** A 200 response doesn't mean the service is healthy. The database might be down, the outbox might be 10 minutes behind, or memory might be exhausted.

**Priority:** High. Currently, we discover issues from user reports, not monitoring.

---

## 10. Comprehensive Integration Test Suite for Multi-Tenancy

### Current State

Multi-tenant isolation is tested manually and via CI boundary checks.

### What I'd Do Differently

Automated test suite that verifies isolation for every model:

```typescript
// For each Prisma model with clinicId:
it('Clinic A cannot access Clinic B data via direct query', async () => {
  const clinicAData = await createTestData('clinic-a');
  const result = await prisma.$queryRaw`SELECT * FROM "Patient" WHERE "clinicId" = 'clinic-b'`;
  expect(result).toHaveLength(0);
});
```

**Why:** Manual testing catches known scenarios. Automated testing catches regressions from new code.

**Priority:** High. This is the most critical test suite for a multi-tenant healthcare platform.

---

## Priority Matrix

| Improvement | Priority | Effort | Impact |
| ------------------------------- | ---------- | -------- | ------------------------- |
| Event schema versioning | High | Low | Prevents migration bugs |
| RLS policy testing (pgTAP) | High | Medium | Prevents data leaks |
| Health check endpoints | High | Low | Faster incident detection |
| Multi-tenancy integration tests | High | High | Prevents regressions |
| Event-driven cross-domain | Medium | High | Better decoupling |
| Build caching (Turborepo) | Medium | Low | Developer experience |
| Correlation IDs | Medium | Medium | Better debugging |
| DB connection pool tuning | Medium | Low | Reliability |
| Payment provider abstraction | Low | Medium | Future-proofing |
| Frontend form generation | Low | Medium | Less boilerplate |

---

## What I'm Proud Of

Despite the tech debt, certain decisions aged well:

1. **DDD architecture** — 29 domains without coupling. This would be chaos without clear boundaries.
2. **Zod-first types** — zero type drift. Every other approach would have accumulated drift.
3. **Postgres-as-queue** — zero infrastructure cost, transactional enqueue. Still the right call at our scale.
4. **7-layer defense** — zero data leaks in production. The depth was worth the complexity.
5. **Transactional outbox** — zero lost events. The 2-second lag is a fair trade-off.

---

## What I'd Tell My Future Self

> "Ship the MVP fast. Add the schema versioning, RLS tests, and health checks before you hit 50 clinics. The payment abstraction can wait. The event-driven architecture can wait. The Turborepo migration can wait. But the schema versioning is a ticking time bomb — fix it before you have outbox events in production that can't be migrated."
---

[← Previous: Long Tail Domains](21-long-tail-domains.md) · [ Back to Index](INDEX.md) · [Next: Docita Resume Defense →](../../80-lanes-abroad-full-stack/80.16-docita-resume-defense.md)
