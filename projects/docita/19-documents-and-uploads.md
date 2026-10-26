# 19 — Files: Authorize Uploads, Persist Object Identity and Bound Access

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



Consider a doctor opening an upload link without a normal staff session. The link must grant a narrow upload capability, validate the file, associate the result with the intended record and prevent competing uploads from consuming that capability twice. Generating a secret solves only the first part.

## Definition

A file workflow connects upload permission, object storage that retains files, database records identifying each file's owner, and read permission. Docita connects these parts through an interface for storage providers, upload-session secrets, and code that resolves file URLs.

> **Textbook Definition:** A file-access workflow coordinates authorization, upload capability, object persistence and resource ownership. Object identifiers and generated links are references to stored content, not independent proof of permission.

This case describes source inspected on **2 October 2026**. Sequential checks and intended policies are distinguished from concurrent guarantees and production evidence.

## First Principles

The database and object store commit independently. A secret proves possession, not the identity or clinical authority of its holder. A presigned URL contains a signature granting a particular storage operation until expiry. Anyone holding it can use that permission; it does not recheck application roles on each request.

A correct design therefore needs explicit capability scope, atomic ownership transitions, file validation, durable object identity and recovery when a storage write and database write diverge.

## Why Put Storage Behind a Port?

`StorageProvider` exposes five operations—`upload`, `uploadBuffer`, `delete`, `generateSignedUrl` and `getObject`—and a `supportsSignedUrls` flag. Callers depend on that contract rather than constructing a storage SDK.

| Implementation | Inspected behavior | Boundary |
| -------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Local | Writes beneath an upload directory; multipart upload returns an `/uploads/...` path | Disk lifecycle and served-file permissions require separate decisions |
| R2 | Uses S3 client operations; upload returns an object key | Credentials, bucket policy and provider semantics still matter |

The module selects local storage outside production. In production it selects R2 when the provider and required configuration are present; otherwise this factory logs a warning and falls back to local storage. The warning says startup validation should block that situation, but a warning is not proof that boot was blocked.

Local storage tied to an application instance can disappear when that instance is replaced, so it is unsuitable as an automatic substitute for durable production storage. With several instances, a read can also miss files stored on another instance. Changing storage providers requires moving existing bytes, checking metadata and resolving stored identities; switching configuration alone does not migrate objects.

## How an Upload Session Grants a Narrow Capability

The create service generates **32 random bytes**, encodes the secret as base64url and stores its SHA-256 hash. It returns the plaintext secret to the caller at creation and defaults to a **15-minute** expiry. Purpose distinguishes general uploads from doctor signatures; a doctor identifier can associate the session with its target.

The upload guard requires the session ID and `X-Upload-Secret` header before multipart parsing. It loads the session and validates the hashed secret using a length check and `timingSafeEqual`, then checks expiry and prior use. The service validates again before uploading.

```text
authorized issuance → session ID + secret → guard checks capability
  → parse and validate file → write object → update session record
```

A random, high-entropy secret hashed at rest prevents the hash itself from serving as the bearer secret. It does not make the database reveal no information, protect a leaked plaintext link, or authenticate the real-world doctor. Protect issuance, delivery, logs and referrer exposure, and bind the capability to its intended operation.

### Readiness Checks Do Not Make Consumption Atomic

The inspected `updateSession` loads and validates the session, uploads the object, then performs `updateMany` with a predicate containing only the session ID. It does not atomically claim a still-unused session before the object write.

A source-extracted probe using controlled persistence and storage reproduced this trace:

| Call A | Call B |
| ---------------------- | ----------------------------- |
| Reads unused session | Reads the same unused session |
| Passes readiness check | Passes readiness check |
| Uploads object A | Uploads object B |
| Updates session by ID | Updates session by ID |

Both calls uploaded and updated the session. This is source-level evidence of a concurrent gap, not a production exploit claim. A later sequential request is rejected by the used-status check; that is a weaker property than one concurrent consumer.

A stronger protocol atomically claims the unused, unexpired capability, identifies the owner of the claim and defines recovery if upload fails. Storage work should not be held inside a long database lock without evaluating that cost. Completion and compensation need to account for the claimed owner and object identity.

## How the Upload Endpoint Validates Bytes

The current upload controller applies a multipart size limit from `MAX_FILE_SIZE`, currently **10 MiB**, and permits JPEG, PNG, WebP and PDF MIME values. It also calls `assertAllowedFileSignature` after parsing. The old claim that the upload surface has no type or size checks is incorrect.

These checks operate at the endpoint. Purpose-specific restrictions, image dimensions, decompression/resource limits and any required malware checks are separate policies. A claimed MIME type alone is not trustworthy. The local provider resizes image uploads to fit within 2000 × 2000 without enlargement; R2's inspected upload path sends the supplied file bytes instead, so callers should not assume identical image processing.

An uploaded signature image also is not automatically a cryptographic digital signature. Keep the file's purpose and provenance separate from claims of legal or clinical validity.

## How Object Identity Becomes a Read URL

Opaque keys separate stored identity from a temporary access URL. The resolver signs object keys when the provider supports signing and builds API URLs for local paths. It also passes existing absolute HTTP(S), data and blob values through for compatibility.

The implementation therefore supports mixed legacy forms; “the database never stores URLs” is too strong. A key remains useful across a provider migration only if the corresponding object is moved and the new resolver addresses it correctly. A local path and an R2 object key are not automatically interchangeable.

### The Application TTL Policy

