# 07 — Prescription Validation and PDF Generation

## Definition

Prescription validation applies application rules before saving a medication order. PDF generation then presents a persisted prescription as a document. These are separate responsibilities: a readable PDF does not establish that the clinical decision was correct.

The engineering problem is to reject known invalid input without presenting a limited rule set as a complete clinical safety system.

## First Principles

A validator can only reason about the facts and rules it receives. Missing allergy records, unrecognized medication names and incomplete dose context remain unknown. Passing a check therefore means that this check did not reject the input, not that the prescription is safe for the patient.

Persistence and background processing also have different failure modes. A saved prescription may exist before a PDF is ready; a queued job may fail after the HTTP request succeeds. The UI must distinguish clinical record state from document-generation state.

## Why the Checks Run Before Persistence

The inspected command service follows this sequence:

```text
Doctor in clinic → signature field and VERIFIED status
                               ↓
                     patient in clinic
                               ↓
                  recorded-allergy matching
                               ↓
                      dose-string check
                               ↓
              controlled-substance context check
                               ↓
                save prescription → emit event
```

A missing doctor, missing patient or missing clinic context is rejected. The service requires a nonempty doctor signature URL and VERIFIED verification status. These are product checks over stored fields, not independent proof of registration validity or a cryptographic digital signature.

The create command can supply doctor details that override profile defaults. The PDF later reads some live doctor data, including the signature URL. If historical identity must be frozen, define trusted snapshot fields and allowed overrides explicitly.

## How Allergy Matching Works

The utility considers recorded allergies whose type is DRUG. It compares normalized medication and allergen names, then checks configured medication classes and cross-reactivity mappings.

A matched allergy with severity SEVERE or LIFE_THREATENING makes the prescription-level result critical and the command rejects creation. Other matched warnings are logged and creation continues through the remaining checks.

This is not drug–drug interaction analysis. It is also not evidence that a mild recorded reaction makes another drug acceptable. The severity and matching rules are implementation policy and require clinical ownership.

String matching has important boundaries: spelling, brand/generic naming, combination products, empty names and incomplete records can alter results. An empty allergy list skips this stage rather than proving absence of allergies. Normalize and validate recorded data, retain uncertainty, and test the configured rules without inventing patient-safety outcome counts.

## Examples: What a Dose-string Check Leaves Unknown

`validateDosage` parses a numeric value and optional unit from a string. It looks up a small configured table by normalized medication name and compares the number to the table's minimum and maximum.

| Input condition | Utility behavior | Command consequence |
| ------------------------------- | -------------------------------------- | -------------------------------------------------- |
| Cannot parse a number | Invalid with warning severity | Logs a warning; does not reject through this check |
| Medication absent from table | Valid flag with informational severity | Does not reject through this check |
| Number outside configured range | Invalid with critical severity | Rejects creation |
| Number within configured range | Valid and standard flags | Continues to other checks |

The parsed unit is not converted to the configured unit before comparison. The function also does not use dosing frequency to verify the table's maximum-daily field. Thus a numeric comparison alone cannot establish unit equivalence or total daily exposure.

The create path invokes the general utility, not the separate pediatric validator. Age, weight, route, indication, formulation, renal function and interactions are not inferred from that call. Keep this explanation about software behavior; do not use the table as prescribing guidance.

For reliable decision support, prefer structured medication identity, strength, unit, route and schedule, backed by a maintained and clinically reviewed rule source. Make uncovered inputs visible instead of treating an informational result as complete validation.

## Controlled-substance Matching Depends on Context

The command checks the medication list once, with an `isTeleconsultation` context. If the caller omits that field, it derives the value from the appointment type. An explicit caller value overrides that fallback, so verify who may supply it and whether it agrees with authoritative appointment data.

The utility matches configured generic terms with word boundaries. A brand name without the generic term may not match. In the implemented policy, a matched item in teleconsultation blocks creation; the in-person path logs matched categories and continues.

This describes the source's policy. It does not establish a complete current formulary, legal classification or all required prescribing documentation. Those rules need a maintained owner and independent validation.

## How the PDF Is Generated and Retrieved

The orchestrator exposes synchronous generation and explicit async enqueue. Async generation delegates to the shared PDF job service with prescription ID, type and clinic ID. The create service emits a local PRESCRIPTION_CREATED event; the event's existence alone does not prove that it durably enqueues every prescription PDF.

