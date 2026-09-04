# Interview Drills - REST APIs

> **1 file.** Curated Q&A to close the loop on the full REST/API stack.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview%20Drills-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Interview Questions](20.3.5.01-interview-questions.md) | Curated Q&A across design, HTTP mechanics, payloads/errors, edge and scale | 2 hrs |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the drills, then cite real answers:

| Drill | Docita evidence |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| "Offset vs cursor pagination?" | `apps/api/src/shared/common/pagination.helper.ts` - keyset implementation to walk through |
| "Make POST retries safe" | `apps/api/src/shared/modules/idempotency/idempotency.interceptor.ts` - header-driven replay window |
| "Design webhook delivery" | `apps/api/src/shared/modules/webhooks/outgoing/outgoing-webhook.service.ts` - signing + retry/backoff in one service |
---

[← Previous: ../04 Edge And Scale/index](../04-edge-and-scale/INDEX.md)
