# Git Advanced — Index

> **Study time:** ≈ 1 h 23 m of reading (11 files, ~8 min average).
> **11 files** — Advanced Git operations from the object model, branching strategies, rebase, cherry-pick, hooks, bisect, reflog, format-patch, code archaeology, LFS/partial clones, and commit signing to interview questions.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Tooling-%2364748b)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Git:** Every senior engineer must be fluent. The object model explains every other command. Branching strategies affect team velocity. Rebase vs merge decisions affect history. Bisect, reflog, and code archaeology save hours when debugging "who broke this?". At scale, LFS and partial clones keep big repos usable; signed commits anchor supply-chain security. This section is short but high-value.

---

## Topic Categories

| Category | Files | Why it matters |
| ------------------------------------------ | ----: | ----------------------------------------------------------------------- |
| [Internals](#internals) | 1 | Objects, refs, packfiles — the mental model behind every command |
| [Branching & History](#branching--history) | 2 | Choose an integration/release path, then move or port commits safely |
| [Automation](#automation) | 1 | Git hooks, Husky, commitlint — enforce standards |
| [Advanced Commands](#advanced-commands) | 2 | Bisect, reflog, worktree, patches — the power tools |
| [Investigation](#investigation) | 1 | Code archaeology — finding who/when/why |
| [Scale & Security](#scale--security) | 2 | LFS, partial clones, signed commits — repos that stay fast and provable |
| [Interview Prep](#interview-prep) | 1 | 40 source-linked questions |

---

## Internals

Understand this once and `reset`, `rebase`, and recovery stop being scary.

| # | File | Topics | When to read | Role priority | General importance | Read time |
| --: | ------ | -------- | -------------- | --- | --- | ----------: |
| 01 | [Git Internals: Objects, Refs & Packfiles](40.6.01-git-internals-objects-refs-packfiles.md) | file-to-commit trace, object identities, refs and HEAD, pack storage, reset/rebase effects, reflog recovery limits, linked worktrees | First — it unlocks everything else | Important | Foundational | 10 min |

---

## Branching & History

How your team organizes work.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 02 | [Branching Strategies](40.6.02-branching-strategies.md) | Integration cadence, review policy, Git Flow, trunk-based delivery, supported release lines | Choose from release and support needs, not team-size labels | Important | Foundational | 6 min |
| 03 | [Rebase & Cherry-Pick](40.6.03-rebase-cherry-pick.md) | Rewrite private patch series, compare rebases, backport fixes, resolve replay conflicts | Update a topic branch or move one fix to a supported release | Important | Foundational | 8 min |

GitHub Flow and trunk-based development can coexist: one describes a pull-request review path, while the other emphasizes short integration cycles. Choose review controls and release-line ownership separately.

**Decision:**

```text
What does the product need?
├── One active release line, frequent integration → trunk-based development
│   └── Use reviewed short-lived branches when the repository requires a PR
├── A clear PR loop, releases from the default branch → GitHub Flow
├── Planned version preparation plus a separate integration line → Git Flow
└── Several older versions still supported → trunk + scoped release branches
    └── Define who backports, what runs on each line, and when each line closes
```

---

## Automation

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Git Hooks](40.6.04-git-hooks.md) | Staged/message checks, Husky/lint-staged, receiver policy, post-receive boundary—choose by event and authority | Important | Foundational | 7 min |

---

## Advanced Commands

The power tools.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Advanced Commands](40.6.05-git-advanced-commands.md) | Bisect’s test contract, reflog recovery limits, stash vs worktree, pinned submodules, reset vs revert | Important | Foundational | 6 min |
| 06 | [Patch, Bundle & Archive](40.6.06-patch-and-bundle.md) | Ordered mbox replay, sign-off vs signature, bundle prerequisites and limits, tracked-tree release archives | Important | Foundational | 7 min |

---

## Investigation

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 07 | [Code Archaeology](40.6.07-code-archaeology.md) | `git blame`, `git log -S`, `git bisect`, `git reflog`, history investigation | Important | Foundational | 12 min |

---

## Scale & Security

Keeping large repositories fast and history trustworthy.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [Git at Scale: LFS & Partial Clones](40.6.08-git-at-scale-lfs-partial-clones.md) | LFS pointer files/smudge-clean filters, partial clone (`--filter=blob:none`), sparse-checkout, Scalar, CI shallow clones (`fetch-depth`), repo size audits | Important | Foundational | 8 min |
| 09 | [Signed Commits & Repository Security](40.6.09-signed-commits-repository-security.md) | GPG vs SSH vs Sigstore signing, Verified badges, branch protection enforcement, mailmap identity hygiene, CI verify steps, supply-chain context | Important | Foundational | 7 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 10 | [Interview Questions](40.6.10-interview-questions.md) | 40 source-linked questions with answers | Important | Foundational | 7 min |

---

## Suggested Study Order

1. **Git Internals** — the object model makes everything else click
2. **Branching Strategies** — explain integration cadence, review gates, and supported releases before naming a model
3. **Rebase & Cherry-Pick** — must know
4. **Git Hooks** — for senior roles
5. **Advanced Commands** — for the "what would you do if…" questions
6. **Code Archaeology** — for debugging questions
7. **Patch, Bundle & Archive** — choose the right artifact for review, offline history transfer, or a source release
8. **LFS & Partial Clones** — for platform/scale roles
9. **Signed Commits** — for security-minded teams
10. **[Section revision](REVISION.md)** — explain each state transition without copying
11. **Interview Questions** — test decisions with a failure scenario

---

## Common interview topics

- "What happens when you run `git commit`?" (object model)
- "Rebase vs merge — when to use which?"
- "How do you find which commit introduced a bug?" (bisect)
- "How do you undo a commit? What about an already-pushed commit?"
- "How do you resolve a merge conflict?"
- "What does `git reflog` do? How has it saved you?"
- "Should this change move as a patch, bundle, or source archive?"
- "Walk me through your team's branching strategy."
- "How would you keep a multi-GB repository cloneable?" (LFS, partial clones, shallow CI)

---

## Cross-References

- [CI/CD](../40.3-ci-cd/INDEX.md) — pipelines run on branches
- [Monorepo](../40.8-monorepo/INDEX.md) — branching for monorepos
- [Production Engineering](../../50-quality/50.4-production-engineering/INDEX.md) — bisect for production bugs

---

## Navigation

[← Previous: Build Tools](../40.5-build-tools/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Serverless & Edge →](../40.7-serverless-edge/INDEX.md)

---

## Docita Anchor

Source walkthrough for [Docita](../../projects/docita/INDEX.md), checked against the local source on 10 October 2026. These files illustrate intended checks; their existence does not prove every gate currently passes or is deployed.

| Topic | Source to inspect | Boundary |
| -------------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
| Local feedback | `.husky/pre-commit` and `.husky/pre-push` | Read the actual scripts and invoked gates; client hooks are bypassable |
| Integration checks | CI workflow definitions and package scripts | Verify required server checks and current results separately |
| Workflow consistency | `check-workflow-script-refs.mjs` | Script references are checked; this is not deployment or signature evidence |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
