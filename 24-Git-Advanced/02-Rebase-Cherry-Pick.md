# Rebase & Cherry-Pick

## Definition
- **Rebase**: A Git operation that reapplies commits on top of another base tip, creating a linear history
- **Cherry-pick**: A Git operation that applies a specific commit from one branch to another

## Why Do We Need Them?
- **Rebase**: Clean, linear history without merge commits
- **Cherry-pick**: Apply specific fixes to multiple branches without merging entire branches
- Both help maintain clean project history and manage complex development workflows

## How It Works

### Rebase Flow
```
Before Rebase:
main:      A---B---C---D
                  \
feature:           E---F---G

After Rebase:
main:      A---B---C---D
                        \
feature:                 E'---F'---G'
```

### Cherry-Pick Flow
```
Before Cherry-Pick:
main:      A---B---C---D
                  \
feature:           E---F---G

After Cherry-Pick (commit E to main):
main:      A---B---C---D---E'
                  \
feature:           E---F---G
```

## Code Examples

### Basic Rebase
```bash
# Rebase feature branch onto main
git checkout feature
git rebase main

# Resolve conflicts during rebase
# After resolving conflicts:
git add .
git rebase --continue

# Abort rebase if needed
git rebase --abort

# Skip a commit during rebase
git rebase --skip
```

### Interactive Rebase
```bash
# Interactive rebase last 3 commits
git rebase -i HEAD~3

# In editor:
pick abc1234 First commit
pick def5678 Second commit
pick ghi9012 Third commit

# Commands:
# pick = keep commit as is
# reword = change commit message
# edit = amend commit
# squash = combine with previous commit
# fixup = like squash but discard commit message
# drop = remove commit
```

### Rebase vs Merge
```bash
# Merge (preserves history)
git checkout main
git merge --no-ff feature

# Rebase (linear history)
git checkout feature
git rebase main
git checkout main
git merge feature  # Fast-forward merge
```

### Cherry-Pick Single Commit
```bash
# Cherry-pick a specific commit
git cherry-pick abc1234

# Cherry-pick multiple commits
git cherry-pick abc1234 def5678 ghi9012

# Cherry-pick range of commits
git cherry-pick abc1234..ghi9012

# Cherry-pick without committing
git cherry-pick --no-commit abc1234
```

### Cherry-Pick from Another Branch
```bash
# Cherry-pick from specific branch
git cherry-pick feature~2  # Second commit from tip of feature
git cherry-pick feature^   # First parent of feature tip

# Cherry-pick merge commit
git cherry-pick -m 1 <merge-commit-hash>
```

### Squash Commits
```bash
# Interactive rebase to squash
git rebase -i HEAD~5

# Mark commits to squash
pick abc1234 Feature commit 1
squash def5678 Feature commit 2
squash ghi9012 Feature commit 3

# Or use squash flag directly
git merge --squash feature
git commit -m "Feature: combine all changes"
```

### Rebase with Upstream
```bash
# Rebase onto remote main
git fetch origin
git rebase origin/main

# Rebase with autostash
git rebase --autostash origin/main

# Set upstream tracking
git branch --set-upstream-to=origin/main feature
```

### Resolving Rebase Conflicts
```bash
# During rebase, conflicts occur
# 1. Edit conflicted files
# 2. Stage resolved files
git add .

# 3. Continue rebase
git rebase --continue

# Or abort if needed
git rebase --abort
```

## Real-World Use Cases
1. **Keeping feature branches updated**: Rebase feature onto main regularly
2. **Applying hotfixes**: Cherry-pick fix to multiple release branches
3. **Cleaning up history**: Interactive rebase before merging
4. **Selective feature deployment**: Cherry-pick specific features
5. **Release management**: Cherry-pick only needed commits to release

## Common Mistakes
1. **Rebasing public branches**: Never rebase commits that have been pushed
2. **Losing work**: Always backup before rebase/cherry-pick
3. **Not testing after operations**: Always test after rebase or cherry-pick
4. **Overusing interactive rebase**: Can be time-consuming
5. **Not resolving conflicts properly**: Can introduce bugs
6. **Cherry-picking merge commits**: Requires `-m` flag
7. **Ignoring upstream changes**: Always fetch before rebase

## Best Practices
1. **Rebase local branches only**: Don't rebase pushed commits
2. **Use interactive rebase for cleanup**: Before merging feature branches
3. **Cherry-pick carefully**: Ensure context is correct
4. **Test thoroughly**: After any rebase or cherry-pick
5. **Communicate with team**: When rewriting history
6. **Use autostash**: For convenience during rebase
7. **Keep commits atomic**: Easier to cherry-pick
8. **Document cherry-picks**: Track applied commits

