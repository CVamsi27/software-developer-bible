# 02 — Multi-Tenancy & Row-Level Security

> The hardest problem in Docita — provable data isolation between 25+ clinics handling Protected Health Information.

---

## Context

Docita serves 25+ clinics from a single PostgreSQL database. Each clinic's data must be completely invisible to other clinics. In healthcare, a data leak isn't just a bug — it's a compliance violation under DPDP (India's data protection law) and can result in fines, loss of license, and patient harm.

**The scale of the problem:**

- 149 Prisma models, most with a `clinicId` field
- 95 API routes, each needing tenant scoping
- Multiple developer workflows adding new queries daily
- Background workers running without HTTP request context

**The question:** How do you guarantee that Clinic A can never see Clinic B's data, even if a developer makes a mistake?

---

## Decision: 7-Layer Defense-in-Depth

### Layer 0: JWT Authentication

**What:** Every request carries a JWT token. The token contains `userId`, `clinicId`, `role`, and `subscription` claims.

**Why it's not enough:** JWTs prove *who you are*, not *what you can access*. A valid token for Clinic A's doctor doesn't prevent them from requesting Clinic B's patient data in the URL.

**Code:** `apps/api/src/shared/modules/auth/guards/jwt.strategy.ts`

### Layer 1: AsyncLocalStorage Tenant Context

**What:** Node.js `AsyncLocalStorage` carries the tenant context (clinicId, userId) through the entire request lifecycle — no parameter threading required.

```typescript
// apps/api/src/shared/common/middleware/tenant.middleware.ts
import { AsyncLocalStorage } from 'async_hooks';

interface TenantContext {
  clinicId?: string;
  userId?: string;
  bypassed?: boolean;
  preTenant?: boolean;  // authenticated but no clinic yet (onboarding)
}

export const tenantStorage = new AsyncLocalStorage<TenantContext>();

export function getCurrentTenant(): TenantContext | undefined {
  return tenantStorage.getStore();
}

export function getClinicIdOrFail(): string {
  const context = getCurrentTenant();
  if (!context?.clinicId) throw new Error('No tenant context available');
  return context.clinicId;
}
```

**Why AsyncLocalStorage:** The alternative is passing `clinicId` as a parameter to every function. At 28 domains × ~50 repository methods, that's 1,400 places where a missed parameter = data leak. ALS makes it implicit.

**The risk:** `setTimeout` loses ALS context. A detached promise running after the request finishes has no tenant context. We have a CI check (`check-detached-promises.mjs`) that flags any `setTimeout` or detached `Promise` in the codebase.

### Layer 2: RBAC Roles Matrix

**What:** Each role (DOCTOR, NURSE, ADMIN_DOCTOR, CLINIC_ADMIN, INTERNAL) has a fixed set of permissions. The `TenantGuard` + role guard verify the user has the right role for the endpoint.

**Why it's not enough:** RBAC can express "doctors can view patients" but not "doctors can view only *their* assigned patients." Adding more roles to handle this = role explosion.

### Layer 3: Subscription/Tier Guard

**What:** Feature gating based on clinic subscription tier. Free clinics can't access WhatsApp messaging. Starter clinics can't access insurance claims.

**Why it matters for tenancy:** A clinic on the Free tier trying to access Pro features gets a 403 before any data query runs. This reduces the attack surface.

### Layer 4: ABAC PolicyGuard

**What:** Object-level access control. The `PolicyGuard` is a global NestJS guard that evaluates typed policies for each request.

```typescript
// packages/authorization/src/policies/patient.policy.ts
export class PatientPolicy implements IPolicy {
  evaluate(subject: Subject, resource: Patient, action: Action): PolicyDecision {
    // Deny-overrides: any deny wins
    if (subject.clinicId !== resource.clinicId) return { effect: 'DENY', reason: 'cross-tenant' };
    if (subject.role === Role.DOCTOR && resource.assignedDoctorId !== subject.userId) {
      return { effect: 'DENY', reason: 'not-assigned' };
    }
    return { effect: 'ALLOW' };
  }
}
```

