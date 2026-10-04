# 02 — Tenant Isolation: Carry Identity to the Database Operation

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



A request for a patient record must establish both the caller’s identity and permission to access that record. A valid login for one clinic cannot authorize another clinic’s data.

This case study describes source inspected on 2 October 2026. Repository configuration and tests are evidence of implementation; they do not prove the deployed connection role, current production traffic, or absence of incidents.

## Definition

A tenant is a customer organization, such as a clinic, that shares the application with others. Tenant isolation prevents one tenant’s operation from reading or changing another tenant’s protected state. Authentication establishes identity; application authorization decides whether that identity may perform the operation. Row-level security (RLS) lets database policies restrict which rows the executing database role may access, using context supplied for its session or transaction.

## First Principles

An identifier supplied in a URL is untrusted. A pooled connection is not permanently associated with one request. Async context carries values but does not establish their authority. Therefore identity, access decisions and database scope must stay connected to the operation at every boundary.

## Trace a clinic request through the implementation

```text
verified identity → tenant/role/policy checks → clinic context
→ scoped database transaction → row policy → result
```

| Component | Its role in the whole | What it cannot establish alone |
| ----------------------- | -------------------------------------------------------------- | ------------------------------------------------------------- |
| JWT authentication | Verify the token and obtain caller claims | Object access or current clinic membership |
| Tenant and role guards | Reject requests outside the permitted tenant or role | Every resource-specific condition |
| ABAC policies | Evaluate ownership, assignment and other resource attributes | Database connection scope |
| AsyncLocalStorage | Carry request-local identity and active transaction references | Permission, trusted identity or a durable job context |
| Prisma tenant extension | Apply application-level tenant discipline | Every raw query or privileged path |
| PostgreSQL RLS | Apply row policies for the executing role and context | Correct application role, enabled scope or safe bypass policy |
| Audit pipeline | Record attributable access and changes | Proof that every possible leak was prevented |

Subscription gating controls feature entitlement. It can coexist with authorization, but a paid plan does not grant access to another clinic’s data.

## AsyncLocalStorage carries context; it does not validate it

The current `tenant.middleware.ts` stores clinic identity, user identity, a bypass flag and a pre-tenant flag. `getClinicIdOrFail()` rejects a missing clinic identity.

Timers and promises created within an async scope can inherit that scope. They do not universally lose it when the HTTP request finishes. The more dangerous distinction is lifetime: a delayed operation can retain a reference to a transaction that has already ended. Independently scheduled workers need a separately validated job context; they cannot rely on a request store being present.

Make the source of each context value explicit. A clinic ID obtained from verified identity and checked membership is different from a client-supplied clinic ID. A bypass flag is a privileged decision, not a convenience default.

## Keep the database setting and query on the same transaction

The inspected interceptor opens an interactive transaction when RLS is enabled for an authenticated clinic request. `applyRlsScope()` applies transaction-local settings through parameterized calls:

```typescript
// Source excerpt: apply-rls-scope.ts; tx is a Prisma transaction client.
await tx.$executeRaw`SELECT set_config('app.rls_enabled', 'on', true)`;
await tx.$executeRaw`SELECT set_config('app.current_clinic_id', ${clinicId}, true)`;
```

The final `true` makes each setting transaction-local. The clinic ID is bound as a value rather than interpolated into SQL text. The helper also validates the expected identifier shape.

The active transaction store and routing extension attempt to send model operations through that same transaction client. Setting context on connection A cannot scope a query executed on connection B. Whether the latter query errors, denies rows or sees broader data depends on its role and policy; connection mismatch is not intrinsically an RLS bypass in every design.

## Understand the actual policy’s enable switch

The inspected migration enables row policies on tenant tables and contains this condition in both read visibility and write checks:

```sql
-- Excerpt of the inspected policy expression, not a complete migration.
current_setting('app.rls_enabled', true) IS DISTINCT FROM 'on'
OR "clinicId" = current_setting('app.current_clinic_id', true)
```

This is a staged-enforcement switch. When the enable setting is absent or not `on`, the first condition permits rows. When enabled, the clinic comparison determines the row boundary. The `true` argument to `current_setting` returns a missing setting as null instead of raising an error.

Consequently, the guarantee depends on more than the existence of a policy. Confirm the database role, table coverage, scope settings, query route, and intended privileged paths. Table owners and roles with bypass privileges have different behavior; the rollout document requires a non-owner application role and does not enable `FORCE ROW LEVEL SECURITY`.

## A routing limitation found during this review

