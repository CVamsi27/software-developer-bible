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

## Interview Questions

### Beginner (5-10)

1. **What is git bisect?**

   - Binary search tool to find which commit introduced a bug.

2. **What is git stash?**

   - Temporarily stores modified tracked files.

3. **What is git reflog?**

   - Reference log showing all HEAD movements.

4. **What is the difference between revert and reset?**

   - Revert creates new commit undoing changes, reset moves HEAD.

5. **What is git worktree?**

   - Multiple working directories attached to same repository.

6. **What is git submodule?**

   - Repository embedded inside another repository.

7. **What is git cherry-pick?**

   - Apply specific commit from one branch to another.

8. **What is git sparse-checkout?**

   - Partial checkout of repository contents.

### Intermediate (5-10)

9. **How do you use git bisect to find a bug?**

   - Start bisect, mark good/bad commits, let Git find first bad commit.

10. **How do you recover a lost commit with reflog?**

    - Find commit in reflog, checkout or reset to that commit.

11. **How do you manage multiple branches simultaneously?**

    - Use git worktree for separate working directories.

12. **When should you use git stash vs commit?**

    - Stash for temporary storage, commit for permanent changes.

13. **How do you update all submodules?**

    - `git submodule update --remote --merge`.

14. **What is the difference between `git diff` and `git diff --staged`?**

    - Diff shows unstaged changes, --staged shows staged changes.

15. **How do you search commits by message?**

    - `git log --grep="search term"`.

16. **What is the `--no-commit` flag in cherry-pick?**

    - Applies changes without creating a commit.

### Senior (10-15)
17. **How would you use bisect with automated testing?**

    - Use `git bisect run` with test script to automate process.

18. **What are the limitations of git reflog?**

    - Only local, expires after 90 days by default.

19. **How do you handle merge conflicts with worktree?**

    - Resolve in one worktree, commit, then update others.

20. **What is the impact of submodules on CI/CD?**

    - Need to initialize and update, can cause build failures.

21. **How do you implement a hotfix workflow with worktree?**

    - Create worktree for hotfix, fix issue, merge, cleanup.

22. **What is the difference between `git reset` modes?**

    - Soft (staged), mixed (unstaged), hard (discard).

23. **How do you clean up repository history?**

    - Use rebase, filter-branch, or BFG Repo-Cleaner.

24. **What is the role of reflog in disaster recovery?**

    - Tracks all HEAD movements, allows recovery of lost commits.

### FAANG-style (5-10)
25. **Design a debugging workflow for a production issue.**

    - Reproduce, bisect, fix, test, deploy, monitor.

26. **How would you handle a corrupted repository?**

    - fsck, reflog recovery, clone from backup, BFG cleaner.

27. **What are the trade-offs between submodules and monorepo?**

    - Submodules: independent, complex. Monorepo: unified, simpler.

28. **How do you manage 100+ submodules?**

    - Automation, documentation, CI/CD integration, version pinning.

29. **Design a system for automated git operations.**

    - Scripts, hooks, CI/CD integration, monitoring, rollback.

### Follow-ups (5-10)
30. **How does git bisect handle non-deterministic failures?**

    - Use `--skip` to skip flaky tests, run multiple times.

31. **What happens if you delete a branch referenced in reflog?**

    - Reflog still contains commits, can be recovered.

32. **How do you handle submodule version conflicts?**

    - Update to compatible versions, test thoroughly.

33. **What is the future of git submodules?**

    - Git subtree, monorepos, package managers gaining popularity.

34. **How do you implement git operations in CI/CD?**

    - Use Git tokens, SSH keys, automated workflows.

## Summary
Git advanced commands provide powerful tools for debugging, recovery, and complex workflows. Master bisect for debugging, reflog for recovery, worktree for parallel work, and understand when to use revert vs reset. Practice these commands in safe environments before using in production.

## References & Learn More

- [Git Documentation](https://git-scm.com/docs)
- [Git Bisect](https://git-scm.com/docs/git-bisect)
- [Git Reflog](https://git-scm.com/docs/git-reflog)
- [Git Worktree](https://git-scm.com/docs/git-worktree)
- [Git Submodule](https://git-scm.com/docs/git-submodule)