---
section: Git Advanced
category: Reference
tags: [concept, reference, guide]
---

# Git Code Archaeology

## Definition

**Code archaeology** is the practice of investigating a codebase's history to answer questions like: "When was this line added?", "Who wrote this code?", "What commits introduced this bug?", "Why was this design decision made?" Git provides powerful tools (`log`, `blame`, `bisect`, `pickaxe`) that turn version control from a backup mechanism into a queryable history database.

For senior engineers, code archaeology is a daily skill. Production bugs require finding the regression-introducing commit. Refactors require understanding the history of a file. Code review requires context. Performance investigations require identifying what changed.

## Why Do We Need It?

1. **Find regression-introducing commits** with `git bisect` (binary search over commit history)
2. **Understand code history** with `git blame` (who wrote what, when)
3. **Track changes** with `git log -S` (pickaxe — find when a string was added/removed)
4. **Onboard to unfamiliar code** by reading commit messages, not just current state
5. **Audit and compliance** (who had access to what, when)
6. **Justify design decisions** in code review with links to original commits

## How It Works

### The Investigation Toolkit

```text
┌─────────────────────────────────────────────────────────────────┐
│              Git Code Archaeology Toolkit                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Question                                Tool                   │
│  ──────────────────────────────────────────────────────────── │
│  Who wrote this line?                     git blame              │
│  When was this string added?              git log -S "string"    │
│  What changed in this file?               git log -p -- file     │
│  When was this function added?            git log -S "function"  │
│  Which commit broke this?                 git bisect             │
│  What's in this commit?                   git show <sha>         │
│  What's the history of this file?         git log --follow       │
│  Find commits by message                  git log --grep         │
│  Find commits by author                   git log --author       │
│  Most-modified files                      git log --stat         │
│  Recent activity by author                git shortlog           │
│  When was a branch created?               git reflog             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### git blame — Who Wrote This?

```bash
# Show author of each line in a file
git blame src/auth/login.ts

# Show with line numbers and short SHA
git blame -s src/auth/login.ts

# Limit to a line range
git blame -L 10,30 src/auth/login.ts

# Ignore whitespace changes
git blame -w src/auth/login.ts

# Show original commit (not subsequent moves)
git blame -C src/auth/login.ts  # -C: detect code moved from other files
```

```text
$ git blame -L 1,10 src/auth/login.ts
^abc1234 (Alice  2024-01-15) export async function login(email: string) {
def56789 (Bob    2024-01-18)   const user = await db.users.findByEmail(email);
^abc1234 (Alice  2024-01-15)   if (!user) throw new Error('Not found');
def56789 (Bob    2024-01-18)   return user;
ghi78901 (Carol  2024-02-01) }
```

### git log -S (Pickaxe) — When Was This String Added?

```bash
# Find when "deprecated" was added to a function name
git log -S "oldFunctionName" --oneline

# Search for a function signature
git log -S "function validateToken(token: string)" --oneline

# Search across all branches
git log --all -S "secret_key" --oneline

# Show the diff for each match
git log -S "deprecated" -p --pickaxe-all
```

```bash
# git log -G (regex) — same but with regex matching
git log -G "TODO|FIXME" --oneline
```

### git log -p — Full Diffs in History

```bash
# Show all changes to a file
git log -p -- src/auth/login.ts

# Show last 5 commits' diffs to a file
git log -p -5 -- src/auth/login.ts

# Show changes in a date range
git log -p --since="2024-01-01" --until="2024-02-01" -- src/

# Show changes matching a path filter
git log -p --all -- "src/api/*.ts"
```

### git bisect — Binary Search for the Bad Commit

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark a known good commit
git bisect good v1.0.0

# Git checks out a middle commit — test it
npm test  # or run your repro

# Mark as good or bad
git bisect good  # tests pass
git bisect bad   # tests fail

# Repeat until git finds the first bad commit
# Output: "abc123 is the first bad commit"

# Automated bisect with a test script
git bisect start HEAD v1.0.0
git bisect run npm test
# Git uses exit code 0 (good) / 1 (bad) to find the regression

# End the session
git bisect reset
```

