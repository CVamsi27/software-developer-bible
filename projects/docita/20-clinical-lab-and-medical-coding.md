# 20 — Lab Release and Medical Code Catalogs

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

The clinical domain combines two distinct capabilities: lab-order workflow and medical-code lookup/synchronization. Lab workflow connects results to a local release policy. Coding supplies identifiers used in clinical records and claim-readiness checks.

A lab result can be ready before its payment flag is recorded, while a catalog search can fail because an external service is unavailable. Neither case should be hidden behind a generic successful status.

## First Principles

A release predicate can express policy clearly, but evaluating it before an external send does not prevent another request from evaluating it too. State authorization, notification attempt and patient delivery need separate identities and states.

A local code catalog is a materialized view of an external source. A partial sync, changed description or fallback source can make it stale or semantically different. Source, code system and version are part of a code's identity—not merely its text.

## Why Lab Release Uses Two Preconditions

`LabOrder.canRelease()` requires a non-terminal order, a result URL and a paidAt value. Both upload-result and verify-payment paths reload the order and invoke releaseIfReady. This lets either ordering reach the same local eligibility condition.

That conjunction describes implemented product policy, not a universal clinical or legal justification for withholding results. Clinical/financial policy ownership, urgent access and permitted overrides need explicit decisions outside this Boolean method.

Payment verification here records method, reference and verifier. It does not independently reconcile the amount against a billing invoice or provider collection. A paidAt field is local evidence of the workflow action.

## How Release and Notification Actually Run

The command rejects an earlier terminal snapshot. Result upload stores an object, attaches its key, then checks release eligibility. Payment recording updates local payment fields and checks eligibility.

Release reloads context, requires result and paidAt, prepares a result link, attempts WhatsApp send, catches send failures, then marks the order COMPLETED/released. Notification happens before the final state write, not as one transaction with it.

```text
Ready result + local payment flag
                 ↓
Read release context → generate access link
                 ↓
Attempt WhatsApp send; log caught failure
                 ↓
Mark order COMPLETED and released
```

Two concurrent releasers can both send before either marks completion. The repository's markReleased update filters ID and clinic, without a conditional current-status or release-ownership predicate. A cancelled order can also change after the earlier check. Reloading reduces staleness but does not create an atomic claim.

The URL-generation call occurs outside the send try/catch. A signing failure can stop release, while a caught send failure permits completion. A ForbiddenException does not necessarily mean template rejection; entitlement and other permission checks can produce it.

No patient phone logs a warning and still permits local release. Distinguish released/available from notified and delivered. The WhatsApp stale sweep reports unresolved delivery; it does not automatically resend or repair it.

## Examples: Result-first and Payment-first

| Ordering | Local eligibility |
| ---------------------------- | --------------------------------------------- |
| Upload first, no paidAt | Keep result attached; wait for payment action |
| Payment first, no result URL | Keep payment evidence; wait for result upload |
| Both present, non-terminal | Try the release path |
| COMPLETED or CANCELLED | Reject through the current service checks |

These cases test the predicate. Add concurrent calls, cancellation during release, signing failure, notification failure and crash after accepted send to test the full mechanism.

For providers supporting signed URLs, the result link uses the shared PDF-access TTL of 15 minutes. Otherwise the stored URL/key is used directly. This is not a universal expiring private link: provider capability, key resolution and authenticated retrieval determine access.

A separate authorized retrieve/re-notify operation can refresh access without reopening a terminal clinical order. Stable notification identity and recovery should preserve the original release evidence.

## Coding Providers Must Preserve Code-system Identity

The port exposes ICD/procedure search and batch-stream operations. The composite routes ICD to NLM and selects procedure source from configuration: NLM HCPCS or a configured licensed provider. The latter validates response shapes and uses cursor pagination, but can fall back to NLM on missing configuration or failure.

NLM's referenced endpoint supplies HCPCS **Level II**, which is distinct from CPT. Mapping that response into a model named CptCode does not turn it into CPT or establish jurisdiction/insurer suitability. Retain code system, source, version and applicable rights explicitly. [NLM HCPCS API documentation](https://clinicaltables.nlm.nih.gov/apidoc/hcpcs/v3/doc.html).

Provider configuration does not itself grant a license. A fallback can change semantic coverage and mix systems in the local table, particularly after a partial licensed stream. Surface the active source and degraded state rather than silently presenting interchangeable results.

## How Search Cooldown and Sync Work

The NLM client maintains per-system cooldown state. Configured search requests use five-second timeouts; a failure suppresses subsequent external calls for five minutes. This bounds repeated failure pressure, but does not prove every keystroke succeeds locally or that all instances share one breaker.

