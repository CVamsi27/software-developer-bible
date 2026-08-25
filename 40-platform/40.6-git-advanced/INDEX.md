# Git Advanced — Index

> **10 files** — Advanced Git operations from the object model, branching strategies, rebase, cherry-pick, hooks, bisect, reflog, format-patch, code archaeology, LFS/partial clones, and commit signing to interview questions.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Tooling-%2364748b)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Git:** Every senior engineer must be fluent. The object model explains every other command. Branching strategies affect team velocity. Rebase vs merge decisions affect history. Bisect, reflog, and code archaeology save hours when debugging "who broke this?". At scale, LFS and partial clones keep big repos usable; signed commits anchor supply-chain security. This section is short but high-value.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Internals](#internals) | 1 | Objects, refs, packfiles — the mental model behind every command |
| [Branching & History](#branching--history) | 2 | Branching strategies + rebase/cherry-pick — the day-to-day |
| [Automation](#automation) | 1 | Git hooks, Husky, commitlint — enforce standards |
| [Advanced Commands](#advanced-commands) | 2 | Bisect, reflog, worktree, patches — the power tools |
| [Investigation](#investigation) | 1 | Code archaeology — finding who/when/why |
| [Scale & Security](#scale--security) | 2 | LFS, partial clones, signed commits — repos that stay fast and provable |
| [Interview Prep](#interview-prep) | 1 | 50+ Qs |

---

## Internals

Understand this once and `reset`, `rebase`, and recovery stop being scary.

| # | File | Topics | When to read | Read time |
|--:|------|--------|--------------|----------:|
| 01 | [Git Internals: Objects, Refs & Packfiles](40.6.01-git-internals-objects-refs-packfiles.md) | blob/tree/commit/tag model, `hash-object`/`mktree` demos, HEAD & refs, packfiles/deltas, reflog safety net, gc/repack, how reset/rebase move refs, `.git` directory tour | First — it unlocks everything else | 30 min |

---

## Branching & History

How your team organizes work.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 02 | [Branching Strategies](40.6.02-branching-strategies.md) | Git Flow, GitHub Flow, trunk-based development, release branches | Pick the model for your team | 30 min |
| 03 | [Rebase & Cherry-Pick](40.6.03-rebase-cherry-pick.md) | Interactive rebase, conflict resolution, cherry-pick workflows | Linear history, porting fixes | 25 min |

**Decision:**

```text
What branching model?
├── Open-source / many contributors → GitHub Flow (PR per feature)
├── Multiple production versions → Git Flow (develop/release/hotfix)
├── High-velocity team / strong CI → Trunk-based (short-lived branches, feature flags)
└── Monorepo with release trains → Custom (release branches per package)
```

---

## Automation

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Git Hooks](40.6.04-git-hooks.md) | Client/server hooks, pre-commit, Husky, commitlint, lint-staged | 25 min |

---

## Advanced Commands

The power tools.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 05 | [Advanced Commands](40.6.05-git-advanced-commands.md) | `git bisect`, `git reflog`, `git worktree`, `git submodule`, `git filter-branch`/`filter-repo` | 30 min |
| 06 | [Patch & Bundle](40.6.06-patch-and-bundle.md) | `format-patch`, `am`, `send-email`, bundles, OSS contribution workflow | 20 min |

---

## Investigation

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [Code Archaeology](40.6.07-code-archaeology.md) | `git blame`, `git log -S`, `git bisect`, `git reflog`, history investigation | 25 min |

---

## Scale & Security

Keeping large repositories fast and history trustworthy.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 08 | [Git at Scale: LFS & Partial Clones](40.6.08-git-at-scale-lfs-partial-clones.md) | LFS pointer files/smudge-clean filters, partial clone (`--filter=blob:none`), sparse-checkout, Scalar, CI shallow clones (`fetch-depth`), repo size audits | 25 min |
| 09 | [Signed Commits & Repository Security](40.6.09-signed-commits-repository-security.md) | GPG vs SSH vs Sigstore signing, Verified badges, branch protection enforcement, mailmap identity hygiene, CI verify steps, supply-chain context | 20 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 10 | [Interview Questions](40.6.10-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## Suggested Study Order

1. **Git Internals** — the object model makes everything else click
2. **Branching Strategies** — must know (you'll be asked what your team uses)
3. **Rebase & Cherry-Pick** — must know
4. **Git Hooks** — for senior roles
5. **Advanced Commands** — for the "what would you do if…" questions
6. **Code Archaeology** — for debugging questions
7. **Patch & Bundle** — for OSS contribution
8. **LFS & Partial Clones** — for platform/scale roles
9. **Signed Commits** — for security-minded teams
10. **Interview Questions** — final review

---

## Common interview topics

- "What happens when you run `git commit`?" (object model)
- "Rebase vs merge — when to use which?"
- "How do you find which commit introduced a bug?" (bisect)
- "How do you undo a commit? What about an already-pushed commit?"
- "How do you resolve a merge conflict?"
- "What does `git reflog` do? How has it saved you?"
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