**Why ABAC on top of RBAC:** RBAC handles 90% of access control. ABAC handles the remaining 10% — "doctor can view only their assigned patients," "patient can view only their own data," "admin can view all patients in their clinic."

**Deny-overrides:** Any policy deny wins over any allow. Unmatched policies default to deny. This is the safest default — if a new policy is added but not wired up, access is denied rather than allowed.

### Layer 5: Repository Tenant Scoping

**What:** Prisma middleware automatically adds `clinicId` to every query. Even if a developer forgets the filter, the middleware enforces it.

**Why it's not enough:** Prisma middleware is application-level. A SQL injection or a direct `$queryRaw` call bypasses it.

### Layer 6: PostgreSQL Row-Level Security (RLS)

**What:** Database-level policies that filter rows based on the `app.current_clinic_id` session variable. Even if all application layers fail, the database itself enforces isolation.

```sql
-- Policy example (simplified)
CREATE POLICY clinic_isolation ON "Patient"
  USING ("clinicId" = current_setting('app.current_clinic_id')::text);
```

**Why RLS is the critical layer:** It's the last line of defense. If a developer writes `prisma.patient.findMany()` without any filter, RLS ensures only the current clinic's rows are returned.

**The hard part — connection pooling:**

Prisma uses a connection pool. Each query might run on a different connection. If you `SET LOCAL app.current_clinic_id` on connection A, but the query runs on connection B, RLS silently bypasses.

**Solution:** Route ALL queries through a single interactive transaction per request:

```typescript
// apps/api/src/shared/common/interceptors/tenant-context.interceptor.ts
intercept<TResponse>(context: ExecutionContext, next: CallHandler<TResponse>): Observable<TResponse> {
  const request = context.switchToHttp().getRequest();
  const user = request.user;

  if (user && (user.clinicId || user.role === Role.INTERNAL)) {
    const tenantContext = { clinicId: user.clinicId, userId: user.id, bypassed: user.role === Role.INTERNAL };

    if (this.config.isRlsEnabled() && tenantContext.clinicId && !tenantContext.bypassed) {
      // Open a single interactive transaction, set the GUC, run the handler inside it
      return from(
        this.prisma.$transaction(async (tx) => {
          await applyRlsScope(tx, tenantContext.clinicId);
          return runWithActiveTx(tx, () => tenantStorage.run(tenantContext, () => lastValueFrom(next.handle())));
        }, getRlsRequestTransactionOptions()),
      );
    }

    return from(tenantStorage.run(tenantContext, () => lastValueFrom(next.handle())));
  }

  return next.handle();
}
```

**The `runUnrestricted` escape hatch:** Background workers (queue processing, cron jobs) run without a request context. They need to access all clinics' data. The `PrismaService.runUnrestricted()` method bypasses RLS for these cases:

```typescript
// apps/api/src/shared/modules/queue/postgres-queue.service.ts
// RLS-BYPASS: background queue workers run without per-request clinic session
const row = await this.prisma.runUnrestricted(async () =>
  this.prisma.queueJob.create({ data: { name, data, status: 'WAITING', ... } })
);
```

**Why `set_config` instead of `SET LOCAL`:** The function-call form binds the value as a parameter, preventing SQL injection. The regex check (`/^[A-Za-z0-9_-]+$/`) is a second wall.

### Layer 7: Audit Logging

**What:** Every PHI access is logged with user, clinic, action, and timestamp. This provides an audit trail for compliance.

**Why it matters:** Even if all other layers work, you need to *prove* they worked. Audit logs answer: "Who accessed this patient's data, and when?"

---

## Alternatives Considered

