# Reading Flow and Corpus Review Implementation Plan

> **For agentic workers:** Use executing-plans to implement the work and keep review evidence by path. Parallel editorial reviewers may own disjoint directory groups after the mechanical format migration.

**Goal:** Review all Markdown, remove chapter TL;DR repetition, improve learning flow, separate revision practice, and commit/push verified results.

**Architecture:** Concept chapters introduce the definition before deriving constraints and mechanisms, then give examples, decisions, mistakes and one final summary. Revision practice moves into a separate companion per category, as confirmed by the user. Interview banks retain their distinct interview role. Existing chapter URLs and sequence numbers remain stable.

**Tech Stack:** Markdown, Python verification scripts, Jekyll navigation/search generation, Git.

## Reading design

The user supplied a shared JavaScript explanation as an organization reference. Prefer a concrete problem, the rule that explains it, a small execution trace or diagram, and a focused comparison of alternatives. Define unfamiliar terms when they enter the explanation. Explain each new component’s relationship to the whole before naming its kinds; a heading such as “Environment Records in Detail” is insufficient if the reader has not learned what a record does inside a lexical environment. A heading earns its place by advancing understanding; do not fill every template slot with another overview. Keep technical depth through precise boundaries and examples rather than repeated prose. Use the reference's teaching approach, not its oversimplified technical claims.

## Priority update — 2 October 2026

The user now prioritizes the resume and target senior/founding full-stack TypeScript roles in Munich/Berlin. Review all relevant topics, preserve required mechanisms and important examples, and use JavaScript.info as an additional reading-flow reference. Prioritize JavaScript/TypeScript, React/Vite/Next.js, Node/Express/NestJS, PostgreSQL/Prisma, tenant isolation/authorization, jobs/outbox/idempotency/webhooks, AI guardrails, testing, deployment and observability. Pause further Indian SDE and Java-track work; preserve completed edits without claiming those deferred tracks are fully reviewed. Commit and push remain authorized after the applicable gates pass.

## Global Constraints

- User instructions supersede the previous TL;DR and inline-revision contract.
- Never change or commit the career-ops tool repository.
- Preserve personal data in its canonical directory; do not copy it into audit artifacts.
- Hand-review technical assertions and preserve unique information removed from opening summaries.
- Use official documentation and executable probes for version-sensitive claims.
- Counts and reading times are generated from disk.
- Run `bash scripts/verify.sh` before the final commit and push.

## Tasks

- [ ] Inventory every Markdown path, document genre, section order and revision coverage.
- [ ] Remove TL;DR sections from teaching chapters with fence-aware parsing; record removed public teaching text for editorial recovery of unique facts. Preserve useful document introductions without the retired label in operational/reference documents.
- [ ] Put Definition before First Principles in concept chapters and update the canonical-order contract, fixtures, AGENTS.md and contributing.md.
- [ ] Implement the chosen separate revision layout, preserving fresh existing question pairs and links to chapter sections. Replace retired duplicated cheat sheets through editorial review, not mechanical answer generation.
- [ ] Review disjoint corpus areas for incorrect claims, stale examples, repetition, missing mechanisms and reading order; record every reviewed path and outstanding issue.
- [ ] Update category and stack INDEX reading stages so learning, review and interview practice are distinct navigation steps.
- [ ] Regenerate with `python3 scripts/read_time.py --write`, `python3 scripts/gen_master_index.py`, and `python3 scripts/check_counts.py --write`.
- [ ] Run the full gates, link checks, example probes and `git diff --check`; resolve every failure before committing.
- [ ] Review the complete diff and repository scope, then commit and push to the configured origin; verify the remote commit.
