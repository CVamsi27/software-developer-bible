# 20 — Documents, Uploads & Storage

> The storage abstraction under every file Docita touches — patient documents, doctor signatures, prescription/PDF outputs — with single-use upload sessions, a local-vs-R2 provider switch chosen by environment, and signed URLs whose lifetimes encode the sensitivity of what they expose.

---

## Context

Docita stores many kinds of files, with very different sensitivity and lifetime needs:

- **Patient medical documents** (reports, scans) — PHI, viewed repeatedly by clinic staff.
- **Doctor signatures** — legally significant (prescriptions require a digital signature), uploaded once.
- **Generated clinical PDFs** (prescriptions, lab reports) — PHI created by Docita itself, fetched briefly by the patient.
- **Clinic templates** (letterheads, Rx layouts) — less sensitive, edited often.

**The problems:** (1) production object storage (Cloudflare R2) costs money and needs credentials, while every local dev/CI run still needs working uploads — so storage must be *swappable by environment*; (2) an upload endpoint reachable without a login is a spam/abuse hole, but the doctor-signature flow happens *outside* a normal staff session (a doctor clicks an emailed link) — so there must be a bearer capability that isn't a user session; (3) the DB should store opaque object keys, never absolute URLs, because the URL scheme changes when you switch providers; (4) every URL handed to a browser must not outlive its purpose — a 15-minute clinical-PDF link is a very different risk from a profile photo.

---

## Decision 1: A StorageProvider Port + Environment-Driven Factory

### What We Chose

An abstract `StorageProvider` port defines five operations: `upload(file)`, `uploadBuffer(buffer)`, `delete(key)`, `generateSignedUrl(key, ttl)`, `getObject(key)`, plus the capability flag `supportsSignedUrls`. Two implementations exist — `LocalStorageProvider` (writes to `/uploads/...` served by the API) and `R2StorageProvider` (S3-compatible Cloudflare R2). The Nest module chooses by environment:

```typescript
// documents.module.ts
const isProduction = configService.isProduction();
if (!isProduction) return new LocalStorageProvider({ apiUrl });
if (provider === 'r2' && hasR2Credentials) return new R2StorageProvider(r2Config, clock);
logger.warn('R2 not fully configured; falling back to local provider...');
return new LocalStorageProvider({ apiUrl });
```

### Why This Was Chosen

- **Local dev/CI needs zero cloud credentials** — every developer, every test run, and the preview environment upload files to local disk; only production (with R2 env vars present) hits real object storage.
- **Production falls back loudly, not silently** — a misconfigured prod boots with a warning that startup validation *should* have blocked, rather than failing on first upload.
- **The R2 client is straight S3** (`S3Client` + `PutObjectCommand`/`DeleteObjectCommand` + presigner) — Docita gets Cloudflare's zero-egress-cost storage without learning a second SDK; swapping to AWS S3 later is a config change, not a code change.

### Trade-offs

- **Two providers to keep in sync** — every new port method (e.g., `uploadBuffer` for raw PDF bytes) must be implemented twice; specs for both (`local-storage.provider.spec.ts`, `r2-storage.provider.spec.ts`) pin the contract.
- **Local storage is not durable** — it lives on the API instance's disk, which is fine for a single dev box but would be wrong for a multi-instance deploy; the production path *must* be R2, and the warning comment admits the fallback risk.
- **Metadata normalization differs** — R2 metadata has strict key/value rules (lowercase, length caps), so the R2 provider normalizes keys (`[a-z0-9-_]`, ≤128 chars) and values (stringified, ≤512) while local storage ignores most of it; a metadata consumer can't rely on identical behavior across providers.

---

## Decision 2: Upload Sessions = Single-Use Bearer Capabilities

### What We Chose

Uploads don't go through normal auth. Instead, `UploadsCommandService.createSession` mints an **upload session**:

