# Advanced & Interview — NestJS

> **Study time:** ≈ 16 min of reading (3 files, ~5 min average).
> **3 files.** Senior-level customization with parameter and method decorators and decorator composition, then the curated question bank for final review.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Advanced%20%26%20Interview-success)](../INDEX.md)

---

## Learning flow

First trace a parameter extractor after authentication and distinguish extraction from validation. Then attach route metadata and identify the registered guard or interceptor that consumes it. Test a missing principal and an unregistered consumer before the revision companion and interview bank.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Custom Decorators](20.2.5.01-custom-decorators.md) | Request-value extraction, metadata consumers, validation boundaries, and decorator composition | Essential | Important | 6 min |
| Revision | [Category recall](REVISION.md) | Extraction, metadata, and enforcement boundaries before the interview drill | Essential | Important | — |
| 02 | [Interview Questions](20.2.5.02-interview-questions.md) | 43 practice questions with answers | Essential | Important | 8 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real-world pointers from [docita](https://github.com/CVamsi27/docita) — healthcare platform (NestJS + Prisma + PostgreSQL):

| Topic | Docita evidence |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Custom method decorators | `apps/api/src/shared/modules/auth/decorators/require-policy.decorator.ts` — `@RequirePolicy` metadata consumed by `PolicyGuard` |
| Route metadata decorators | `apps/api/src/shared/modules/idempotency/requires-idempotency.decorator.ts` — marker drives `IdempotencyInterceptor` |
| Role markers | `apps/api/src/shared/modules/auth/auth/roles.decorator.ts` — `@Roles` read back via `Reflector` in `RolesGuard` |

Trace each custom decorator back to its registered guard or interceptor consumer in the module wiring.

---

[← Previous: Quality & Operations](../04-quality-and-operations/INDEX.md)
