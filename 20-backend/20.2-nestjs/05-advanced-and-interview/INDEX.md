# Advanced & Interview - NestJS

> **Study time:** ≈ 48 min of reading (2 files, ~24 min average).
> **2 files.** Senior-level customization with parameter/method decorators and decorator composition, then the curated question bank for final review.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Advanced%20%26%20Interview-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Custom Decorators](20.2.5.01-custom-decorators.md) | Parameter decorators (@CurrentUser, @ClinicId, @Pagination), method decorators (@RateLimit, @Cache, @Audit), decorator composition | 10 min |
| 02 | [Interview Questions](20.2.5.02-interview-questions.md) | 50+ curated questions with answers | 38 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Custom method decorators | `apps/api/src/shared/modules/auth/decorators/require-policy.decorator.ts` - @RequirePolicy metadata consumed by PolicyGuard |
| Route metadata decorators | `apps/api/src/shared/modules/idempotency/requires-idempotency.decorator.ts` - marker drives IdempotencyInterceptor |
| Role markers | `apps/api/src/shared/modules/auth/auth/roles.decorator.ts` - @Roles read back via Reflector in RolesGuard |

Every interview question about decorators/lifecycle is answerable from these files — walk `app.module.ts` registrations to narrate the chain end-to-end.
---

[← Previous: Quality & Operations](../04-quality-and-operations/INDEX.md)
