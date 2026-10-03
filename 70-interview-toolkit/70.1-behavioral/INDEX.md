# Behavioral — Index

> **Study time:** ≈ 46 min of reading (6 files, ~8 min average).
> **Interview-depth behavioral prep.** The universal basics (STAR framework, HR questions, resume) live in [00-strategy](../../00-strategy/INDEX.md); this folder holds the deeper material you use once the basics are internalized.

[![Files](https://img.shields.io/badge/files-6-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why this section:** A behavioral answer turns work into evidence of judgment. Read the [STAR method](../../00-strategy/00.03-star-method.md) first, then use this section to explain the constraint, your contribution, the trade-off, and the observed result.

---

## Reading Passes

1. **Find the decision in the story.** Start with stakeholder management: trace a request, the competing constraints, and the agreed action. Use leadership prompts to find related examples from your own work.
2. **Explain what was uncertain.** Read judgment calls, then technical decision stories. Name what evidence could change the choice, what became durable, and where rollback stops being safe.
3. **Make the evidence easy to follow.** Use the self-audit chapter to repair one missing link in a recording. Finish with the separate revision companion and test your explanation with a listener.

## Topic Categories

| Category | File | When to use | Role priority | General importance |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------- | ------------------ |
| [Stakeholder Management](#stakeholder-management-stories) | [Stakeholder Management Stories](70.1.01-stakeholder-management-stories.md) | Product partnership rounds — scope pushback, deadline negotiation, trade-off communication | Essential | Important |
| [Leadership](#leadership) | [Leadership Questions](70.1.02-leadership-questions.md) | Senior roles — "tell me about a time you led without authority" | Essential | Important |
| [Judgment & Ambiguity](#judgment-calls--ambiguity) | [Judgment Calls & Ambiguity](70.1.03-judgment-calls-ambiguity.md) | Decision-making probes — incomplete data, disagree-and-commit, escalation | Essential | Important |
| [System Design Behavioral](#system-design-behavioral) | [System Design Behavioral](70.1.04-system-design-behavioral.md) | System design rounds — "walk me through a design decision you made" | Essential | Important |
| [Self-Audit](#behavioral-anti-patterns-checklist) | [Behavioral Anti-Patterns Checklist](70.1.05-behavioral-anti-patterns-checklist.md) | Practice phase — find and fix your delivery defects before the loop | Essential | Important |

---

## Stakeholder Management Stories

STAR stories for product partnership: pushing back on scope with evidence, negotiating deadlines with PMs, resolving design conflicts with data, influencing without authority.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 1 | [Stakeholder Management Stories](70.1.01-stakeholder-management-stories.md) | Scope pushback with evidence, deadline negotiation via options, design-conflict data tests, influence without authority, translating trade-offs to business language, decision ownership and results | Essential | Important | 9 min |

---

## Leadership

Senior-signal questions about leading, mentoring, conflict, and decision-making.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 1 | [Leadership Questions](70.1.02-leadership-questions.md) | Leading without authority, mentoring, conflict resolution, delegation, prioritization, handling failure | Essential | Important | 8 min |

---

## Judgment Calls & Ambiguity

Deciding under incomplete data: what remains unknown, what is costly to undo, and who should own the decision. The “70%” idea is a heuristic, not a measured confidence requirement.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 1 | [Judgment Calls & Ambiguity](70.1.03-judgment-calls-ambiguity.md) | Reversible vs irreversible decisions, one-way-door examples, essential evidence before acting, reversal triggers, disagree-and-commit stories, escalation judgment, explanation checks | Essential | Important | 14 min |

---

## System Design Behavioral

How to talk about your past design decisions in interviews.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 2 | [System Design Behavioral](70.1.04-system-design-behavioral.md) | Framing architecture stories with trade-offs, the "show your work" pattern, how to discuss past designs | Essential | Important | 8 min |

**The framework:**
1. **Context** — what was the system, who used it, what was the constraint?
2. **Decision** — what did you choose, and what were the alternatives?
3. **Trade-offs** — what did you sacrifice? What did you gain?
4. **Outcome** — what happened? What did you learn?

---

## Behavioral Anti-Patterns Checklist

Self-audit instrument: locate where a recorded answer loses its context, ownership, or evidence, then repair that passage before trying a mock.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 3 | [Behavioral Anti-Patterns Checklist](70.1.05-behavioral-anti-patterns-checklist.md) | Excessive setup, unclear ownership, unsupported results, prompt mismatch, honest recovery, recording + listener feedback | Essential | Important | 4 min |

---

## The Flow

```text
00-strategy          this folder              your lane folder
(basics)             (interview depth)        (personal material)
STAR framework   →   stakeholder mgmt     →   story-bank.md
HR + resume          leadership questions
                     judgment & ambiguity
                     anti-pattern drills
```

1. **00-strategy** — STAR, HR, resume (read first)
2. **here** — stakeholder, leadership, judgment, self-audit (read for senior rounds)
3. **story-bank.md** — your own stories, written down (in the lane folder)

---

## Cross-References

- [00-strategy](../../00-strategy/INDEX.md) — STAR framework, HR questions, resume
- [Story bank](../../80-lanes-abroad-full-stack/80.12-story-bank.md) — pre-written STAR stories
- [Coding patterns](../70.2-coding-patterns/INDEX.md) — for the technical rounds

---

## Navigation

[← Previous: Strategy](../../00-strategy/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Coding Patterns →](../70.2-coding-patterns/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — its artifacts are raw material for your behavioral stories.

| Topic | Docita evidence |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Judgment / decision-writing (how you think, on record) | `docs/architecture/decisions/` — inspect decision records for reversals (`0009-vercel-retired.md`, `0012-replace-nextjs-with-vite-spa.md`) and deferrals (`0004-rls-rollout-deferred.md`) |
| Incident-response practice (STAR story fuel) | `docs/runbooks/` + `docs/operations/playbooks/` (`razorpay-outage.md`, `db-connection-exhaustion.md`) |
| Ownership beyond code (compliance ops) | `apps/api/src/shared/modules/compliance/data-retention.scheduler.ts` + `archival.service.ts` |

Use an artifact only when you can identify your actual contribution. An ADR records a decision; a playbook records a procedure. Check authorship, dates, deployment records, and incident timelines before claiming that you authored or exercised it.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
