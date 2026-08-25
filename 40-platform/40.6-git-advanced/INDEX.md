# Git Advanced — Index

> **7 files** — Advanced Git operations from branching strategies, rebase, cherry-pick, hooks, bisect, reflog, format-patch, and code archaeology to interview questions.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Tooling-%2364748b)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Git:** Every senior engineer must be fluent. Branching strategies affect team velocity. Rebase vs merge decisions affect history. Bisect, reflog, and code archaeology save hours when debugging "who broke this?". This section is short but high-value.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Branching & History](#branching--history) | 2 | Branching strategies + rebase/cherry-pick — the day-to-day |
| [Automation](#automation) | 1 | Git hooks, Husky, commitlint — enforce standards |
| [Advanced Commands](#advanced-commands) | 2 | Bisect, reflog, worktree, patches — the power tools |
| [Investigation](#investigation) | 1 | Code archaeology — finding who/when/why |
| [Interview Prep](#interview-prep) | 1 | 50+ Qs |

*Slots `40.6.01`, `40.6.08`, `40.6.09` are reserved for upcoming chapters (git internals, git at scale/LFS, signed commits/repository security) — no links yet.*

---

## Branching & History

How your team organizes work.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 01 | [Branching Strategies](40.6.02-branching-strategies.md) | Git Flow, GitHub Flow, trunk-based development, release branches | Pick the model for your team | 30 min |
| 02 | [Rebase & Cherry-Pick](40.6.03-rebase-cherry-pick.md) | Interactive rebase, conflict resolution, cherry-pick workflows | Linear history, porting fixes | 25 min |

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
| 03 | [Git Hooks](40.6.04-git-hooks.md) | Client/server hooks, pre-commit, Husky, commitlint, lint-staged | 25 min |

---

## Advanced Commands

The power tools.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Advanced Commands](40.6.05-git-advanced-commands.md) | `git bisect`, `git reflog`, `git worktree`, `git submodule`, `git filter-branch`/`filter-repo` | 30 min |
| 05 | [Patch & Bundle](40.6.06-patch-and-bundle.md) | `format-patch`, `am`, `send-email`, bundles, OSS contribution workflow | 20 min |

---

## Investigation

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Code Archaeology](40.6.07-code-archaeology.md) | `git blame`, `git log -S`, `git bisect`, `git reflog`, history investigation | 25 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [Interview Questions](40.6.10-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## Suggested Study Order

1. **Branching Strategies** — must know (you'll be asked what your team uses)
2. **Rebase & Cherry-Pick** — must know
3. **Git Hooks** — for senior roles
4. **Advanced Commands** — for the "what would you do if…" questions
5. **Code Archaeology** — for debugging questions
6. **Patch & Bundle** — for OSS contribution
7. **Interview Questions** — final review

---

## Common interview topics

- "Rebase vs merge — when to use which?"
- "How do you find which commit introduced a bug?" (bisect)
- "How do you undo a commit? What about an already-pushed commit?"
- "How do you resolve a merge conflict?"
- "What does `git reflog` do? How has it saved you?"
- "Walk me through your team's branching strategy."

---

## Cross-References

- [CI/CD](../40.3-ci-cd/INDEX.md) — pipelines run on branches
- [Monorepo](../40.8-monorepo/INDEX.md) — branching for monorepos
- [Production Engineering](../../50-quality/50.4-production-engineering/INDEX.md) — bisect for production bugs

---

## Navigation

[← Previous: Build Tools](../40.5-build-tools/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Serverless & Edge →](../40.7-serverless-edge/INDEX.md)
