# Performance Interview Prep

> **1 file.** The curated question bank for web performance rounds — Core Web Vitals mechanics, debugging walkthroughs, lab-vs-field judgment, and budget design.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Contents | Time |
| --: | ------ | ---------- | ------ |
| 01 | [Interview Questions](50.3.4.01-interview-questions.md) | 25+ curated questions with answers | 1-2 hrs |

---

## Questions you will be ready for

- "What are Core Web Vitals? What are the thresholds?"
- "How do you measure LCP? How do you improve it?"
- "Your LCP is 4 seconds. Walk me through how you'd debug it."
- "How do you set performance budgets?"
- "Difference between lab and field data?"
- "INP vs FID — what changed?"

---

## How to use it

Answer out loud before reading the model answer; the debugging walkthroughs ("LCP is 4 seconds...") are judged on structured diagnosis, not memorized fixes.

---

## Cross-References

- [Testing interview bank](../../50.1-testing/06-interview-prep/50.1.6.01-interview-questions.md) — the sibling quality round.
- [Accessibility](../../50.2-accessibility/INDEX.md) — Lighthouse audits cover both.

---

## Navigation

[← Optimization & Governance](../03-optimization-and-governance/INDEX.md) · [↑ Performance Home](../INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at story material you can cite in performance rounds.

| Topic | Docita evidence |
| ------------------------ | ---------------------------------------------------------------------------------------- |
| "Design a budget" story | `scripts/perf/route-budgets.config.mjs` (per-route budgets, checked in CI) |
| Debugging-story material | `slow-query-logging.service.ts` + `query-budget.extension.ts` in `apps/api/src/shared/…` |
| Ops follow-through story | `docs/operations/SLOS.md` + `ops-alert.listener.ts` |
