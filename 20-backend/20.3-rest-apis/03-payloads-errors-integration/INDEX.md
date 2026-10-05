# Payloads, Errors & Integration - REST APIs

> **Study time:** ≈ 2 h of reading (8 files, ~15 min average).
> **8 files.** The contract details clients feel daily: pagination strategies (offset vs cursor vs keyset), RFC 9457 Problem Details, long-running operations (202 Accepted + operation resources), file upload architectures (proxy multipart vs presigned direct-to-S3), webhooks — the "reverse API" — plus the two contracts everyone forgets: **serialization & wire formats** and **transactional email delivery**.

[![Files](https://img.shields.io/badge/files-8-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Payloads%20%26%20Errors-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Pagination](20.3.3.01-pagination.md) | Offset vs cursor vs keyset — deep dive | Essential | Foundational | 30 min |
| 02 | [Error Handling Design](20.3.3.02-error-handling-design.md) | RFC 9457 Problem Details, validation errors | Essential | Foundational | 11 min |
| 03 | [Long-Running API Operations](20.3.3.03-long-running-api-operations.md) | `202 Accepted` pattern, operation resource schema, polling vs webhook completion, progress & partial results, idempotent resubmission, cancellation, NestJS sketch | Essential | Foundational | 14 min |
| 04 | [File Upload APIs](20.3.3.04-file-upload-apis.md) | Multipart streaming, presigned S3 direct uploads, resumable (`Content-Range`, tus), virus-scan gates, metadata sidecars, MIME sniffing + size caps | Essential | Foundational | 15 min |
| 05 | [Webhooks](20.3.3.05-webhooks.md) | At-least-once delivery, HMAC signature verification, replay protection, retry with backoff, ordering + idempotency keys, DLQ | Important | Important | 23 min |
| 06 | [Serialization & Wire Formats](20.3.3.06-serialization-and-wire-formats.md) | JSON limits (64-bit precision, dates, undefined), protobuf field-number contracts, MessagePack/CBOR/Avro, schema evolution, body limits before parsing, compressed-size comparison | Essential | Foundational | 11 min |
| 07 | [Transactional Email & Notification Delivery](20.3.3.07-transactional-email-and-notifications.md) | Outbox → queue → worker pipeline, idempotency keys from business events, SPF/DKIM/DMARC, bounce + complaint webhooks, suppression lists, deliverability metrics | Essential | Foundational | 13 min |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Pagination | `apps/api/src/shared/common/pagination.helper.ts` - `paginateWithCursor()` keyset helper feeding repositories |
| Error design | `apps/api/src/shared/common/errors/forbidden-problem.ts` - problem-details-style payloads reused across guards and filters |
| Long-running operations | `apps/api/src/shared/modules/queue/pdf-job.service.ts` - enqueue-then-poll PDF jobs with status + signed URL |
| File upload APIs | `apps/api/src/shared/common/utils/upload.utils.ts` - multer disk storage staged behind MIME/extension checks |
| Webhooks (ingress) | `apps/api/src/shared/modules/webhooks/razorpay-webhook-verification.helper.ts` - HMAC signature check + replay dedupe |
| Webhooks (egress) | `apps/api/src/shared/modules/webhooks/outgoing/outgoing-webhook.service.ts` - HMAC-signed deliveries with 5s→300s backoff cap |
---

[← Previous: HTTP Mechanics](../02-http-mechanics/INDEX.md) · [Next: Edge & Scale →](../04-edge-and-scale/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