### git log --grep — Search Commit Messages

```bash
# Find commits mentioning "performance"
git log --grep="performance" --oneline

# Find commits referencing a ticket number
git log --grep="JIRA-1234" --oneline

# Multiple patterns (OR)
git log --grep="fix" --grep="bug" --all-match --oneline

# Case-insensitive
git log --grep="API" -i --oneline
```

### git shortlog — Activity by Author

```bash
# Commits per author
git shortlog -sn

# In a date range
git shortlog -sn --since="2024-01-01"

# With email
git shortlog -sne

# Group by author, show all their commits
git shortlog --author="alice@example.com" --no-merges
```

### git log --stat — File-Level Activity

```bash
# Show file change stats per commit
git log --stat -10

# Find most-modified files in last 6 months
git log --since="6 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Show commits modifying a directory
git log --stat -- src/auth/
```

### git reflog — Recover "Lost" Work

```bash
# Show all HEAD movements (90 days by default)
git reflog

# Find a "lost" commit
git reflog | grep "Reset:"
# Output: abc123 HEAD@{2}: reset: moving to main
#         def456 HEAD@{1}: commit: WIP on feature

# Recover the WIP commit
git checkout def456
# or
git cherry-pick def456
```

## Real-World Use Cases

### 1. Production Bug Investigation

```bash
# "Login broke sometime in the last 2 weeks"
git log --since="2 weeks ago" --oneline -- src/auth/
# Find the suspect commit

git bisect start HEAD main
git bisect run ./test-login.sh
# Git identifies the regression-introducing commit
```

### 2. Onboarding to a Legacy Codebase

```bash
# Read the commit history of the most complex file
git log --follow -p -- src/legacy/monster.ts | less

# Find the original author of a key function
git log -S "function parsePDF" --pretty=format:"%h %an %ad %s" --date=short
```

### 3. Code Review Context

```bash
# Reviewer asks: "Why is this here?"
git blame -L 45,55 src/api/handlers.ts
# Now you can read the original commit message
git show <sha-from-blame>
```

### 4. License and Compliance Audit

```bash
# Find when a specific dependency was added
git log -S "import.*from 'lodash'" --oneline

# Find all commits mentioning "secret" or "key"
git log --grep="secret" -i --oneline

# Find authors who touched security-sensitive files
git log --since="1 year ago" --author=@ -- src/auth/ src/crypto/
```

### 5. Performance Regression Hunt

```bash
# "LCP regressed from 1.5s to 3s in the last month"
git log --since="1 month ago" --oneline -- src/components/Header.tsx

# Find commits that added large dependencies
git log --diff-filter=A --name-only --pretty=format: | grep "package.json"
```

## Common Mistakes

### 1. Ignoring Whitespace in blame

```bash
# ❌ Bad: blame shows recent reformatter as author
git blame src/file.ts

# ✅ Good: ignore whitespace-only changes
git blame -w src/file.ts
```

### 2. Bisecting Without a Reliable Test

```text
❌ Bad: "I think it works now" — flaky results
✅ Good: write a deterministic test (unit, integration, or shell script)
```

`git bisect run` is only as good as the test's exit code.

### 3. Searching the Wrong Branch

```bash
# ❌ Bad: only searches current branch
git log -S "oldFunction"

# ✅ Good: search all branches and history
git log --all -S "oldFunction"
```

### 4. Trusting blame After Major Refactors

After a `git mv` or mass-rename, `git blame` may show the refactor commit instead of the original author. Use `git blame -C` to detect moved code.

### 5. Skipping `--follow` for Renamed Files

```bash
# ❌ Bad: only shows history after rename
git log -- src/auth/login.ts

# ✅ Good: follows renames
git log --follow -p -- src/auth/login.ts
```

## Best Practices

1. **Use `git blame -w`** to ignore whitespace-only changes
2. **Use `git log -S` (pickaxe)** to find when strings appeared/disappeared
3. **Automate bisect** with `git bisect run <test-script>` for reliable results
4. **Search all branches** with `--all` when investigating
5. **Use `--follow` for renamed files**
6. **Write commit messages with archaeology in mind** — "why" not just "what"
7. **Tag releases** so bisect can find known-good commits quickly
8. **Use `git log --grep` and `--author`** for ticket/author-based searches
9. **Use `git shortlog -sn`** to find domain experts for a file
10. **Read commit messages during code review** — they document decisions

