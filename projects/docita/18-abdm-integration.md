# 18 — ABDM Integration (India's Health Stack)

> Interoperability with India's Ayushman Bharat Digital Mission — care contexts, consent-based data sharing, and an outbound/inbound transaction ledger where every gateway callback is recorded as a state transition, not trusted blindly.

---

## Context

ABDM (Ayushman Bharat Digital Mission) is India's national health interoperability layer. A clinic with an ABHA-linked patient can share records with any other ABDM participant — labs, hospitals, insurers — **but only with the patient's explicit, granular consent**. Docita's `abdm` domain implements the provider (HIP) side:

- **Care contexts** — each sharable clinical resource (a prescription, a record bundle) gets a reference like `DOCITA-{sourceType}-{sourceId}`.
- **Link requests** — ask ABDM to associate a care context with a patient's ABHA address.
- **Consent requests** — request the patient's permission to share.
- **Data pushes** — when consent is granted, push health information to the requesting participant's data-push URL.
- **Gateway callbacks** — ABDM calls back asynchronously (link granted, consent granted/denied, data-push accepted); Docita must correlate each callback to its originating request.

**The problems:** (1) ABDM is an *async, callback-driven* gateway — Docita fires a request, gets nothing synchronously, and must reconcile a callback that may arrive minutes later (or never); (2) callbacks arrive at a **public** endpoint keyed only by clinicId + type — the request must be correlated to a specific consent/care-context without trusting the payload; (3) no gateway config (dev vs prod) must behave safely — the system must record *pending/retryable* state instead of failing loudly; (4) push payloads carry PHI to an external URL — failures must be auditable with full context.

---

## Decision 1: A Transaction Ledger as the Single Source of Truth

### What We Chose

Every interaction with ABDM — care-context creation, link request, share request, consent request, inbound callback, outbound push — writes an **`AbdmTransaction`** row with `type`, `direction` (INBOUND/OUTBOUND), `status` (`SUCCEEDED`/`FAILED`/`RETRYABLE`/`PENDING`), `requestId`, `transactionId`, and `correlationId` (the care-context reference). The ops inbox (`getOpsInbox`) is literally a query over these states:

```typescript
// apps/api/src/domains/abdm/application/services/abdm-exchange.service.ts
listTransactions(clinicId, ['RETRYABLE']),
listTransactions(clinicId, ['FAILED']),
listConsentRequests(clinicId),
listExternalRecords(clinicId),
```

### Why This Was Chosen

- **Callback-driven flows need a durable memory** — Docita can't keep an in-flight map in RAM across restarts; the ledger survives crashes and gives the ops inbox its content.
- **Correlation is explicit** — every outbound request stores the `requestId`/`transactionId`/`correlationId` trio, and every callback handler looks up by those keys instead of trusting payload shape alone.
- **Status vocabulary matches reality** — `RETRYABLE` (gateway not configured / provider hiccup) is distinct from `FAILED` (a real rejection); the ops inbox surfaces exactly the rows a human or a retry job should act on.

### Trade-offs

- **The ledger is a write-amplifier** — one logical flow (link + consent + push) can write 5+ transaction rows; cheap at this volume, but it's a lot of rows for a small clinic.
- **A retry job over RETRYABLE rows exists only as an inbox** — nothing *automatically* re-drives RETRYABLE transactions yet; it's manual via the inbox (see What Could Be Better).

---

## Decision 2: Gateway-Configurable Degradation (No Config = Safe Recorded State)

### What We Chose

Before any external call, the code checks `gateway.isConfigured()`. If the ABDM gateway isn't configured (local dev, staging, or a clinic that disabled ABDM), the request still writes its ledger row but marks it `RETRYABLE` instead of throwing:

```typescript
// abdm-exchange.service.ts — requestCareContextGatewayAction
await this.repository.createTransaction({ ..., status: gatewayConfigured ? 'PENDING' : 'RETRYABLE', ... });
```

Care-context *creation* is purely local (a reference number + `hiType`), so it always succeeds. Only the gateway-touching steps degrade. `assertClinicAbdmEnabled` also guards the whole domain — a clinic that hasn't opted into ABDM gets a clean error before any ledger noise.

### Why This Was Chosen

- **Dev/CI never depends on a live national gateway** — the domain is fully testable without network access; specs stub the gateway client (`abdm-exchange.service.spec.ts`).
- **Failure is recorded, not swallowed** — the RETRYABLE rows are visible in the ops inbox, so "did this ever send?" is answerable even when the gateway was down at request time.
- **Feature-opt-in per clinic** — ABDM is a capability clinics enable; the domain is off by default and loud when used without enablement.

### Trade-offs

- **A misconfigured production gateway silently accumulates RETRYABLE rows** rather than paging someone; the heartbeat/alerting around the ops inbox is the missing piece.

---

## Decision 3: Callbacks Are Reconciliations, Not Events

### What We Chose

The public callback endpoint (`POST /abdm/callbacks/:clinicId/:type`) is handled by `AbdmCallbackStateService.applyCallbackState`, which treats every callback as a **state update against a known ledger row**, never as a trigger to trust fresh data:

- Consent callbacks → update the consent request (`GRANTED`/`FAILED`), storing the raw artifact.
- Link callbacks → find the care context **by reference**, mark it linked only if the callback "looks successful".
- Data-push callbacks → resolve the care context by reference; if it's missing, record a `FAILED` M2_DATA_PUSH transaction with a descriptive error ("ABDM care context not found for data push") instead of crashing.

