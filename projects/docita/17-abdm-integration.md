# 17 — ABDM Ledger, Callback Trust and Data Exchange

## Definition

The ABDM integration connects local patient identity and care-context records to external health-information workflows. Its current source includes local care contexts, consent requests, callback recording, a gateway client and an operational inbox. That is not evidence of a complete certified interoperability flow.

The concrete question is whether a received callback is authorized to change consent state or trigger an external push—not merely whether it names an existing care context.

## First Principles

Correlation identifies the operation an event claims to describe. Authentication establishes who sent it. Authorization determines whether that sender and operation may perform the requested change. Consent scope and encryption establish additional data-sharing conditions. These checks cannot substitute for one another.

External calls and database writes are separate commits. An HTTP success, a ledger row and a receiver's valid acceptance each prove different facts. Required recovery needs durable operation identity and state transitions, not just a list of failures.

## Why a Ledger Helps

Transactions retain type, direction, status and available request, transaction and correlation IDs. The inbox queries retryable/failed transactions, pending consent requests and recent external records. This supports diagnosis across process restarts.

The ledger uses more than a simple success/failure vocabulary: inbound callback recording uses ACKNOWLEDGED and local context generation uses INTERNAL direction. Fields are not populated identically on every path. A recorded RETRYABLE status does not schedule or complete a retry automatically.

Care contexts use stable source-derived references. Creation checks clinic enablement, a verified ABHA patient, and source ownership, then obtains a patient FHIR bundle and stores the context. Source-specific permission and data minimization still matter: creating a context for one record must not imply consent to share the patient's entire available bundle.

## How Link, Share and Consent Requests Differ

The link/share helper creates an outbound ledger transaction and changes local context status to LINK_REQUESTED or SHARE_REQUESTED. It checks the global integration enabled flag, not complete gateway configuration, and the inspected method does not dispatch a link/share HTTP request itself.

Consent creation checks the patient's verified ABHA address, generates a request ID, stores the consent request, and calls the configured gateway consent method when configured. It then records dispatch outcome. Those steps are separate writes/calls, so failures can leave partial operation evidence.

When unconfigured, consent dispatch is recorded RETRYABLE. That is useful visibility, but production misconfiguration needs alerting and a defined retry owner. Local context creation can also fail validation or storage; it does not always succeed just because it avoids a gateway call.

The gateway's older verifyAbha method is explicitly marked as a deprecated path in source. A separate ABHA client contains the newer identity flow. Verify which controller/service path is wired before presenting a legacy method as the complete current integration.

## Examples: Authenticated Callback Is Not Completed Consent Validation

The callback command already invokes a shared webhook verifier with a configured shared-secret header, raw body and optional timestamp. It rejects failed verification and treats replay rejection separately. The old documentation's statement that callback authentication was entirely TODO was incorrect.

This is shared-secret authentication, not proof of verification against published asymmetric gateway keys. Inspect the verifier's replay-store, timestamp and failure policies independently; do not infer them from the parameter names.

```text
Callback ingress → configured authentication/replay check
                                      ↓
                         record inbound transaction
                                      ↓
                       optional external-record write
                                      ↓
                         consent/link state handling
                                      ↓
                       optional outbound data push
```

The exchange records a callback before state handling. If patient ID, health-information type and JSON payload exist, it can create a new external-record row. Thus callbacks are not limited to updating known ledger rows, and JSON shape validation is not FHIR or ownership validation.

Consent handling looks up clinic-scoped request/consent identity and maps a small success-word set to GRANTED; other statuses become FAILED. It retains raw artifact data. This loses distinctions such as denied, expired or revoked unless handled elsewhere, and it does not itself validate a complete consent artifact's scope, time window, recipient or permitted data.

Link handling looks up care-context reference within the clinic and marks it linked on a success-looking status. A match is useful correlation, not proof of a valid permitted link.

## What the Current Push Path Actually Sends

Whenever callback dataPushUrl and care-context reference are present, state handling can dispatch a push. That branch is not conditioned on the success-word check or an explicit GRANTED, unexpired, unrevoked consent in this method.

If the context is missing, it records a failed outbound transaction. Otherwise it passes callback payload as encryptionMaterial to the gateway. The gateway requires an object containing encryptedContent, checksum and keyMaterial, then posts those supplied values with context reference and media label.

