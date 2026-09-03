# 21 — Clinical, Lab Orders & Medical Coding

> The second clinical pillar beyond prescriptions: a lab-order lifecycle (order → sample → result → paid → released) whose release gate is *payment AND result*, and an ICD-10/CPT medical-coding layer that syncs the national code catalog in the background, searches it with a circuit-breaker, and feeds the insurance-claims readiness gate from deep-dive 11.

---

## Context

Deep-dive 07 covered prescriptions — the outpatient Rx side of clinical care. The `clinical` domain holds the rest of the clinical data model, in two halves:

**Lab workflow** — clinics order lab tests (internally or to an external lab directory). An order moves through: ORDERED → SAMPLE_COLLECTED → (result uploaded → RESULT_READY) → (payment verified) → COMPLETED, or CANCELLED. The patient receives the result over WhatsApp — *but only after payment*.

**Medical coding** — ICD-10-CM (diagnoses) and CPT/HCPCS (procedures) codes, which Indian billing and insurance claims depend on (deep-dive 11's readiness gate checks "uncoded diagnoses/procedures"). Doctors search the catalog at billing time and mark favorites; the system auto-suggests and syncs a *common codes* subset locally so search works offline of the national API.

**The problems:** (1) releasing a lab result is a *financial + clinical* gate — a clinic that gives away results before payment loses revenue, but a lab that withholds a result after payment breaches care; (2) the code catalog is huge (ICD-10-CM is ~70k codes) and lives on an *external* API — search must not block on a flaky national service, and the local sync must be incremental and batched; (3) CPT is proprietary (AMA-licensed) while ICD and HCPCS are public (NLM) — one provider abstraction must hide two very different licensing realities; (4) every lab step is PHI-sensitive and clinic-scoped.

---

## Decision 1: Lab Order Release = `result AND paid`, Encoded in the Entity

### What We Chose

The `LabOrder` domain entity carries the rule as a method, not scattered `if`s:

```typescript
// core/entities/lab-order.entity.ts
/** Results may only be released to the patient once the lab has uploaded a
 *  result AND the front desk has verified payment. A released/cancelled order
 *  cannot be released again. */
canRelease(): boolean {
  return !this.isTerminal() && this.hasResult() && this.isPaid();
}
```

The command service then has two entry points — `uploadResult` and `verifyPayment` — and *both* end by calling `releaseIfReady`, which re-loads the order (so the decision reflects the just-committed write, not a stale copy) and releases if `canRelease()`:

```typescript
// application/services/lab-workflow-command.service.ts
async uploadResult(id, clinicId, file, input) {
  ...
  await this.workflowRepository.attachResult(id, clinicId, {...}, now);
  await this.releaseIfReady(id, clinicId);   // result present, is it paid?
}

async verifyPayment(id, clinicId, data) {
  ...
  await this.workflowRepository.verifyPayment(id, clinicId, data, now);
  await this.releaseIfReady(id, clinicId);   // paid — is the result there?
}
```

### Why This Was Chosen

- **The release gate is a conjunction, whichever side arrives last triggers it** — a lab that uploads a result before the front desk verifies cash, and a front desk that verifies payment before the lab uploads, both converge on the same outcome without either side needing to know the other's state.
- **The entity is the single owner of the rule** — `canRelease()` is unit-testable without Prisma (`lab-order.entity.spec.ts`) and can't drift between the two call paths.
- **Terminal states are respected** — releasing twice, releasing a cancelled order, or uploading to a completed order all throw `BadRequestException` at the service boundary.

### Alternatives Considered

- A state machine (like claims) with RELEASE as a first-class transition — the order statuses already encode the timeline; the conjunction lives in the entity because "result uploaded" and "paid" are *fields*, not statuses. Forcing them into a status enum would have doubled the state space (RESULT_READY_PAID, RESULT_READY_UNPAID...).
- Manual release button only — rejected: it would depend on a human noticing both preconditions.

### Trade-offs

- **No "released without WhatsApp" retry** — release sends the WhatsApp template once; a delivery failure (Meta outage, no phone) is logged and the release still completes. There's no re-send path except a manual re-release (which the terminal guard blocks!). See What Could Be Better.
- **Payment verification is manual at the front desk** — no reconciliation against the invoice/payment rails from deep-dive 04; a cash payment for a lab test is recorded in the lab domain, not linked to the billing invoice.

---

## Decision 2: Release Delivery = Signed URL + WhatsApp Template, Degrading Gracefully

### What We Chose

On release, the workflow loads a `LabOrderReleaseContext` (order + patient + test name + clinic name), generates a **15-minute signed URL** for the result file when the storage provider supports it (reusing deep-dive 19's `GENERATED_PDF_SIGNED_URL_TTL_SECONDS`), and sends the `lab_result_ready` WhatsApp template with patient name, clinic name, test name, date, and the link:

```typescript
// lab-workflow-command.service.ts (releaseResult)
const resultLink = this.storageProvider.supportsSignedUrls
  ? await this.storageProvider.generateSignedUrl(ctx.resultUrl, GENERATED_PDF_SIGNED_URL_TTL_SECONDS)
  : ctx.resultUrl;

try {
  await this.sendMessage.execute({ ..., templateName: 'lab_result_ready', variables: { ..., resultLink } });
} catch (error) {
  if (error instanceof ForbiddenException) {
    this.logger.log(`Lab result WhatsApp skipped for order ${id}: ${error.message}`);  // template not approved — not fatal
  } else {
    this.logger.error(`Failed to send lab result WhatsApp for order ${id}`, error);
  }
}
```

### Why This Was Chosen

- **PHI lifetime discipline inherited from the storage layer** — a lab result link in a patient's WhatsApp is a 15-minute bearer URL, not a permanent one (same policy as prescription PDFs).
- **Template rejection ≠ broken release** — Meta template approvals are outside Docita's control; a `ForbiddenException` from an unapproved template logs and continues rather than wedging the order in COMPLETED-but-unsent limbo. Other failures are logged loudly for investigation.
- **The send is a use-case, not a direct client call** — `SendMessageUseCase` (from the WhatsApp domain) keeps the clinical domain depending on a capability, mirroring the port pattern used across the codebase.

### Trade-offs

- **Fire-and-forget after the first attempt** — no queued retry, no delivery receipt handling in this path (the WhatsApp domain's daily reconciliation covers delivery broadly, but a per-order "did the patient open it?" trail isn't here).
- **Patients without a phone number** get a logged warning and *no result delivery* — the release still happens (the result is in the clinic's worklist), but the "send the result to the patient" promise silently degrades.

---

## Decision 3: Code-Catalog Provider Abstraction Over Two Licensing Realities

### What We Chose

A `CodeCatalogProvider` port defines four operations: `searchIcdCodes`, `searchCptCodes`, `streamIcdCodes(onBatch)`, `streamCptCodes(onBatch)`. Three implementations exist:

- `NlmCodeCatalogProvider` — ICD-10-CM from the public NLM clinical tables API; CPT searches go to NLM's **HCPCS** table (public), mapped onto the CPT model.
- `LicensedCptCodeCatalogProvider` — the AMA-licensed CPT catalog behind an API key (config-gated); Zod-validated responses with cursor pagination (`nextCursor`).
- `CompositeCodeCatalogProvider` — chooses the CPT source at runtime from config (`getCptCatalogSource()`: `nlm_hcpcs` | `licensed`), defaulting to NLM, while ICD always routes to NLM.

```typescript
// infrastructure/external/composite-code-catalog.provider.ts
private resolveCptProvider(): CodeCatalogProvider {
  const source = this.config.getCptCatalogSource();
  return this.cptProviders.get(source) ?? this.nlmProvider;
}
```

### Why This Was Chosen

- **Licensing is a deployment concern, not a code concern** — customers who hold a CPT license get `licensed`; everyone else legally uses public HCPCS data. The domain code never branches on licensing — the composite resolves it once.
- **Search and stream share one shape** — whether the source is NLM or licensed, the sync service (below) and the search endpoints consume identical interfaces, so adding a new catalog source later is one provider class.
- **The licensed provider is defensive about its contract** — every response is validated with a strict Zod schema (unknown keys rejected), because a paid API changing shape silently would corrupt the local catalog.

### Trade-offs

- **HCPCS ≠ CPT** — NLM's HCPCS table is the public proxy for procedure codes; descriptions and code sets overlap but aren't identical to licensed CPT. Claims submitted with HCPCS-derived codes may differ from AMA CPT — an honest limitation for non-licensed customers (and exactly why the licensed provider exists).
- **Config indirection** — a misconfigured `cptCatalogSource` silently falls back to NLM (the `?? this.nlmProvider` default); fine for correctness, potentially surprising for a customer who paid for CPT.

---

## Decision 4: Search With a Circuit Breaker; Sync as Streamed, Batched Upserts

### What We Chose

**Search path** — the NLM client wraps every call with a per-system circuit breaker: on failure it `markSearchUnavailable(system, reason)` and refuses further calls for a cooldown (`NLM_FAILURE_COOLDOWN_MS` = 5 min), returning empty/offline results instead of hammering a down national API; a successful call clears the breaker (`clearSearchUnavailable`). ICD and HCPCS breakers are independent (one system failing doesn't disable the other).

**Sync path** — `MedicalCodeSyncService.syncCommonCodes()` runs ICD and CPT syncs in parallel. Each streams the external catalog in batches (ICD paginated by letter-prefix `A–Z`, page size 500, max offset 7500; CPT/HCPCS prefixes `A–V`, filtered `obsolete:false`) and for every batch:

1. Dedupes by code.
2. `findExisting` for the batch's codes.
3. Splits into records-to-create vs records-to-update (update only when description/category changed or the code isn't yet flagged common).
4. Bulk-creates new; bulk-updates in chunks of 100 (`UPDATE_BATCH_SIZE`).

```typescript
// medical-code-sync.service.ts
await this.codeCatalogProvider.streamIcdCodes(async (batch) => {
  await this.syncCodeBatch({
    records: batch,
    findExisting: (codes) => this.medicalCodingRepository.findExistingIcdCodes(codes),
    createMany: (data) => this.medicalCodingRepository.createCommonIcdCodes(data),
    updateMany: (data) => this.medicalCodingRepository.updateCommonIcdCodes(data),
  });
  batch.forEach((c) => seen.add(c.code));
});
```

The cron runs on `CRON_SCHEDULES.MEDICAL_CODE_SYNC`, heartbeat-tracked, disabled in non-cron processes.

### Why This Was Chosen

- **Search UX must never hang on NLM** — doctors type diagnoses at billing time; a 5-second NLM timeout with a 5-minute cooldown is the difference between "coding works" and "billing is blocked by a third party."
- **Sync is incremental and idempotent** — the find-then-create/update split means re-running the sync is safe; the `isCommon` flag is the actual write (full catalog rows exist for codes the clinic has used; the sync *promotes* the common subset).
- **Batching bounds memory and transactions** — streaming with per-batch callbacks never loads the full catalog into memory; 100-row update chunks keep each statement small.
- **Prefix-parallel streaming respects the API's shape** — NLM's offset API is capped; walking letter prefixes is how the *entire* catalog is reachable within the cap.

### Trade-offs

- **The sync covers the "common" surface, not literally all ~70k ICD codes** — `NLM_SYNC_MAX_OFFSET = 7500` per prefix run bounds the sync; ultra-rare codes are searchable live but may not be in the local common set.
- **Search falls back to live API** when the code isn't local — which reintroduces the external dependency for the long tail; acceptable, but the circuit breaker is the safety net.
- **Sync failure modes are per-run** — if a sync crashes mid-stream, the partial batch is already committed (create/update per batch); re-running converges (idempotent), but there's no transactional all-or-nothing.

---

## Decision 5: Coding Settings + Favorites Are Per-Clinic, Feature-Flagged

### What We Chose

`ClinicalSettingsService` reads clinic settings through a strict Zod schema (`medicalCodingEnabled`, `medicalCodingProvider`, `medicalCodingAutoSuggest`, `medicalCodingPreferredSystem`) with sensible defaults (`enabled !== false`, provider `internal`, autoSuggest on, preferred system ICD-10). The medical-coding controller exposes per-clinic ICD/CPT search, **doctor favorites** (add/remove/list per code system), common-code lists, and an **uncoded-visits** endpoint — the same data the claims readiness gate (deep-dive 11) aggregates for `assertClaimReady`.

### Why This Was Chosen

- **Coding is an opt-out-able capability per clinic** — small clinics may skip medical coding entirely (their insurance volume doesn't justify it); the settings gate keeps it from being forced on every workflow.
- **Favorites are the doctor-productivity layer** — a physician's top 20 diagnoses differ by specialty; favorites + autoSuggest + common codes together make search fast enough that doctors actually code instead of skipping it (which is what makes the claims gate meaningful).
- **Settings defaults are "on"** — `enabled !== false` and `autoSuggest !== false` mean the feature works before anyone configures it; strict-schema validation means a bad write is rejected, not silently stored.

### Trade-offs

- **Settings live in the clinic settings JSON blob** — `normalizeSettings` defensively reads raw values with fallbacks; a typo'd key silently yields the default rather than failing (deliberate, but hides config errors).
- **Uncoded-visits is a cross-domain read** — computed by the clinical repo over appointments/invoices that other domains own; the coupling is read-only and behind the repo interface, but it's the same "read other domains' tables" pattern that needs care under RLS.

---

## What Worked

- **The conjunction release gate never leaked a result or a payment** — the symmetric `releaseIfReady` on both paths meant the "result first" and "payment first" orderings both ended in a single, correct release.
- **The NLM circuit breaker absorbed real outages** — when NLM throttled, search degraded to local common codes + favorites instead of timing out every keystroke; the per-system breakers meant an ICD outage didn't kill CPT search.
- **Streamed sync loaded the catalog without memory spikes** — prefix-walking + 500-row batches kept the sync bounded, and re-runs converged cleanly (idempotent upsert by code).
- **The provider abstraction absorbed the CPT licensing decision** — adding the licensed provider required zero changes in the sync service or controllers; config flipped the source.

## What Failed

- **First sync attempt tried to fetch the full catalog in one request** — NLM's API caps offsets; the code hit the cap and silently truncated the catalog until prefix-walking replaced single-stream pagination.
- **A release with an unapproved WhatsApp template wedged the order** — an early version treated template failure as fatal *after* marking released, leaving orders COMPLETED but patients never notified; the `ForbiddenException`-is-a-log branch fixed the state/notification mismatch.
- **Favorites were initially global** — doctors at different clinics shared favorite lists until favorites became clinic- and doctor-scoped; cross-clinic doctors (deep-dive 15) were the trigger.

## What Could Be Better

- **Result re-send path** — the terminal guard correctly prevents double-release, but a patient who lost the 15-minute link has no way to get it again; a "re-generate signed URL without re-releasing" endpoint would fix the patient experience without weakening the gate.
- **Link lab payment to billing** — verifying payment in the lab domain while invoices live in billing means a clinic can't see "lab revenue" reconciled with invoices; a payment-reference link to deep-dive 04's rails would close it.
- **Sync alerting on drift** — if the external catalog changes descriptions, the sync updates rows silently; a "N codes changed this sync" digest would surface catalog churn.
- **AutoSuggest needs an audit** — `autoSuggest` currently suggests from common codes + history; there's no feedback loop on whether suggestions get accepted (which would make the claims gate even cleaner).

---

## Code Evidence

| Claim | File |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Lab order entity + release rule | `apps/api/src/domains/clinical/core/entities/lab-order.entity.ts` |
| Workflow command (release gate, WhatsApp) | `apps/api/src/domains/clinical/application/services/lab-workflow-command.service.ts` |
| Workflow query (queue) | `apps/api/src/domains/clinical/application/services/lab-workflow-query.service.ts` |
| Lab order repository (statuses) | `apps/api/src/domains/clinical/infrastructure/persistence/prisma-lab.repository.ts` |
| Code sync service (batched upsert) | `apps/api/src/domains/clinical/application/services/medical-code-sync.service.ts` |
| Sync cron | `apps/api/src/domains/clinical/medical-code-sync.cron.ts` |
| Catalog provider port | `apps/api/src/domains/clinical/core/providers/code-catalog.provider.ts` |
| Composite (licensing switch) | `apps/api/src/domains/clinical/infrastructure/external/composite-code-catalog.provider.ts` |
| NLM client (circuit breaker, prefix stream) | `apps/api/src/domains/clinical/infrastructure/external/nlm-coding.client.ts` |
| Licensed CPT provider | `apps/api/src/domains/clinical/infrastructure/external/licensed-cpt-code-catalog.provider.ts` |
| Coding settings (strict schema) | `apps/api/src/domains/clinical/application/services/clinical-settings.service.ts` |
| Medical-coding HTTP surface | `apps/api/src/domains/clinical/presentation/controllers/medical-coding.controller.ts` |
| Lab workflow + tests controllers | `apps/api/src/domains/clinical/presentation/controllers/lab-workflow.controller.ts`, `lab-tests.controller.ts` |
| Claim readiness gate consumer | `apps/api/src/domains/billing/core/services/claim-validation.service.ts` |

---

## Interview Script (60 seconds)

> "The clinical domain has two halves. Lab orders move ORDERED → SAMPLE_COLLECTED → RESULT_READY → COMPLETED, and the release gate is a conjunction encoded in the domain entity: a result goes to the patient only when a result file exists AND payment is verified. Both the upload-result and verify-payment commands end by calling the same `releaseIfReady`, so whichever side arrives last triggers the release — a lab that uploads before payment and a front desk that verifies before the lab uploads converge on the same outcome. On release, the patient gets a WhatsApp message with a 15-minute signed URL, and a template rejection is logged, not fatal. The second half is medical coding: one `CodeCatalogProvider` port hides two licensing realities — public NLM ICD/HCPCS and an API-keyed licensed CPT catalog — chosen by config at runtime. Search has a per-system circuit breaker with a five-minute cooldown so billing never hangs on a flaky national API, and a heartbeat cron streams the catalog in letter-prefixed batches, deduping and upserting into a local common-codes table that feeds both doctor search and the insurance-claims readiness gate."

---
