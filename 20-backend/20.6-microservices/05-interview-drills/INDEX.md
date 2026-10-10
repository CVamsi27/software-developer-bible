# Interview Drills - Microservices

> **Study time:** ≈ 10 min of reading (1 files, ~10 min average).
> **1 file.** 30+ senior-level Q&A covering decomposition, communication, data, transactions, observability, and failure handling — start with a short answer, then choose one scenario for a timed design discussion.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview%20Drills-blue)](../INDEX.md)

---

## Practice after the learning passes

Complete the topology, messaging, data and resilience chapters and their revision companions first. Give a two-minute explanation, trace one timeout or duplicate, then defend a trade-off. Use a 30–45-minute session for a full system-design prompt, not for every definition.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Interview Questions](20.6.5.01-interview-questions.md) | Curated senior-level microservices Q&A | Important | Important | 10 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

The local [Docita](https://github.com/CVamsi27/docita) source inspected on 10 October 2026 provides concrete NestJS/Prisma examples. Source presence does not establish deployment, throughput or successful recovery. Walk through the code and identify what still needs runtime evidence:

| Drill | Docita evidence |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Saga / outbox drill | `apps/api/src/shared/modules/outbox/outbox.service.ts` - transaction-local event intent; explain relay retries and duplicate listener effects |
| Circuit-breaker drill | `apps/api/src/shared/common/utils/circuit-breaker.ts` - thresholds and state transitions in one small class |
| "Split the monolith" drill | `apps/api/src/app.module.ts` - candidate module seams; extraction also needs independent data ownership and release contracts |

---

[← Previous: Resilience](../04-resilience/INDEX.md)