## Performance Considerations
- **Rebase**: Can be slow with many commits
- **Cherry-pick**: Fast for individual commits
- **Interactive rebase**: Requires manual intervention
- **Conflict resolution**: Can be time-consuming
- **Large repositories**: Consider shallow clones

## Interview Questions

### Beginner (5-10)
1. **What is git rebase?**
   - Reapplies commits on top of another base, creating linear history.

2. **What is git cherry-pick?**
   - Applies a specific commit from one branch to another.

3. **What is the difference between rebase and merge?**
   - Rebase creates linear history, merge preserves branch history.

4. **When should you use rebase?**
   - When you want clean, linear history without merge commits.

5. **When should you use cherry-pick?**
   - When you need to apply specific commits to other branches.

6. **What is interactive rebase?**
   - Rebase that allows editing, squashing, or dropping commits.

7. **What is the `-m` flag in cherry-pick?**
   - Specifies which parent to use when cherry-picking a merge commit.

8. **How do you abort a rebase?**
   - `git rebase --abort` returns to the original state.

### Intermediate (5-10)
9. **What happens to commits during rebase?**
   - New commits are created with different hashes but same changes.

10. **How do you resolve conflicts during rebase?**
    - Edit files, stage changes, continue rebase with `git rebase --continue`.

11. **What is the difference between `git merge --squash` and `git rebase -i`?**
    - Squash combines all changes into one commit, interactive rebase allows selective squashing.

12. **How do you cherry-pick a range of commits?**
    - `git cherry-pick start..end` or `git cherry-pick start^..end`.

13. **What is autostash in rebase?**
    - Automatically stashes changes before rebase and applies after.

14. **How do you track cherry-picked commits?**
    - Cherry-picked commits have different hashes, track manually or use `git log --cherry`.

15. **What is the difference between `git pull` and `git pull --rebase`?**
    - Pull --rebase rebases your changes on top of remote changes.

16. **How do you rebase onto a different branch?**
    - `git rebase --onto newbase oldbase branch`.

### Senior (10-15)
17. **When should you never rebase?**
    - Never rebase commits that have been pushed to a shared repository.

18. **How does rebase affect commit hashes?**
    - All rebased commits get new hashes, breaking references.

19. **What is the `--onto` flag in rebase?**
    - Rebases commits from one branch onto another, excluding commits from a third branch.

20. **How do you handle cherry-pick conflicts?**
    - Same as merge conflicts: resolve, stage, continue cherry-pick.

21. **What is the difference between `git revert` and `git reset`?**
    - Revert creates new commit that undoes changes, reset moves HEAD.

22. **How do you cherry-pick multiple branches?**
    - Iterate through branches or use a script to cherry-pick commits.

23. **What is the impact of rebase on pull requests?**
    - Can make review difficult, prefer merge for PRs.

24. **How do you handle upstream changes during rebase?**
    - Fetch first, then rebase onto upstream branch.

### FAANG-style (5-10)
25. **Design a workflow for applying hotfixes to multiple release branches.**
    - Cherry-pick fix to each branch, test independently, coordinate releases.

26. **How would you handle a large-scale rebase across 100+ branches?**
    - Script the process, test each branch, coordinate with team, have rollback plan.

27. **What are the trade-offs between rebase and merge in large teams?**
    - Rebase: clean history but risky. Merge: safe but messy history.

28. **How do you implement a feature flag system with cherry-pick?**
    - Cherry-pick feature flag code, enable/disable via configuration.

29. **Design a system to track cherry-picked commits across branches.**
    - Use commit message markers, database tracking, or Git hooks.

### Follow-ups (5-10)
30. **How does rebase handle merge commits?**
    - Skips merge commits unless specified with `-m`.

31. **What is the difference between `git rebase` and `git rebase -i`?**
    - Interactive allows editing commits, regular just replays them.

32. **How do you undo a cherry-pick?**
    - `git revert <cherry-picked-commit-hash>`.

33. **What is the `--no-commit` flag in cherry-pick?**
    - Applies changes without creating a commit.

34. **How do you handle binary files during rebase?**
    - Same as text files, but conflicts may require manual resolution.

## Summary
Rebase and cherry-pick are powerful Git operations for managing history and applying specific changes. Rebase creates clean, linear history while cherry-pick allows selective commit application. Use them carefully, especially on shared branches, and always test after applying these operations.

## References & Learn More
- [Git Rebase Documentation](https://git-scm.com/docs/git-rebase)
- [Git Cherry-pick Documentation](https://git-scm.com/docs/git-cherry-pick)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Pro Git Book](https://git-scm.com/book/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)