- A 32-byte random plaintext secret (`randomBytes(32).toString('base64url')`) — *returned once* to the caller.
- Only its SHA-256 hash is stored on the session row.
- Sessions expire (default 15 minutes) and carry a `purpose` (`GENERAL` | `DOCTOR_SIGNATURE`).

Uploading (`POST /uploads/session/:id`) is guarded by `UploadSessionSecretGuard`, which requires the secret in the `X-Upload-Secret` header and calls `assertReadyForUpload`:

```typescript
// uploads-session.helpers.ts
if (expected.length !== candidate.length || !timingSafeEqual(expected, candidate)) {
  throw new UnauthorizedException('Invalid upload credentials');
}
// validateSessionReadyForUpload additionally rejects:
if (session.expiresAt < now) throw BadRequestException('This upload link has expired');
if (session.status === 'uploaded' || session.fileUrl) throw BadRequestException('This upload link has already been used');
```

After a successful upload the session flips to `uploaded` — it can never be used again — and the file's object metadata records *who* (or what) uploaded it (`modified_by`, `modified_by_role`, `auth_method`, `auth_ip`, `auth_user_agent`) for audit.

### Why This Was Chosen

- **Bearer capability, not user session** — a doctor clicking an emailed signature link has no staff session, but the emailed link + one-time secret is exactly the right capability for "upload exactly one signature."
- **Hashed at rest, compared in constant time** — a DB read of the sessions table leaks nothing usable (SHA-256, not plaintext), and `timingSafeEqual` prevents timing attacks on the secret comparison.
- **Single-use + expiry bound the blast radius** — a leaked `X-Upload-Secret` is worthless after the session is used or its 15 minutes pass.
- **Upload provenance is embedded in the object** — storage metadata answers "who uploaded this and from where" even after the session row is long gone, feeding the same audit instinct as every other PHI write.

### Trade-offs

- **The secret is shown once** — if the caller loses it (page refresh, copied link truncated), they must mint a new session; there's no recovery, by design.
- **Session rows are write-amplified** — create + validate + upload + status flip is four DB interactions per file; negligible at clinic volume.
- **Secret lives in the URL or header** — a link-shared session URL is bearer-capable until expiry; the 15-minute window keeps that acceptable, but sessions are not for long-lived sharing.

---

## Decision 3: Opaque Keys in the DB, URLs Resolved at Read Time

### What We Chose

The database stores **object keys**, not absolute URLs, and a `StoredFileUrlResolverService` decides how to turn a key into a browser-ready URL *at read time*:

- Local path (`/uploads/...` or relative) → absolute API URL (`toAbsoluteApiUrl`).
- Object key + provider supports signed URLs → `generateSignedUrl(key, GENERIC_STORED_FILE_SIGNED_URL_TTL_SECONDS = 4h)`.
- Object key + local provider → API-served `/uploads/{key}`.
- Already-absolute HTTP(S) or `data:`/`blob:` values pass through untouched (legacy rows).

```typescript
// stored-file-url-resolver.service.ts
if (this.storageProvider.supportsSignedUrls) {
  return { url: await this.storageProvider.generateSignedUrl(trimmed, GENERIC_STORED_FILE_SIGNED_URL_TTL_SECONDS), storedUrl: trimmed };
}
return { url: this.toAbsoluteApiUrl(`/uploads/${trimmed}`), storedUrl: trimmed };
```

### Why This Was Chosen