```text
Explicit async request → persisted job/status → worker generates bytes
                                                  ↓
                                             storage upload
                                                  ↓
                                      persist stored key/version
                                                  ↓
                                     authorized status/retrieval
```

Do not promise a fixed rendering duration or require WebSocket delivery as the only way to learn completion. A durable status endpoint and retryable retrieval can support clients that disconnect.

The synchronous `getPdf` path behaves differently by provider capability. With signed-URL storage, it returns a URL for an existing stored PDF or generates, uploads and persists one. Without signed-URL support, it generates a buffer directly. Storage capability is therefore part of the access design, not a cosmetic provider detail.

The generator requires clinic context and reads the prescription through a clinic-scoped repository call. It includes patient, clinic, doctor, medication and coded-diagnosis fields. The rendered date uses the current clock and signature resolution uses current doctor data; regeneration can differ from an earlier document even for the same prescription.

Upload happens before the prescription's stored PDF key and generation metadata are updated. A later database failure can leave an orphan object. The object key is stable per prescription, so concurrent or repeated generation also needs a deliberate overwrite/version policy.

## Real-world Decisions and Boundaries

Decide whether a rule failure blocks saving, requires explicit clinician acknowledgment, or leaves a review task. Separate uncovered input from a known violation. Warning-only paths must be visible to the decision-maker; logging alone does not ensure review.

Treat medication and patient facts as sensitive. The command logs warning counts rather than entire medication lists in some paths, but that does not establish privacy across every event, PDF, storage metadata and downstream service.

The local event and usage call occur after persistence. The usage call catches failure, and local event delivery is not a durable outbox. A successful create response does not prove downstream document generation or usage accounting completed. Use reconciliation when those effects are required.

## Mistakes and Best Practices

- Claiming zero clinical incidents or blocked dangerous orders from source inspection: measure outcomes separately.
- Calling a signature image a cryptographic signature: specify what authenticity the mechanism actually provides.
- Calling a passed string check comprehensive dose validation: inspect units, identity and missing context.
- Treating async work as automatically reliable: trace enqueue, claim, retries, completion and disconnected clients.
- Treating a regenerated PDF as immutable historical evidence: snapshot trusted inputs and version documents when required.

Test tenant-scoped references, missing profile fields, unsupported medication names, unparseable input, unit mismatch, warning/block behavior, authoritative consultation context and failures between upload and metadata persistence.

## Code Evidence

Paths are in the inspected Docita checkout; these are implementation observations rather than clinical or production validation.

| Mechanism | Source path |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| Create checks and side effects | `apps/api/src/domains/prescriptions/application/services/prescriptions-command.service.ts` |
| Recorded allergy matching | `packages/utils/src/medical/allergy-validation.ts` and `allergy-matchers.ts` |
| Dose-string policy | `packages/utils/src/medical/dosage-validation.ts` |
| Context-sensitive matching | `packages/utils/src/medical/controlled-substance-validation.ts` |
| PDF generation and persistence | `apps/api/src/domains/prescriptions/application/services/prescription-pdf-orchestrator.service.ts` |
| Async job lifecycle | `apps/api/src/shared/modules/queue/pdf-job.service.ts` |

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | The command rejects configured critical conditions before persistence and separates PDF orchestration. |
| Current limitations | String-based rules and live rendering inputs do not establish comprehensive clinical safety or immutable history. |
| Recommended design | Use trusted structured medication/context data with clinically owned versioned rules; surface uncovered inputs and acknowledgements; snapshot authorized document inputs and version generated artifacts. |
| Evidence needed | Rule fixtures distinguish rejected, acknowledged and uncovered cases; tenant boundaries hold; regenerated documents can be traced to their input and rule/template versions. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Explain each validation rule through its inputs, rejection condition and unknowns. Keep clinical record creation separate from PDF generation, storage and delivery. A passed application check or generated document is narrower evidence than a safe prescription or immutable clinical history.

## See Also

- [Category revision](REVISION.md) — validation and PDF questions.
- [Async processing](03-async-processing.md) — local events and durable jobs.
- [Documents and uploads](19-documents-and-uploads.md) — storage and signed access.
- [Clinic workflows](05-clinic-workflows.md) — consultation state and tenant scope.
- [Case-study index](INDEX.md) — reading order.
