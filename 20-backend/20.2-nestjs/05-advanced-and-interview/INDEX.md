# Advanced & Interview - NestJS

> **Study time:** ≈ 21 min of reading (3 files, ~7 min average).
> **3 files.** Senior-level customization with parameter/method decorators and decorator composition, then the curated question bank for final review.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Advanced%20%26%20Interview-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Custom Decorators](20.2.5.01-custom-decorators.md) | Parameter decorators (@CurrentUser, @ClinicId, @Pagination), method decorators (@RateLimit, @Cache, @Audit), decorator composition | Essential | Important | 11 min |
| Revision | [Category recall](REVISION.md) | Extraction, metadata and enforcement boundaries before the interview drill | Essential | Important | — |
| 02 | [Interview Questions](20.2.5.02-interview-questions.md) | 40 practice questions with answers | Essential | Important | 8 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare application (NestJS + Prisma + PostgreSQL). Use the following paths to investigate the current checkout; these references do not establish deployment readiness:

| Topic | Docita evidence |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Custom method decorators | `apps/api/src/shared/modules/auth/decorators/require-policy.decorator.ts` - @RequirePolicy metadata consumed by PolicyGuard |
| Route metadata decorators | `apps/api/src/shared/modules/idempotency/requires-idempotency.decorator.ts` - marker drives IdempotencyInterceptor |
| Role markers | `apps/api/src/shared/modules/auth/auth/roles.decorator.ts` - @Roles read back via Reflector in RolesGuard |

Use these evidence paths to investigate decorator registration and consumption in the project. The reference examples still require checking the current checkout; they do not prove every lifecycle or transport feature ships there.
---

[← Previous: Quality & Operations](../04-quality-and-operations/INDEX.md)