This path does not demonstrate deriving encryption material, encrypting the stored FHIR bundle or verifying that supplied ciphertext represents the authorized local records. The media label does not validate a FHIR document. The source's stored bundle and its outbound supplied-content path must not be described as one proved encrypted transformation.

The external URL helper requires HTTPS and rejects obvious local/literal-IP destinations. This call supplies no participant-origin allowlist. The helper itself documents that it does not defeat DNS rebinding, and redirect/egress behavior needs separate enforcement. A callback-selected URL is therefore a sensitive trust boundary, not an arbitrary destination to accept merely because it parses.

A successful HTTP response maps to SUCCEEDED, even if the response body provides no transaction ID. The service then marks context shared and sends a notification, recording each outcome separately. Receiver semantic validation and an end-to-end accepted clinical exchange remain unverified.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Tenant-qualified source checks, explicit integration enablement, retained operation records, existing callback authentication and failed-context evidence support investigation. |
| Limitations | Some link/share paths only record intent; callback status normalization is coarse; external record creation and pushes need stronger consent/ownership checks; ciphertext is supplied rather than demonstrated as locally generated. |
| Recommended trust boundary | Authenticate according to the actual gateway contract, correlate a unique operation, validate tenant/patient/participant and consent artifact scope, then reject expired/revoked or out-of-order transitions. |
| Recommended exchange | Snapshot only authorized records, validate the required FHIR profile, encrypt that snapshot through the negotiated protocol, and constrain destination/DNS/redirect/egress behavior to trusted participants. |
| Recommended durability | Use a durable inbound inbox and outbound jobs with operation identity, bounded retries, fencing and evidence of both transport and semantic acceptance. |
| Acceptance evidence | Wrong-clinic/unknown/replayed callbacks cannot change records; revoked consent prevents new dispatch; supplied URLs cannot reach unauthorized destinations; the receiver decrypts and validates the exact authorized bundle in a sandbox contract test. |

These are recommended requirements, not an implemented or certified production claim. Keep provider-side and requester-side responsibilities explicit; a consent request endpoint alone does not establish a complete role implementation.

## Mistakes and Best Practices

- Treating correlation as authentication or consent: verify each independently.
- Treating generic JSON as valid health data: use profile validation and authorized resource scope.
- Treating encrypted-looking fields as encryption evidence: prove the transformation from approved local data to receiver-decryptable content.
- Treating an inbox as a retry worker: record owner, due time, attempt and completion evidence.
- Persisting raw callbacks without minimization: protect retained sensitive payloads and define retention/access policies.

Test failure between every persistence/dispatch step, duplicate and reordered callbacks, mismatched patient/context, missing configuration, consent expiry/revocation, invalid artifacts, forbidden egress and receiver validation. Source inspection alone cannot support claims of completed certification, successful clinical exchange or production reliability.

## Code Evidence

Paths are in the inspected Docita checkout.

| Mechanism | Source path |
| ------------------------------------------------ | --------------------------------------------------------------------------------- |
| Context, request and inbox orchestration | `apps/api/src/domains/abdm/application/services/abdm-exchange.service.ts` |
| Callback authentication entry | `apps/api/src/domains/abdm/application/services/abdm-callback-command.service.ts` |
| Callback state and push branch | `apps/api/src/domains/abdm/application/services/abdm-callback-state.service.ts` |
| Gateway transport and supplied content | `apps/api/src/domains/abdm/infrastructure/abdm-gateway.client.ts` |
| Consent lookup, callback/external record storage | `apps/api/src/domains/abdm/infrastructure/repositories/prisma-abdm.repository.ts` |
| URL shape restrictions | `apps/api/src/shared/common/http/safe-external-url.ts` |

## Summary

The ledger provides operational evidence, while authentication, correlation, consent, authorized data preparation, encryption and receiver validation provide distinct exchange guarantees. Describe implemented branches exactly and prove the full protocol before claiming complete interoperability.

## See Also

- [Category revision](REVISION.md) — callback trust and exchange questions.
- [Async processing](03-async-processing.md) — durable ingress and outbound jobs.
- [Patient portal](16-patient-portal.md) — patient identity boundaries.
- [Documents and uploads](19-documents-and-uploads.md) — sensitive object access.
- [Case-study index](INDEX.md) — reading order.