The stream walks prefixes sequentially with page size 500 and an offset bound of 7500. NLM documents those pagination limits, and search terms are partial matches; walking letter terms alone is not proof of exhaustive catalog coverage. [NLM pagination contract](https://clinicaltables.nlm.nih.gov/apidoc/hcpcs/v3/doc.html).

The client catches a fetch failure, marks cooldown and returns from streaming. The sync can then report the number seen without an explicit complete/partial result. A resolved promise is not proof of full synchronization.

For each batch, MedicalCodeSyncService deduplicates code strings, reads existing rows, creates missing entries and updates changed descriptions/categories or common flags in chunks of 100. ICD and procedure syncs run concurrently. Committed batches remain if a later batch fails.

This is useful incremental work, but find-then-create requires database uniqueness/conflict handling under concurrent runs. The seen set grows with unique codes, so streaming bounds page payloads rather than all memory. Description updates also need a historical version policy for already-coded records.

A reliable sync retains source/version, cursor/checkpoint, attempted and completed coverage, additions/changes/retirements, failure reason and a completion watermark. Never replace an approved catalog view with a partially received version without a deliberate policy.

## Settings, Favorites and Claim Readiness

The settings schema is strict, while the service normalizes legacy settings with defaults: enabled and autoSuggest unless explicitly false, provider internal, preferred system ICD-10. The update method accepts a typed patch; runtime schema enforcement must be verified at the controller/input boundary, not inferred from its TypeScript type.

Favorites, common-code lists and uncoded-visit views support clinical workflow. Their ownership and effective feature gating need tenant/doctor scope. Coding identifiers present on a record can satisfy the local claims gate, but do not establish that those codes are correct, current or accepted by the recipient.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Strengths | Shared release predicate, clinic-qualified repository operations, provider ports, separate cooldowns and incremental sync make mechanisms explicit. |
| Limitations | Release can race or complete without notification; manual paidAt is not financial reconciliation; provider fallback changes semantics; swallowed stream failure can resemble completion. |
| Recommended lab design | Atomically authorize one release/version under current state, commit required notification work with it, and track attempt/delivery separately; offer scoped retrieval and safe resend without reopening clinical state. |
| Recommended catalog design | Store system/source/version identity, enforce validated configuration and visible fallback, checkpoint sync and publish only defined completed coverage; preserve historical coded facts. |
| Acceptance evidence | Concurrent release creates one authorized state effect and recoverable notification; cancellation blocks stale release; partial sync is visibly incomplete; different code systems never silently collide. |

These are proposals, not shipped guarantees or clinical validation. Link payments to authoritative billing evidence when that is the intended release prerequisite, and let the responsible clinical policy define urgent-access behavior.

## Mistakes and Best Practices

Avoid zero-leakage claims, invented outage incidents and complete-catalog assertions. Measure coverage and freshness. Test both prerequisite orderings plus concurrency, tenant access, provider capability, timeout/cooldown, malformed responses, cursor repetition, fallback mixing and replayed batches.

## Code Evidence

Paths are in the inspected Docita checkout.

| Mechanism | Source path |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Eligibility predicate | `apps/api/src/domains/clinical/core/entities/lab-order.entity.ts` |
| Send and completion order | `apps/api/src/domains/clinical/application/services/lab-workflow-command.service.ts` |
| Release predicate in writes | `apps/api/src/domains/clinical/infrastructure/persistence/prisma-lab.repository.ts` — markReleased |
| Batch synchronization | `apps/api/src/domains/clinical/application/services/medical-code-sync.service.ts` |
| Source routing and fallback | `apps/api/src/domains/clinical/infrastructure/external/composite-code-catalog.provider.ts` and `licensed-cpt-code-catalog.provider.ts` |
| Cooldown and prefix streaming | `apps/api/src/domains/clinical/infrastructure/external/nlm-coding.client.ts` |
| Settings normalization | `apps/api/src/domains/clinical/application/services/clinical-settings.service.ts` |

## Summary

Separate lab eligibility, atomic release and notification completion. For medical catalogs, preserve system/source/version and distinguish complete synchronization from partial success. Local flags and generic storage models cannot establish clinical, financial or interoperability correctness on their own.

## See Also

- [Category revision](REVISION.md) — lab and catalog questions.
- [WhatsApp integration](06-whatsapp-integration.md) — send and delivery boundaries.
- [Insurance claims](11-insurance-claims.md) — local coding-readiness checks.
- [Documents and uploads](19-documents-and-uploads.md) — URL capability and access.
- [Case-study index](INDEX.md) — reading order.

## References

- [NLM HCPCS API](https://clinicaltables.nlm.nih.gov/apidoc/hcpcs/v3/doc.html) — Level II data identity and pagination limits.
