# Payloads, Errors & Integration - REST APIs

> **5 files.** The contract details clients feel daily: pagination strategies (offset vs cursor vs keyset), RFC 7807 error design, long-running operations (202 Accepted + operation resources), file upload architectures (proxy multipart vs presigned direct-to-S3), and webhooks — the "reverse API".

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Payloads%20%26%20Errors-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Pagination](20.3.3.01-pagination.md) | Offset vs cursor vs keyset — deep dive | 20 min |
| 02 | [Error Handling Design](20.3.3.02-error-handling-design.md) | RFC 7807 problem details, validation errors | 15 min |
| 03 | [Long-Running API Operations](20.3.3.03-long-running-api-operations.md) | `202 Accepted` pattern, operation resource schema, polling vs webhook completion, progress & partial results, idempotent resubmission, cancellation, NestJS sketch | 25 min |
| 04 | [File Upload APIs](20.3.3.04-file-upload-apis.md) | Multipart streaming, presigned S3 direct uploads, resumable (`Content-Range`, tus), virus-scan gates, metadata sidecars, MIME sniffing + size caps | 25 min |
| 05 | [Webhooks](20.3.3.05-webhooks.md) | At-least-once delivery, HMAC signature verification, replay protection, retry with backoff, ordering + idempotency keys, DLQ | 30 min |

---

[← Back to REST APIs](../INDEX.md)
