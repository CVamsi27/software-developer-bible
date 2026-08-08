---
section: Git Advanced
category: Reference
tags: [concept, reference]
---

# Git Advanced Commands

## Definition
Git advanced commands are powerful tools for debugging, history manipulation, and repository management. They go beyond basic add/commit/push operations to provide sophisticated workflows.

## Why Do We Need Them?

- **Debugging**: Find when bugs were introduced
- **Recovery**: Recover lost commits or branches
- **Efficiency**: Manage complex workflows
- **Collaboration**: Handle merge conflicts and parallel development
- **Maintenance**: Clean up repository history

## How It Works

### Command Categories

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Git Advanced Commands                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Debugging          History           Repository                │
│  ┌─────────────┐    ┌─────────────┐   ┌─────────────────────┐  │
│  │  bisect     │    │  rebase     │   │  worktree           │  │
│  │  blame      │    │  reflog     │   │  submodule          │  │
│  │  grep       │    │  stash      │   │  sparse-checkout    │  │
│  └─────────────┘    └─────────────┘   └─────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Git Bisect

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good abc1234

# Git will checkout middle commit
# Test the commit, then mark as good or bad
git bisect good  # or
git bisect bad

# Continue until Git finds the first bad commit
# When done:
git bisect reset

# Automate bisect with script
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run npm test

```

### Git Reflog

```bash
# Show reflog (all HEAD changes)
git reflog

# Show reflog for specific branch
git reflog show main

# Restore lost commit
git reflog
# Find commit hash
git checkout abc1234

# Restore branch to specific commit
git reset --hard abc1234

# Clean up reflog
git reflog expire --expire=now --all
git gc --prune=now

```

### Git Stash

```bash
# Stash current changes
git stash

# Stash with message
git stash push -m "Work in progress: feature X"

# Stash specific files
git stash push -m "Stash only package.json" package.json

# List stashes
git stash list

# Apply stash (keep stash)
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear

# Show stash contents
git stash show -p stash@{0}

```

### Git Worktree

```bash
# Add worktree for hotfix
git worktree add ../hotfix-branch hotfix/1.0.1

# Add worktree for new feature
git worktree add ../feature-branch feature/new-feature

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../hotfix-branch

# Cleanup
git worktree prune

```

### Git Submodule

```bash
# Add submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# Initialize submodules
git submodule init

# Update submodules
git submodule update

# Clone with submodules
git clone --recursive https://github.com/user/repo.git

# Update all submodules to latest
git submodule update --remote --merge

# Remove submodule
git submodule deinit path/to/submodule
git rm path/to/submodule
rm -rf .git/modules/path/to/submodule

```

### Git Revert vs Reset

```bash
# Revert (safe, creates new commit)
git revert abc1234

# Revert merge commit
git revert -m 1 abc1234

# Reset (dangerous, rewrites history)
# Soft: keeps changes staged
git reset --soft abc1234

# Mixed: keeps changes unstaged (default)
git reset --mixed abc1234

# Hard: discards all changes
git reset --hard abc1234

```

### Git Cherry-Pick Advanced

```bash
# Cherry-pick multiple commits
git cherry-pick abc1234 def5678 ghi9012

# Cherry-pick range
git cherry-pick abc1234..ghi9012

# Cherry-pick without committing
git cherry-pick --no-commit abc1234

# Cherry-pick from different branch
git cherry-pick feature~2

# Cherry-pick merge commit
git cherry-pick -m 1 abc1234

# Abort cherry-pick
git cherry-pick --abort

# Continue after resolving conflicts
git cherry-pick --continue

```

### Git Sparse Checkout

```bash
# Enable sparse checkout
git sparse-checkout init

# Set sparse checkout pattern
git sparse-checkout set src/ docs/

# Add more directories
git sparse-checkout add tests/

# Show current pattern
git sparse-checkout list

# Disable sparse checkout
git sparse-checkout disable

```

### Git Advanced Log

```bash
# Pretty log format
git log --pretty=format:"%h - %an, %ar : %s"

# Graph view
git log --graph --oneline --all

# Show file changes
git log --stat

# Search commits
git log --grep="feature"

# Filter by author
git log --author="John"

# Show last N commits
git log -5

# Show commits affecting file
git log -- path/to/file