## Useful Aliases

```bash
# Add to ~/.gitconfig
[alias]
  # Find when a string was added
  when = log -S

  # Find when a regex was added
  when-rgx = log -G

  # Blame with whitespace ignore
  bl = blame -w

  # Search commit messages
  find = log --grep

  # Most-modified files
  heat = log --since=\"6 months ago\" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

  # Bisect helper
  bs = bisect
```

## Performance Considerations

| Operation | Time | Use Case |
|-----------|------|----------|
| `git blame` on a file | < 1s | Per-line authorship |
| `git log -S "string"` | 1-10s | Find when string appeared |
| `git log -p` on large file | 5-30s | Full history |
| `git bisect` (1000 commits, manual) | 10-15 steps | Find regression |
| `git bisect run` (automated) | 10-15 tests | Same, faster |
| `git log --all` | Seconds-minutes | Full history across all branches |

## Summary

- `git blame` answers "who wrote this line"
- `git log -S` (pickaxe) finds when a string was added/removed
- `git bisect` does binary search over commit history
- `git log --grep` searches commit messages
- `git shortlog -sn` shows commits per author
- `git reflog` recovers "lost" work within 90 days
- Use `-C` for moved code, `-w` to ignore whitespace
- Write commit messages with archaeology in mind

---

## Cheat Sheet
```text
GIT CODE ARCHAEOLOGY CHEAT SHEET
============================================================

WHO WROTE THIS?
  git blame file.ts              # per-line
  git blame -w file.ts           # ignore whitespace
  git blame -C file.ts           # detect moved code
  git blame -L 10,30 file.ts     # line range

WHEN WAS THIS STRING ADDED?
  git log -S "string"            # pickaxe (literal)
  git log -G "regex"             # pickaxe (regex)
  git log --all -S "string"      # all branches

WHAT CHANGED IN THIS FILE?
  git log -p -- file.ts          # full diffs
  git log --follow -p -- file.ts # follow renames
  git log --stat -10 -- file.ts  # file change stats

WHICH COMMIT BROKE THIS?
  git bisect start HEAD main
  git bisect run ./test.sh      # automated
  git bisect reset              # end session

SEARCH COMMIT MESSAGES:
  git log --grep="bug" -i
  git log --grep="JIRA-1234"

ACTIVITY BY AUTHOR:
  git shortlog -sn              # all authors
  git shortlog -sn --since="1y"

RECOVER LOST WORK:
  git reflog                    # last 90 days
  git checkout <sha-from-reflog>

USEFUL FLAGS:
  -w   ignore whitespace
  -C   detect moved code
  --follow   follow renames
  --all   search all branches
  -p   show patches
  --stat  show file stats
  --grep=  search messages
  --author=  filter by author

INTERVIEW TIPS:
  • Walk through bisect workflow for a real bug
  • Explain pickaxe vs grep difference
  • Show how blame handles renames (-C)
  • Mention reflog as a 90-day safety net
```
---

## See Also
- [Branching Strategies](01-Branching-Strategies.md)
- [CI/CD](../15-CI-CD/)
- [Git Advanced Commands](04-Git-Advanced-Commands.md)
- [Git Hooks](03-Git-Hooks.md)
- [Patch & Bundle](06-Patch-and-Bundle.md)
- [Rebase & Cherry-Pick](02-Rebase-Cherry-Pick.md)

## References & Learn More

- [git-blame Documentation](https://git-scm.com/docs/git-blame)
- [git-bisect Documentation](https://git-scm.com/docs/git-bisect)
- [git-log Documentation](https://git-scm.com/docs/git-log)
- [Pro Git Book - Ch. 10 (Inspecting History)](https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection)
- [Pro Git Book - Ch. 11 (Submodules)](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Oh Shit, Git!?!](https://ohshitgit.com/) (recovery reference)
