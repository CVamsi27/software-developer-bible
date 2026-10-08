# Testing Interview Prep

> **Study time:** ≈ 11 min of reading (1 files, ~11 min average).
> **1 file.** The curated question bank for testing rounds — grouped by difficulty, covering strategy, pyramid trade-offs, async/component testing, mocking, and flaky-test debugging.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Contents | Time | Role priority | General importance |
| --: | ------ | ---------- | ------ | --- | --- |
| 01 | [Testing Interview Questions](50.1.6.01-interview-questions.md) | Forty original questions, model answers and changed-condition probes | Practice in several sessions | Essential | Foundational |

---

## First pass: explain the contract and evidence

Complete the preceding [testing learning flow](../INDEX.md) and each category's revision companion. Answer the bank's fundamentals and execution questions aloud, then check the model: what behavior runs, what result is expected and what does the test omit? Return to the canonical example when the boundary is unclear.

## Second pass: change a consequential condition

Use each probe to vary time, ownership, a failure outcome, a version or an assumption. For release and scale questions, name the required evidence, missing coverage and exception owner. For experience questions, prepare a supported personal example with your contribution and limitations; no model answer supplies that history.

## Revisit the gaps

Record questions whose reasoning you could not reproduce. After a delay, answer those again without the model. Continue until you can explain the trace and a changed condition, rather than repeating a memorized tool list.

## Cross-References

- [Coding Patterns interview bank](../../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — the algorithmic counterpart.
- [Accessibility testing questions](../../50.2-accessibility/50.2.08-testing-a11y.md) — a11y overlaps QA rounds.

---

## Navigation

[← Advanced](../05-advanced/INDEX.md) · [↑ Testing Home](../INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) supplies artifacts for inspection. Verify their current contents, test results and your own contribution before using them in an experience answer. A dated audit is historical evidence, not proof that the current release passes.

| Topic | Docita evidence |
| ---------------------------------------------- | ---------------------------------------------------------- |
| Written testing strategy | `docs/testing/TESTING.md` |
| Evidence of audit rigor | `docs/audits/2026-08-19-comprehensive-audit.md` |
| Trade-off writing ("what we deferred and why") | `docs/architecture/decisions/0004-rls-rollout-deferred.md` |