| Setting | Inspected value | Scope |
| ----------------------- | --------------- | --------------------------------------------------------------- |
| Minimum signed TTL | 30 seconds | Positive finite requested values are clamped to the policy band |
| Maximum signed TTL | 24 hours | Application policy, not the provider's maximum |
| Generated PDF TTL | 15 minutes | Shared PDF URL helper |
| Generic stored-file TTL | 4 hours | Generic resolver for signable object keys |

R2's presigner creates a GET capability. Such URLs can be reused until expiry by anyone who possesses them; application authorization should precede issuing one. Expiry limits future access under the signature, not copies already downloaded. [R2 presigned URL documentation](https://developers.cloudflare.com/r2/api/s3/presigned-urls/).

The local provider reports `supportsSignedUrls = false`; its method named `generateSignedUrl` validates the requested TTL but returns a public upload URL. That returned URL is not cryptographically expiring. A caller must respect the capability distinction rather than assuming the method name supplies identical protection in every environment.

Deleting an object can prevent subsequent origin retrieval of that object; it does not erase cached or downloaded copies. Invalidating one already-issued capability without affecting others requires a deliberate access architecture. Do not claim a deleted object remains downloadable merely because its URL has not expired.

## How Generated PDFs and Metadata Fit the Same Workflow

Workers call `uploadBuffer` because the generated PDF is already bytes in memory. They persist its returned object identity and use the shared PDF URL helper. Both the worker and human upload paths use the port, but their file-validation and memory profiles differ: `getObject` returns a fully buffered object in both inspected implementations.

A crash after object upload but before database persistence can leave an orphan. A database record without accessible bytes is the opposite inconsistency. Cleanup requires an age/ownership-aware reconciliation process so it does not delete an in-flight valid upload.

The upload service supplies provenance such as session ID, purpose, actor, time and request context. R2 normalizes metadata keys to lowercase with replacement/length limits and truncates values; the local provider ignores upload metadata. Metadata can be sensitive and is not equivalent to a protected, append-only audit log.

## Real-World Decisions

| Requirement | Mechanism to evaluate | Remaining boundary |
| ------------------------------ | ------------------------------------------------ | ----------------------------------------------------------------- |
| Upload without a staff session | Narrow, expiring bearer capability | Authorized issuance, delivery and target binding |
| Exactly one concurrent upload | Atomic claim with owner-aware completion | Recovery and orphan cleanup |
| Sensitive document download | Authorized URL issuance or authenticated proxy | Bearer sharing, caches and downloaded copies |
| Provider migration | Stable object identity plus byte migration | Legacy paths, metadata and access-policy differences |
| Large files | Bounded processing or streaming where supported | Provider and proxy memory behavior |
| Document-read audit | Explicit authorized read paths and audit records | Signed-URL origin downloads may bypass the application controller |

The inspected document controller logs patient or clinic list reads; template access combines tier, role and feature decorators. This establishes behavior on those controller paths, not that every object download passes through them. If read auditing moves asynchronously, preserve the required durable audit responsibility rather than assuming a best-effort queue is equivalent.

## Mistakes

- Describing separate validation and update steps as atomic single-use consumption.
- Treating a short TTL as complete authorization or guaranteed harmless leakage.
- Assuming local and R2 providers have identical URL, metadata or processing semantics.
- Switching providers without migrating stored bytes.
- Claiming controller audit logging covers direct signed-URL downloads.
- Inferring incident-free production behavior from source tests or comments.

## Best Practices

Test simultaneous consumption, exact expiry boundaries, missing and invalid secrets, type/signature mismatch, size limits and failure between object and database writes. Verify sensitive reads and URL issuance per tenant. Document provider differences and fail closed when durable production storage is unavailable. Observe orphan recovery and access/audit paths with representative objects, keeping secrets and sensitive metadata out of logs.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Storage ports, file signatures, scoped token records and key resolution support multiple providers. |
| Current limitations | Token consumption is not atomic, provider access semantics differ, and upload/metadata failures can leave orphans. |
| Recommended design | Atomically claim upload capability, validate bounded bytes, quarantine until metadata is committed, authorize reads before short-lived access, and reconcile owned orphan objects with version-aware cleanup. |
| Evidence needed | Concurrent use of one capability yields one accepted upload; unsupported files fail; cross-tenant reads are denied; failed metadata persistence leaves recoverable quarantine rather than a published orphan. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

A file workflow needs more than storage and a secret: it must connect authorized capability issuance, atomic ownership, validated bytes, durable object identity and controlled reads. Docita supplies useful components, while its current upload sequence and provider differences limit the guarantees that can accurately be claimed.

## See Also

- [Category revision](REVISION.md) — questions after the case studies.
- [Async processing](03-async-processing.md) — worker crash and retry boundaries.
- [Tenant isolation](02-multi-tenancy-rls.md) — authorized database access.
- [Deployment](10-deployment-infrastructure.md) — proxy buffering and storage configuration.
- [Case-study index](INDEX.md) — reading stages.

## References

- [Cloudflare R2 presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/).

Docita source inspected on 2 October 2026:

- `apps/api/src/domains/documents/application/ports/storage-provider.port.ts`
- `apps/api/src/domains/documents/documents.module.ts`
- `apps/api/src/domains/documents/infrastructure/local-storage.provider.ts` and `r2-storage.provider.ts`
- `apps/api/src/domains/documents/application/services/uploads-command.service.ts` and `uploads-session.helpers.ts`
- `apps/api/src/domains/documents/application/services/stored-file-url-resolver.service.ts`
- `apps/api/src/domains/documents/presentation/guards/upload-session-secret.guard.ts`
- `apps/api/src/domains/documents/presentation/controllers/uploads.controller.ts` and `documents.controller.ts`
- `apps/api/src/shared/modules/document-generation/pdf/pdf-url.helpers.ts`
