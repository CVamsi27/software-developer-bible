# Behavioral — Index

> **Study time:** ≈ 46 min of reading (6 files, ~8 min average).
> **Interview-depth behavioral prep.** The universal basics (STAR framework, HR questions, resume) live in [00-strategy](../../00-strategy/INDEX.md); this folder holds the deeper material you use once the basics are internalized.

[![Files](https://img.shields.io/badge/files-6-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why this section:** A behavioral answer turns work into evidence of judgment. Read the [STAR method](../../00-strategy/00.03-star-method.md) first, then use this section to explain the constraint, your contribution, the trade-off, and the observed result.

---

## Pass 1 — Find the Decision and Your Contribution

Read stakeholder management, then use the leadership prompts to choose related events from your actual work. Trace the request, competing constraints, decision owner, your action, and outcome. A fictional example teaches structure; it is not evidence to claim as your experience.

## Pass 2 — Explain Uncertainty and Durable Consequences

Read judgment calls and technical decision stories. Identify what was unknown, what evidence could change the choice, and what could still be undone after rollout. Explain the rollback boundary before describing a migration as reversible.

## Pass 3 — Repair One Missing Link

Use the self-audit chapter on a recording. Locate where the listener loses the constraint, ownership, or evidence and revise that passage. Practice with an interruption and a follow-up rather than memorizing the whole story.

## Choose the Prompt That Matches Your Evidence

| Category | File | When to use | Role priority | General importance |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------- | ------------------ |
| Stakeholder Management | [Stakeholder Management Stories](70.1.01-stakeholder-management-stories.md) | Product partnership rounds — scope pushback, deadline negotiation, trade-off communication | Essential | Important |
| Leadership | [Leadership Questions](70.1.02-leadership-questions.md) | Senior roles — "tell me about a time you led without authority" | Essential | Important |
| Judgment & Ambiguity | [Judgment Calls & Ambiguity](70.1.03-judgment-calls-ambiguity.md) | Decision-making probes — incomplete data, disagree-and-commit, escalation | Essential | Important |
| System Design Behavioral | [System Design Behavioral](70.1.04-system-design-behavioral.md) | System design rounds — "walk me through a design decision you made" | Essential | Important |
| Self-Audit | [Behavioral Anti-Patterns Checklist](70.1.05-behavioral-anti-patterns-checklist.md) | Practice phase — find and fix your delivery defects before the loop | Essential | Important |

## Finish With Revision, Then Your Own Story Bank

Work through [section revision](REVISION.md), then write a short factual account of one matching event. Use the [story-bank guide](../../80-lanes-abroad-full-stack/80.12-story-bank.md) for preparation and keep personal records in their canonical private location. Check each claim against the actual artifact, measurement, or timeline before using it in an interview.

A strong result can be qualitative. If a metric is available, include its denominator, period and uncertainty. Report unresolved limits and collaborators’ contributions as part of the same account.

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — its artifacts are raw material for your behavioral stories.

| Topic | Docita evidence |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Judgment / decision-writing (how you think, on record) | `docs/architecture/decisions/` — inspect decision records for reversals (`0009-vercel-retired.md`, `0012-replace-nextjs-with-vite-spa.md`) and deferrals (`0004-rls-rollout-deferred.md`) |
| Incident-response practice (STAR story fuel) | `docs/runbooks/` + `docs/operations/playbooks/` (`razorpay-outage.md`, `db-connection-exhaustion.md`) |
| Ownership beyond code (compliance ops) | `apps/api/src/shared/modules/compliance/data-retention.scheduler.ts` + `archival.service.ts` |

Use an artifact only when you can identify your actual contribution. An ADR records a decision; a playbook records a procedure. Check authorship, dates, deployment records, and incident timelines before claiming that you authored or exercised it.

## Continue Into Technical Practice

- [Interview strategy](../../00-strategy/INDEX.md) — prerequisites: resume, communication, STAR and HR preparation
- [Coding patterns](../70.2-coding-patterns/INDEX.md) — algorithm practice for technical rounds
- [Technical Decision Stories](70.1.04-system-design-behavioral.md) — connect a design mechanism to actual work evidence

## Navigation

[← Previous: Strategy](../../00-strategy/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Coding Patterns →](../70.2-coding-patterns/INDEX.md)