# Show commits between dates
git log --after="2023-01-01" --before="2023-12-31"

```

### Git Advanced Diff

```bash
# Compare branches
git diff branch1..branch2

# Compare specific commits
git diff abc1234..def5678

# Compare working directory
git diff

# Compare staged changes
git diff --staged

# Compare with statistics
git diff --stat

# Compare only word changes
git diff --word-diff

# Compare ignoring whitespace
git diff --ignore-all-space

```

### Git Advanced Blame

```bash
# Show who changed each line
git blame path/to/file

# Show with line ranges
git blame -L 10,20 path/to/file

# Show with revision
git blame abc1234 path/to/file

# Show with date
git blame --date=short path/to/file

```

## Real-World Use Cases

1. **Bug hunting**: Use bisect to find when bug was introduced

2. **Recovery**: Use reflog to recover lost commits

3. **Parallel work**: Use worktree for multiple branches

4. **Dependencies**: Use submodule for external libraries

5. **Emergency fixes**: Use stash for quick context switching

6. **Selective deployment**: Use cherry-pick for specific features

## Common Mistakes

1. **Using reset --hard**: Can lose work, prefer revert

2. **Not backing up before complex operations**: Always backup

3. **Ignoring submodules**: Can cause confusion

4. **Overusing stash**: Can become unmanageable

5. **Not cleaning up worktrees**: Wastes disk space

6. **Confusing revert and reset**: Different purposes

7. **Not understanding reflog**: Can't recover lost work

## Best Practices

1. **Prefer revert over reset**: Safe for shared branches

2. **Use descriptive stash messages**: Easy to find later

3. **Keep worktrees organized**: Named clearly, cleaned up

4. **Document submodule usage**: Team understanding

5. **Use bisect for debugging**: Efficient bug hunting

6. **Learn reflog**: Essential for recovery

7. **Practice complex operations**: In safe environment

8. **Backup before risky operations**: Always

## Performance Considerations

- **Bisect**: Fast binary search algorithm
- **Reflog**: Lightweight, stores locally
- **Stash**: Fast for temporary storage
- **Worktree**: Shares repository, efficient
- **Submodule**: Can be slow to update
- **Sparse checkout**: Reduces disk usage

## Summary
Git advanced commands provide powerful tools for debugging, recovery, and complex workflows. Master bisect for debugging, reflog for recovery, worktree for parallel work, and understand when to use revert vs reset. Practice these commands in safe environments before using in production.

---

## Cheat Sheet
```text
GIT ADVANCED COMMANDS CHEAT SHEET
============================================================

DEBUGGING:
  git bisect start              # find bad commit via binary search
  git bisect bad / good <sha>   # mark commits
  git bisect run <script>       # automated bisect
  git bisect reset              # end session
  git blame -L 10,20 file.ts    # who changed lines 10-20
  git log -S 'string' --oneline # find when string was added
  git log --author='name'       # filter by author

RECOVERY:
  git reflog                    # all HEAD movements (90 days)
  git reset --hard <sha>        # restore from reflog
  git fsck --lost-found         # find dangling objects
  git stash list / pop / drop   # temporary saves
  git worktree add <path> <br>  # multiple working dirs

REWRITING:
  git rebase -i HEAD~N          # edit last N commits
  git commit --amend            # modify last commit
  git filter-repo --path file   # remove file from history
  git filter-branch             # older, slower alternative

INSPECTION:
  git log --oneline --graph     # visual history
  git log --stat                # file change stats
  git show <sha>                # commit details
  git diff <a>..<b>             # compare commits
  git shortlog -sn              # commits per author

INTERVIEW TIPS:
  • Explain how reflog can save you from "lost" commits
  • Discuss bisect run for automated test-based debugging
  • Show how worktrees enable parallel branch work
```
---

## See Also
- [CI/CD](../15-CI-CD/)
- [Monorepo](../28-Monorepo/)

## References & Learn More

- [Git Documentation](https://git-scm.com/docs)
- [Git Bisect](https://git-scm.com/docs/git-bisect)
- [Git Reflog](https://git-scm.com/docs/git-reflog)
- [Git Worktree](https://git-scm.com/docs/git-worktree)
- [Git Submodule](https://git-scm.com/docs/git-submodule)
