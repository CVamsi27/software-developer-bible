# Interview Prep

> **Study time:** ≈ 6 min of reading (1 file, ~6 min average).
> **1 file.** Senior-depth Q&A over the whole stack — lifecycle contracts, retry/idempotency discipline, backup drills, coordination, scaling levers, and zero-downtime shipping — each answer naming the mechanism and the failure mode it guards.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

For each pattern, state what it promises, which mechanism enforces that promise, and when it can fail. Practice readiness versus liveness, retry safety with idempotency keys, measured backup recovery, ownership checks using fencing tokens, database scaling choices, and blue-green versus canary deployments. Use the follow-up questions, such as “we do canary, do we still need blue-green?”, to explain operating decisions as well as syntax.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Infra & Ops Patterns Interview Questions](30.3.6.01-interview-questions.md) | Probe contracts, retry+idempotency, RPO/RTO & drills, fencing tokens, measured scaling levers, blue-green vs canary, flag debt, erasure pipeline design, on-call levers, scenario drills | Important | Specialized | 6 min |

---

## Practice Path

Complete each learning category and its REVISION companion first. Then answer the bank aloud: name the authority, trace the uncertain/crash boundary, and change one condition before comparing alternatives. Practice scenarios are prompts; use only incidents/results you can substantiate as personal experience.

## Cross-References

- [Microservices Interview Drills](../../../20-backend/20.6-microservices/05-interview-drills/INDEX.md) — the distributed-patterns half of the same topics
- [Resilience & Recovery](../02-failure-and-recovery/INDEX.md) — the mechanisms behind the retry/idempotency answers
- [Shipping & Evolution](../05-shipping-and-evolution/INDEX.md) — deploy patterns and their interview questions in depth

---

## Navigation

[← Shipping & Evolution](../05-shipping-and-evolution/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md)