The current routing core temporarily sets a shared async-store entry’s `tx` to null while awaiting a forwarded operation. An overlapping sibling operation can observe that null and take the base-client fallback:

```text
first query clears shared tx → first query waits
→ second query sees no active tx → second uses base client
→ first query finishes and restores tx
```

A source-extracted probe with controlled delegates reproduced this branch on 2 October 2026. It did not connect to a database or establish a production exposure. Given the policy’s enable switch, the fallback needs a database-level isolation test before claiming every concurrent query is routed and protected.

A safer routing design should keep recursion prevention local to the nested async scope, rather than mutate the sibling-visible store across an await. This is a proposed implementation correction, not a claim that the source repository was changed in this documentation pass.

## Explain ABAC using the current policy conditions

**RBAC** means role-based access control; **ABAC** means attribute-based access control, which evaluates facts such as resource ownership or assignment. Here `INTERNAL` is the application’s internal-access classification, not a universal database role.

The inspected patient policy has an INTERNAL bypass, patient ownership checks and clinical-role handling. Assignment is enforced for a plain DOCTOR when the resource marks `requiresAssignment`; it is not an unconditional rule for every doctor operation. The policy relies on resource attributes being populated correctly.

Avoid calling RBAC “90%” and ABAC “10%” of authorization without measurement. Explain the specific checks and their composition. Internal access, missing attributes and pre-tenant flows deserve explicit tests rather than a blanket “deny-overrides guarantees isolation” statement.

## Workers need explicit scope and narrow privilege

A background job can carry its validated clinic identity into a scoped transaction. Being outside HTTP does not inherently require access to all clinics. The inspected `runUnrestricted()` changes application tenant context to `bypassed: true`; that statement alone does not change a PostgreSQL role or automatically disable all database policies.

For genuinely cross-tenant work, define the job, credential, permitted operations and audit trail. A generic unrestricted helper is an escape hatch that needs evidence of controlled use.

## Verify the boundary before defending the claim

Test as the actual non-owner application role with two tenants: omitted scope, wrong scope, read and write checks, explicit/raw queries, nested transactions, concurrent sibling operations, rollback, connection reuse and worker paths. Test privileged paths separately. A test file’s existence is not a passing result, and a historical pass is not current deployment evidence.

For performance claims, measure representative query plans and load. The old universal RLS overhead percentage and tenant-count threshold for moving to distributed PostgreSQL were unsupported.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Tenant context and database policy provide complementary isolation mechanisms. |
| Current limitations | Isolation depends on the database role, applied policies, transaction context and every bypass path. |
| Recommended design | Use a non-owner runtime role, transaction-local tenant context, tenant-scoped constraints and separately authorized cross-tenant jobs; test every public resource operation against another tenant. |
| Evidence needed | A two-tenant matrix proves denied reads/writes, pooled-connection reuse does not leak context, and privileged jobs leave an attributable audit record. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Tenant isolation depends on trusted identity, resource authorization, transaction routing and database-role behavior working together. The source implements these mechanisms, but its enable switch and overlapping-query routing limitation prevent an unconditional guarantee without further verification.

## See Also

- [Revision](REVISION.md) — separate questions for the case-study category.
- [Async processing](03-async-processing.md) — carry scope across durable work.
- [Resume evidence pack](../../80-lanes-abroad-full-stack/80.17-docita-interview-evidence-pack.md) — separate source, tests and operational evidence.

## Source Evidence

Paths below are relative to the Docita source repository inspected on 2 October 2026:

| Evidence | Source path |
| ----------------------------- | ----------------------------------------------------------------------------- |
| Request context | `apps/api/src/shared/common/middleware/tenant.middleware.ts` |
| Request transaction | `apps/api/src/shared/common/interceptors/tenant-context.interceptor.ts` |
| Parameterized scope | `apps/api/src/shared/modules/rls/apply-rls-scope.ts` |
| Active transaction store | `apps/api/src/shared/modules/rls/active-tx.storage.ts` |
| Actual routing extension | `apps/api/src/shared/common/extensions/rls-routing.extension.ts` |
| Tenant and privileged context | `apps/api/src/prisma/prisma.service.ts` |
| Patient ABAC conditions | `packages/authorization/src/policies/patient.policy.ts` |
| Gated row policy | `packages/db/prisma/migrations/20260502143500_add_rls_policies/migration.sql` |
| Operator requirements | `docs/compliance/RLS_ROLLOUT.md` |

[← Previous: Architecture Decisions](01-architecture-decisions.md) · [Back to Index](INDEX.md) · [Next: Async Processing →](03-async-processing.md)
