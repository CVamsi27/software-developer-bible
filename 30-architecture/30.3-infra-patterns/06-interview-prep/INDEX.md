# Interview Prep

> **Study time:** ≈ 7 min of reading (1 files, ~7 min average).
> **1 file.** Senior-depth Q&A over the whole stack — lifecycle contracts, retry/idempotency discipline, backup drills, coordination, scaling levers, and zero-downtime shipping — each answer naming the mechanism and the failure mode it guards.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Every pattern in this stack is a contract, and interviews test whether you can state the contract, its enforcement mechanism, and its failure mode. This file drills exactly that: readiness vs liveness, why retries need idempotency keys, RPO/RTO as drilled numbers, fencing tokens, the database-scaling lever order, blue-green vs canary — with the follow-up traps ("we do canary, do we still need blue-green?") and the scenario answers that separate operators from syntax-reciters.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Infra & Ops Patterns Interview Questions](30.3.6.01-interview-questions.md) | Probe contracts, retry+idempotency, RPO/RTO & drills, fencing tokens, scaling levers in order, blue-green vs canary, flag debt, erasure pipeline design, on-call levers, scenario drills | 7 min |

---

## Cross-References

- [Microservices Interview Drills](../../../20-backend/20.6-microservices/05-interview-drills/INDEX.md) — the distributed-patterns half of the same topics
- [Resilience & Recovery](../02-failure-and-recovery/INDEX.md) — the mechanisms behind the retry/idempotency answers
- [Shipping & Evolution](../05-shipping-and-evolution/INDEX.md) — deploy patterns and their interview questions in depth

---

## Navigation

[← Shipping & Evolution](../05-shipping-and-evolution/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md)
