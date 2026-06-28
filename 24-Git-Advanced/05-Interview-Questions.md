# Git Advanced Interview Questions

## Comprehensive Interview Guide

This chapter contains 30 carefully curated interview questions covering advanced Git concepts, workflows, and commands. Questions are organized by difficulty level and include detailed answers.

---

## Beginner (5-10)

### 1. What is the difference between git merge and git rebase?
**Answer:**
- **Merge**: Preserves branch history, creates merge commit
- **Rebase**: Creates linear history, reapplies commits with new hashes

```bash
# Merge
git checkout main
git merge feature

# Rebase
git checkout feature
git rebase main
```

### 2. What is git stash and when should you use it?
**Answer:**
Git stash temporarily stores modified tracked files:
```bash
# Stash changes
git stash push -m "Work in progress"

# List stashes
git stash list

# Apply and remove
git stash pop
```
Use when:
- Switching branches with uncommitted changes
- Pulling changes without committing
- Testing something quickly

### 3. What is git cherry-pick and how does it work?
**Answer:**
Applies a specific commit from one branch to another:
```bash
# Cherry-pick a commit
git cherry-pick abc1234

# Cherry-pick without committing
git cherry-pick --no-commit abc1234
```
Use for:
- Applying hotfixes to multiple branches
- Selective feature deployment
- Recovering lost commits

### 4. What is git bisect?
**Answer:**
Binary search tool to find which commit introduced a bug:
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out middle commit
# Test, then mark as good or bad
git bisect reset
```

### 5. What is git reflog?
**Answer:**
Reference log showing all HEAD movements:
```bash
# Show reflog
git reflog

# Recover lost commit
git reflog
git checkout abc1234
```

### 6. What is the difference between git revert and git reset?
**Answer:**
- **Revert**: Creates new commit that undoes changes (safe for shared branches)
- **Reset**: Moves HEAD, can discard changes (dangerous for shared branches)

```bash
# Revert
git revert abc1234

# Reset
git reset --hard abc1234  # Discards changes
git reset --soft abc1234  # Keeps changes staged
```

### 7. What is git worktree?
**Answer:**
Multiple working directories attached to same repository:
```bash
# Add worktree
git worktree add ../hotfix-branch hotfix/1.0.1

# List worktrees
git worktree list
```

### 8. What is git submodule?
**Answer:**
Repository embedded inside another repository:
```bash
# Add submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# Update submodules
git submodule update --remote
```

---

## Intermediate (5-10)

### 9. How do you resolve merge conflicts during rebase?
**Answer:**
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

### 10. What is interactive rebase and when should you use it?
**Answer:**
Rebase that allows editing, squashing, or dropping commits:
```bash
# Interactive rebase last 3 commits
git rebase -i HEAD~3

# Commands:
# pick = keep commit
# squash = combine with previous
# reword = change message
# edit = amend commit
# drop = remove commit
```
Use to:
- Clean up commit history before merging
- Combine related commits
- Remove accidental commits

### 11. How do you handle large files in Git?
**Answer:**
```bash
# Use Git LFS
git lfs install
git lfs track "*.psd"
git add .gitattributes

# Or use .gitignore
echo "*.zip" >> .gitignore
```

### 12. What is git subtree?
**Answer:**
Alternative to submodules, merges external repository into subtree:
```bash
# Add subtree
git subtree add --prefix=lib/vendor https://github.com/user/repo.git main --squash

# Update subtree
git subtree pull --prefix=lib/vendor https://github.com/user/repo.git main --squash
```

### 13. How do you find which commit introduced a bug?
**Answer:**
```bash
# Manual bisection
git log --oneline
git checkout abc1234
# Test if bug exists
git checkout def5678
# Test again

# Or use bisect
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run npm test
```

### 14. What is git blame and when to use it?
**Answer:**
Shows who changed each line and when:
```bash
# Show blame
git blame path/to/file

# Show with line ranges
git blame -L 10,20 path/to/file
```
Use to:
- Find who introduced a bug
- Understand code history
- Contact author for context

### 15. How do you clean up repository history?
**Answer:**
```bash
# Interactive rebase
git rebase -i HEAD~5

# Remove large files from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file' \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner
java -jar bfg.jar --strip-blobs-bigger-than 10M repo.git
```

### 16. What is git sparse-checkout?
**Answer:**
Partial checkout of repository contents:
```bash
# Enable sparse checkout
git sparse-checkout init

# Set pattern
git sparse-checkout set src/ docs/
```

### 17. How do you handle multiple remotes?
**Answer:**
```bash
# Add remote
git remote add upstream https://github.com/original/repo.git

# Fetch from all remotes
git fetch --all

# Push to specific remote
git push origin main
git push upstream main
```

### 18. What is the difference between git pull and git pull --rebase?
**Answer:**
- **git pull**: Fetches and merges remote changes
- **git pull --rebase**: Fetches and rebases your changes on top

```bash
# Default
git pull origin main