```typescript
// abdm/application/services/abdm-callback-state.service.ts
if (normalizedType.includes('consent')) {
  await this.repository.updateConsentFromCallback({ ... status: callbackLooksSuccessful(callback) ? 'GRANTED' : 'FAILED', rawArtifact: ... });
}
```

`callbackLooksSuccessful` normalizes the status string (`ok/success/succeeded/granted/linked`) so ABDM's vocabulary variants map to one boolean without per-branch string compares scattered around.

### Why This Was Chosen

- **The ledger row is the source of truth; the callback is evidence** — a malicious or malformed callback can't create state out of thin air because every update keys off an existing requestId/care-context reference.
- **Failed reconciliations are first-class** — the "care context not found" branch writes an auditable FAILED row rather than an unhandled exception that loses the correlation data.
- **Raw payloads are persisted** (`rawArtifact`) so a disputed callback can be re-examined later — the same audit instinct as the claims/verification domains.

### Trade-offs

- **Callback → ledger updates are per-type branches** (consent vs link vs push) rather than a generic state machine; a new ABDM callback type (e.g., consent *revocation*) adds a branch. Fine while the surface is small.

---

## Decision 4: FHIR + Encrypted Health-Information Push

### What We Chose

Outbound sharing converts Docita records through the shared `FhirService` (`shared/modules/fhir`) and pushes via `gateway.pushHealthInformation` with `dataPushUrl`, `transactionId`, `careContextReference`, `hiType`, and the gateway-provided **encryption material** — ABDM mandates encrypted payloads for data in transit to participants. The `M2_DATA_PUSH` direction is recorded per transaction, and dispatches happen from callbacks via `dispatchDataPushFromCallback` (ABDM sends the data-push URL in the consent callback).

### Why This Was Chosen

- **One FHIR module, many consumers** — the same `FhirService` serves ABDM exports; Docita doesn't hand-roll per-participant formats.
- **Encryption is the gateway's contract** — the code passes through the encryption material ABDM supplies rather than inventing its own scheme, which is the only way to interoperate.

### Trade-offs

- **FHIR conversion correctness is the silent risk** — a wrong code system or missing field may pass the push but fail downstream validation at the receiving participant; there's no end-to-end test against a real HIU.

---

## What Worked

- **Ledger-first design made the async gateway debuggable** — every "did the consent ever come back?" support question is answered by one ops-inbox query over transaction rows.
- **Config-gated degradation kept CI green** — no test or local run ever depended on the live ABDM gateway, while production got honest RETRYABLE rows.
- **Correlation-by-reference held** — care-context references (`DOCITA-{type}-{id}`) proved stable across callbacks; the "context not found" defensive branch never fired in anger but exists exactly where a mismatch would surface.

## What Failed

- **First integration assumed synchronous-ish callbacks** — early code polled the gateway for consent status after a fixed delay; real ABDM latency made that wasteful and racy. Replaced with the pure callback-reconciliation model.
- **Callback auth was initially under-specified** — the endpoint is keyed by clinicId+type in the path; early review flagged that the payload (not the path) must drive correlation, and the reconciliation model (Decision 3) was the response. Gateway-level signature verification remains TODO.
- **Devices with disabled ABDM generated confusing ops-inbox rows** — before `assertClinicAbdmEnabled`, misconfigured clinics polluted the ledger with RETRYABLE rows that looked like real failures.

## What Could Be Better

- **Automatic retry job** over `RETRYABLE` transactions (with backoff) — the inbox currently requires a human.
- **Callback signature verification** against ABDM's published keys — the domain correlates safely, but the public endpoint itself should authenticate the gateway.
- **Consent revocation handling** — a patient revoking consent mid-sharing should cascade to a stored state, not just a callback row.
- **End-to-end FHIR contract tests** against a sandbox HIU to de-risk silent conversion errors.

---

## Code Evidence

| Claim | File |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Care contexts / link / share / consent orchestration | `apps/api/src/domains/abdm/application/services/abdm-exchange.service.ts` |
| Command facade | `apps/api/src/domains/abdm/application/services/abdm-command.service.ts` |
| Callback reconciliation | `apps/api/src/domains/abdm/application/services/abdm-callback-state.service.ts` |
| ABHA client | `apps/api/src/domains/abdm/infrastructure/abdm-abha.client.ts` |
| Gateway client | `apps/api/src/domains/abdm/infrastructure/abdm-gateway.client.ts` |
| Ledger repository | `apps/api/src/domains/abdm/infrastructure/repositories/prisma-abdm.repository.ts` |
| HTTP surface (incl. public callbacks) | `apps/api/src/domains/abdm/presentation/controllers/abdm.controller.ts` |
| FHIR conversion | `apps/api/src/shared/modules/fhir/fhir.service.ts` |

---

## Interview Script (60 seconds)

> "ABDM is an asynchronous, callback-driven national gateway, so I built every interaction on a durable transaction ledger — each care-context creation, link/share/consent request, and callback writes a row with type, direction, status (succeeded/failed/retryable), and a correlation triple. The ops inbox is literally a query over that ledger, so 'did the consent come back?' is a SQL query, not a hunt through logs. Two decisions matter most. First, safe degradation: if the gateway isn't configured, requests still record their ledger row as RETRYABLE instead of throwing, so dev and CI never depend on a live national gateway while production failures stay visible. Second, callbacks are reconciliations, not trusted events: every callback updates an existing ledger row keyed by requestId or care-context reference, raw payloads are stored for audit, and a failed match writes a descriptive FAILED row instead of crashing. The gap I'd close next: automatic retries over RETRYABLE rows and gateway callback signature verification."

---