- **Provider switches don't invalidate stored data** — because rows hold keys (`prescriptions/{uuid}.pdf`), migrating from local to R2 (or R2 to S3) requires no data rewrite; only the resolver's behavior changes.
- **TTL policy is centralized and explicit** — the port file declares the whole lifetime band: `MIN 30s`, `MAX 24h` (tighter than R2/S3's 7-day max), generated clinical PDFs get **15 minutes** (`GENERATED_PDF_SIGNED_URL_TTL_SECONDS`), generic private uploads 4 hours. A request for a longer URL is silently clamped, not honored.
- **Legacy absolute URLs keep working** — old rows and third-party URLs don't need a migration.

### Trade-offs

- **Every read is a resolution decision** — cheap branching, but the resolver must know the provider's capability; a local-provider deployment resolving an R2-era key would serve a wrong URL. Realistically environments don't mix, so the risk is theoretical.
- **Signed URL ≠ authorization** — any bearer of the URL can fetch within the TTL; the 15-minute clinical-PDF lifetime is the mitigation, and the resolver doesn't add per-patient checks on top of the URL itself.

---

## Decision 4: Generated PDFs Go Through the Same Port (Buffer Upload + Short TTL)

### What We Chose

The PDF pipeline (prescription/lab PDFs generated by queue workers) uses `uploadBuffer(buffer, objectKey, contentType)` to push bytes straight to storage without a multipart round-trip, then signs a URL for exactly 15 minutes via a shared helper (`generatePdfSignedUrl` → `GENERATED_PDF_SIGNED_URL_TTL_SECONDS`). The same `StorageProvider` port is injected in the worker modules (`queue/pdf-job.service.ts`, clinical lab workflow), so a locally-generated PDF in dev lands on disk and in prod lands in R2 with identical calling code.

### Why This Was Chosen

- **Workers don't do multipart** — the PDF is already a `Buffer` in memory; `uploadBuffer` avoids faking a file object through Multer.
- **One storage contract for human uploads and machine writes** — the port is the single seam; signature uploads (`doctors` domain), patient document uploads, and queue-generated PDFs all speak the same five methods.
- **15-minute TTL is a deliberate PHI decision** — a prescription PDF link in a WhatsApp message must survive a patient opening it shortly after delivery, but shouldn't be bookmarkable for a week. The comment in the port file says exactly this: "Generated clinical PDFs contain PHI, so keep their bearer lifetime short."

### Trade-offs

- **`uploadBuffer` returns the key** and the caller persists it — a worker crash between upload and DB write orphans an object in storage; no garbage-collection job exists yet for orphaned keys.
- **Short TTLs trade convenience for safety** — a patient who opens the link a day later gets a 403 and must re-request the PDF; acceptable for PHI, mildly annoying in practice.

---

## Decision 5: PHI Reads Are Audited at the Controller Boundary

### What We Chose

The read surface for patient documents (`documents.controller.ts`) sits behind tier + role + feature guards and explicitly logs PHI reads *before* returning data — patient-scoped reads log `VIEW_HISTORY` on the patient; unscoped list reads log a clinic-level PHI list read (`logPatientPhiRead` / `logClinicPhiListRead` from the shared audit utils). Templates (`templates.controller.ts`) are role-gated (`ADMIN/DOCTOR/RECEPTIONIST/ADMIN_DOCTOR`) and feature-gated (`PRESCRIPTION_TEMPLATES`) via a reusable `TemplatesApiAccess` decorator.

### Why This Was Chosen

- **Document views are PHI events** — "who looked at this patient's reports" is exactly the question regulators and patients ask; logging at the controller (the narrowest shared point) guarantees no query path bypasses the audit.
- **Reusable access decorators keep policy declarative** — `TemplatesApiAccess` bundles guard + roles + feature so a new template endpoint can't forget its gate.

### Trade-offs

- **Audit logging is synchronous** on the read path — an extra insert per document view; acceptable today, a candidate for the async queue when view volume grows.
- **Feature gating by module means cross-cutting config** — a clinic that pays for prescriptions but not medical documents gets different visibility; that's correct but adds a support-answer surface.

---

## What Worked

- **Local-first storage made development painless** — no engineer ever needed R2 credentials to run the full stack; CI uploaded to disk and tests exercised the real provider contract.
- **The upload-session guard held** — single-use + expiry meant a leaked signature-upload link was never exploitable beyond its 15-minute window, and no double-upload ever landed (the second attempt is rejected by the `uploaded` status).
- **Opaque keys paid off during the R2 rollout** — rows written under local storage needed zero migration; only the resolver behavior changed per environment.

## What Failed

- **Early absolute-URL storage was a migration tax** — rows that stored full URLs (`https://api.../uploads/...`) had to be special-cased forever in the resolver (`isAbsoluteHttpUrl` passthrough), because rewriting them would have touched PHI rows in prod. The "keys only" rule arrived after the first cohort of rows.
- **Metadata assumptions differed between providers** — an early metadata write with uppercase keys worked on local disk but was silently stripped by R2's rules; the R2 normalizer (`normalizeMetadataKey`) fixed it, and the specs now pin both sides.
- **The R2 fallback warning was initially just a log** — a prod box without credentials booted into local storage until startup validation was tightened; the warning text itself admits the gap.

## What Could Be Better

- **Orphaned-object GC** — a sweep of storage keys with no DB row (crashes between upload and persist) would close the only real leak in the pipeline.
- **Upload size/type policy at the session level** — today the guard checks secret/expiry/use but not file type or size; a session-purpose → allowed-mime map (signatures: images only) would harden the doctor flow.
- **Signed-URL revocation** — no way to revoke a not-yet-expired signed URL if a file is deleted mid-TTL; R2/S3 support this via conditional requests only with extra work.
- **Move view-audit to the async queue** when document-view volume grows past synchronous comfort.

---

## Code Evidence

| Claim | File |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Storage port + TTL band | `apps/api/src/domains/documents/application/ports/storage-provider.port.ts` |
| Provider factory (env switch) | `apps/api/src/domains/documents/documents.module.ts` |
| R2 (S3-compatible) provider | `apps/api/src/domains/documents/infrastructure/r2-storage.provider.ts` |
| Local provider | `apps/api/src/domains/documents/infrastructure/local-storage.provider.ts` |
| Upload session mint/use | `apps/api/src/domains/documents/application/services/uploads-command.service.ts` |
| Secret hash + single-use validation | `apps/api/src/domains/documents/application/services/uploads-session.helpers.ts` |
| Session guard (X-Upload-Secret) | `apps/api/src/domains/documents/presentation/guards/upload-session-secret.guard.ts` |
| URL resolution + TTL policy | `apps/api/src/domains/documents/application/services/stored-file-url-resolver.service.ts` |
| PDF signed URL helper | `apps/api/src/shared/modules/document-generation/pdf/pdf-url.helpers.ts` |
| Worker PDF upload | `apps/api/src/shared/modules/queue/pdf-job.service.ts` |
| PHI-audited document reads | `apps/api/src/domains/documents/presentation/controllers/documents.controller.ts` |
| Templates access policy | `apps/api/src/domains/documents/presentation/controllers/templates.controller.access.ts` |
| Signature upload (consumer) | `apps/api/src/domains/doctors/application/services/signature-upload.service.ts` |

---

## Interview Script (60 seconds)

> "Every file Docita touches goes through one `StorageProvider` port with two implementations — local disk and Cloudflare R2 — chosen by a module factory: non-production always uses local (zero credentials, full-stack dev works), and production uses R2 with a loud fallback if credentials are missing. Uploads don't ride normal auth: we mint single-use upload sessions — a 32-byte secret returned once, only its SHA-256 hash stored, 15-minute expiry — and the upload guard requires the secret in a header, rejects expired or already-used sessions in constant time, then flips the session to `uploaded` so it can never be reused. The DB stores opaque object keys, never URLs, and a resolver turns keys into browser URLs at read time with a centralized TTL policy — generated clinical PDFs get 15-minute signed URLs because they contain PHI, generic uploads get 4 hours, and everything is clamped to a 24-hour max. Patient document views are audited at the controller boundary as PHI events. The gap I'd close next is an orphaned-object GC for uploads that crash between the storage write and the DB persist."

---