| Option | Pros | Cons                                                                                                                        |
|--------|------|------                                                                                                                       |
| **Separate database per clinic** | Maximum isolation | Operational overhead at 25+ clinics, can't do cross-clinic analytics                 |
| **Schema-per-tenant** | Good isolation, shared DB | Migration complexity, schema proliferation                                              |
| **Shared schema + application filtering** | Simple | One missed filter = data leak                                                          |
| **Shared schema + RLS (chosen)** | Database-level guarantee, transparent to app | Connection pool complexity, Prisma integration challenges |
| **Citus (distributed PostgreSQL)** | Horizontal scaling | Overkill at 25 clinics, adds operational complexity                               |

### Why Shared Schema + RLS

**The math:** At 25 clinics, separate databases means 25 connection pools, 25 migration runs, 25 backup schedules. Schema-per-tenant means 25 schemas with shared connections — still complex. Shared schema with RLS is one database, one pool, one migration — and the database itself enforces isolation.

**The risk we accepted:** RLS adds ~5-10% query overhead (the policy evaluation). At our scale, this is negligible. If we hit 200+ clinics, we might reconsider Citus.

---

## What Worked

- **Zero data leaks in production** — 7 layers caught every attempt
- **Developer experience** — ALS means developers don't think about tenancy; it's automatic
- **CI enforcement** — boundary violations caught at build time, not in production

## What Failed

- **RLS silent bypass** — during rollout, connection pool routing caused `SET LOCAL` to apply on a different connection than the query. Fixed by routing all queries through a single interactive transaction.

- **Encrypt/decrypt drift** — a new PHI field was added to encrypt but not decrypt. Fixed by CI check (`check:phi-encryption-coverage`).

- **Worker RLS bypass** — background workers initially tried to use the tenant context. They can't — they run without a request. Had to add `runUnrestricted()` escape hatch with careful documentation.

## What Could Be Better

- **RLS policy testing** — we don't have automated tests that verify RLS policies actually block cross-tenant access. We rely on manual testing and the 7-layer defense. Adding `pgTAP` tests would strengthen this.

- **Dynamic policy generation** — currently each table needs a manually written RLS policy. A Prisma extension that auto-generates policies from the schema would reduce human error.

- **Audit log retention** — we log all PHI access but don't have a retention policy. DPDP requires specific retention periods. This needs to be implemented.

---

## Code Evidence

| Claim | File                                                                                         |
|-------|------                                                                                        |
| Tenant middleware (ALS) | `apps/api/src/shared/common/middleware/tenant.middleware.ts`               |
| Tenant context interceptor | `apps/api/src/shared/common/interceptors/tenant-context.interceptor.ts` |
| RLS scope application | `apps/api/src/shared/modules/rls/apply-rls-scope.ts`                         |
| Active TX storage | `apps/api/src/shared/modules/rls/active-tx.storage.ts`                           |
| RLS routing extension | `packages/db/prisma/extensions/rls-routing.ts`                               |
| Tenant guard | `apps/api/src/shared/modules/auth/guards/tenant.guard.ts`                             |
| Emergency access | `apps/api/src/shared/common/interceptors/emergency-access.interceptor.ts`         |
| RLS rollout docs | `docs/compliance/RLS_ROLLOUT.md`                                                  |
| CI boundary check | `scripts/checks/check-prisma-boundary.mjs`                                       |

---

## Interview Script (60 seconds)

> "Multi-tenant data isolation in healthcare required 7 defense layers. The foundation is AsyncLocalStorage carrying the tenant context through every request — no parameter threading. On top of that: RBAC for role-based access, ABAC policies for object-level conditions like 'doctor sees only assigned patients,' Prisma middleware for application-level filtering, and PostgreSQL RLS as the database-level guarantee. The hardest part was RLS — Prisma's connection pool routes queries to different connections, so `SET LOCAL` session variables were silently bypassed. We solved it by routing all queries through a single interactive transaction per request. Background workers use a `runUnrestricted()` escape hatch with careful documentation."
