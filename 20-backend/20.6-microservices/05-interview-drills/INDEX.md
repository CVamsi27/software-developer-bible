# Interview Drills - Microservices

> **Study time:** ≈ 1 h 6 m of reading (1 files, ~66 min average).
> **1 file.** 30+ senior-level Q&A covering decomposition, communication, data, transactions, observability, and failure handling — each answerable in 30-45 minutes with trade-offs and an architecture diagram.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview%20Drills-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Interview Questions](20.6.5.01-interview-questions.md) | Curated senior-level microservices Q&A | Important | Important | 66 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the drills, then cite real answers:

| Drill | Docita evidence |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Saga / outbox drill | `apps/api/src/shared/modules/outbox/outbox.service.ts` - a production outbox you can walk through |
| Circuit-breaker drill | `apps/api/src/shared/common/utils/circuit-breaker.ts` - thresholds and state transitions in one small class |
| "Split the monolith" drill | `apps/api/src/app.module.ts` - module seams are the future service boundaries |

---

[← Previous: Resilience](../04-resilience/INDEX.md)