# Rebase
git pull --rebase origin main
```

---

## Senior (10-15)

### 19. How do you implement a Git workflow for a large team?
**Answer:**
Considerations:
- Branching strategy (Git Flow, GitHub Flow)
- Code review process
- CI/CD integration
- Release management
- Hotfix process

```yaml
# Example workflow
branches:
  main: production
  develop: integration
  feature/*: feature development
  release/*: release preparation
  hotfix/*: emergency fixes
```

### 20. What is the impact of force pushing?
**Answer:**
```bash
# Force push overwrites remote history
git push --force origin feature

# Safer alternative
git push --force-with-lease origin feature
```
Risks:
- Loses commits for collaborators
- Breaks pull requests
- Can cause data loss

### 21. How do you handle monorepos with Git?
**Answer:**
```bash
# Sparse checkout
git sparse-checkout init
git sparse-checkout set packages/my-package/

# Or use Git worktrees
git worktree add ../package-a package-a

# Or use subtrees
git subtree add --prefix=packages/shared https://github.com/user/shared.git main
```

### 22. What is git notes?
**Answer:**
Attach metadata to commits without modifying them:
```bash
# Add note
git notes add -m "Reviewed by senior dev" abc1234

# Show notes
git show abc1234

# Push notes
git push origin refs/notes/*
```

### 23. How do you implement Git hooks for CI/CD?
**Answer:**
```bash
#!/bin/sh
# .git/hooks/pre-push

# Run tests
npm test

# Check for secrets
if grep -r "password" .; then
  echo "Secrets detected!"
  exit 1
fi
```

### 24. What is git bundle?
**Answer:**
Pack objects into single file for transfer:
```bash
# Create bundle
git bundle create repo.bundle HEAD main

# Clone from bundle
git clone repo.bundle

# Verify bundle
git bundle verify repo.bundle
```

### 25. How do you handle Git in CI/CD pipelines?
**Answer:**
```yaml
# GitHub Actions example
steps:
  - uses: actions/checkout@v3
    with:
      fetch-depth: 0  # Full history for analysis

  - name: Setup Git
    run: |
      git config user.name "CI Bot"
      git config user.email "ci@example.com"
```

### 26. What is the difference between git fetch and git pull?
**Answer:**
- **Fetch**: Downloads remote changes, doesn't modify working directory
- **Fetch + merge**: What git pull does

```bash
# Fetch only
git fetch origin

# Then merge manually
git merge origin/main
```

### 27. How do you manage Git permissions?
**Answer:**
```bash
# GitHub: Use branch protection rules
# GitLab: Use protected branches
# Server-side hooks

# Check permissions
git config --get user.name
git config --get user.email
```

### 28. What is git archive?
**Answer:**
Create archive of repository contents:
```bash
# Create zip
git archive --format=zip HEAD -o archive.zip

# Create tar
git archive --format=tar HEAD -o archive.tar
```

### 29. How do you handle Git in containerized environments?
**Answer:**
```dockerfile
# Dockerfile
FROM alpine:latest
RUN apk add --no-cache git
COPY .git /app/.git
WORKDIR /app
RUN git checkout main
```

### 30. What is the future of Git?
**Answer:**
- Better monorepo support
- Improved performance
- Better integration with CI/CD
- Enhanced security features
- Cloud-native workflows

---

## FAANG-style (5-10)

### 31. Design a Git workflow for a 100+ engineer team.
**Answer:**
Considerations:
- Service ownership
- Release coordination
- Cross-team dependencies
- Code review at scale
- Automated testing

```yaml
workflow:
  branching: trunk-based
  feature_flags: true
  code_review: required
  ci_cd: automated
  release: weekly
  hotfix: immediate
```

### 32. How would you handle a corrupted Git repository?
**Answer:**
```bash
# Check for corruption
git fsck

# Recover from reflog
git reflog
git checkout abc1234

# Clone from backup
git clone /path/to/backup repo.git

# Use BFG for cleanup
java -jar bfg.jar --strip-blobs-bigger-than 10M repo.git
```

### 33. What are the trade-offs between Git and other VCS?
**Answer:**
| Feature | Git | SVN | Mercurial |
|---------|-----|-----|-----------|
| **Speed** | Fast | Slow | Fast |
| **Branching** | Excellent | Poor | Good |
| **Learning Curve** | Steep | Moderate | Moderate |
| **Large Files** | Poor | Good | Good |
| **Distributed** | Yes | No | Yes |

### 34. How would you migrate a large repository to Git?
**Answer:**
```bash
# Using git svn
git svn clone --stdlayout --authors-file=authors.txt http://svn.example.com/repo

# Or using svn2git
svn2git http://svn.example.com/repo --authors authors.txt

# Or using git-tfs
git tfs clone http://tfs.example.com/tfs/Collection $/Project
```

### 35. Design a Git backup and disaster recovery system.
**Answer:**
```bash
# Automated backup script
#!/bin/bash
git bundle create backup-$(date +%Y%m%d).bundle --all

# Verify backup
git bundle verify backup-$(date +%Y%m%d).bundle

# Upload to cloud
aws s3 cp backup-$(date +%Y%m%d).bucket s3://backups/
```

---

## Follow-ups (5-10)

### 36. How does Git handle binary files?
**Answer:**
- Stores full copy for each version
- Can use Git LFS for large files
- Delta compression doesn't work well

### 37. What is the difference between git merge and git rebase historically?
**Answer:**
- Merge: Traditional, preserves history
- Rebase: Newer, linear history
- Both valid, use based on context

### 38. How do you handle Git in a microservices architecture?
**Answer:**
```yaml
# Per-service repository
services:
  auth:
    repo: github.com/org/auth
  payment:
    repo: github.com/org/payment

# Or monorepo with sparse checkout
monorepo:
  sparse_checkout: true
  packages: ["services/*"]
```

### 39. What is the impact of Git on developer productivity?
**Answer:**
- Fast branching enables experimentation
- Local commits enable offline work
- Powerful merging reduces conflicts
- Rich history enables debugging

### 40. How do you train team members on advanced Git?
**Answer:**
- Hands-on workshops
- Real-world exercises
- Documentation
- Code reviews
- Pair programming
- Git workshops

## Summary
Advanced Git commands are essential for complex development workflows. Master bisect for debugging, reflog for recovery, and understand when to use revert vs reset. Practice these commands and understand their implications for team collaboration.

## References & Learn More
- [Git Documentation](https://git-scm.com/docs)
- [Pro Git Book](https://git-scm.com/book/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Git Tips](https://github.com/git-tips/tips)