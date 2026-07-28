---
section: Git Advanced
category: Reference
tags: [concept]
---

# Branching Strategies

## Definition
A branching strategy is a framework that defines how branches are created, named, merged, and deleted in a version control system. It provides a structured approach to managing parallel development, releases, and collaboration.

## Why Do We Need It?
Without a branching strategy:

- **Chaos**: Multiple developers working on same code
- **Merge conflicts**: Frequent, difficult to resolve
- **Release issues**: Unstable code mixed with production
- **Code quality**: No separation of features, fixes, experiments
- **Team coordination**: Unclear workflow and responsibilities

## How It Works
Branching strategies define:

- Which branches to create and when
- How to name branches
- Where to merge branches
- How to handle releases
- How to manage hotfixes

### Branching Strategy Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Branching Strategy Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  main (production)                                              │
│  ────────────────────────────────────────────────────────────── │
│                                                                 │
│  develop (integration)                                          │
│  ────────────────────────────────────────────────────────────── │
│                                                                 │
│  feature/*          release/*           hotfix/*                │
│  ──────────────     ──────────────      ──────────────         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Git Flow

```bash
# Start a new feature
git checkout develop
git checkout -b feature/user-authentication

# Work on feature
git add .
git commit -m "feat: add login form"

# Finish feature
git checkout develop
git merge --no-ff feature/user-authentication
git branch -d feature/user-authentication

# Start release
git checkout -b release/1.0.0 develop

# Finish release
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0
git checkout develop
git merge --no-ff release/1.0.0

# Hotfix
git checkout main
git checkout -b hotfix/fix-security-issue
git commit -m "fix: security vulnerability"
git checkout main
git merge --no-ff hotfix/fix-security-issue
git tag -a v1.0.1
git checkout develop
git merge --no-ff hotfix/fix-security-issue

```

### GitHub Flow

```bash
# Create feature branch
git checkout main
git checkout -b feature/add-shopping-cart

# Make changes
git add .
git commit -m "feat: implement shopping cart"

# Push and create PR
git push origin feature/add-shopping-cart
# Create Pull Request on GitHub

# After review and approval
git checkout main
git merge feature/add-shopping-cart
git push origin main

# Delete branch
git branch -d feature/add-shopping-cart
git push origin --delete feature/add-shopping-cart

```

### Trunk-Based Development

```bash
# Work directly on main (or short-lived branches)
git checkout main

# Make small, frequent commits
git add .
git commit -m "refactor: extract validation logic"

# Push frequently
git push origin main

# For larger changes, use short-lived branches
git checkout -b feature/add-payment-integration
# Work for 1-2 days max
git push origin feature/add-payment-integration
# Create PR, review quickly, merge to main

```

### Release Branching

```bash
# Create release branch from develop
git checkout develop
git checkout -b release/2.0.0

# Prepare release
git commit -m "chore: bump version to 2.0.0"
git commit -m "docs: update CHANGELOG"

# Merge to main and tag
git checkout main
git merge --no-ff release/2.0.0
git tag -a v2.0.0

# Merge back to develop
git checkout develop
git merge --no-ff release/2.0.0

```

### Feature Flags with Branching

```bash
# Feature flag approach
git checkout main
git checkout -b feature/new-checkout-flow

# Implement with feature flag
git commit -m "feat: add new checkout flow with feature flag"

# Merge to main (flag disabled)
git checkout main
git merge feature/new-checkout-flow

# Enable flag when ready
# In code: if (featureFlags.newCheckout) { ... }

```

## Real-World Use Cases

1. **Enterprise Applications**: Git Flow for structured releases

2. **Startup/SaaS**: GitHub Flow for rapid iteration

3. **Large Teams**: Trunk-based with feature flags

4. **Mobile Apps**: Release branching for app store cycles

5. **Open Source**: GitHub Flow with PR reviews

## Common Mistakes

1. **Long-lived feature branches**: Leads to merge conflicts

2. **Not deleting merged branches**: Clutters repository

3. **Poor branch naming**: Unclear purpose

4. **Skipping code reviews**: Reduces code quality

5. **Not testing before merge**: Introduces bugs

6. **Overcomplicating strategy**: Unnecessary complexity

7. **Not documenting conventions**: Team confusion

## Best Practices

1. **Keep branches short-lived**: Merge within 1-2 days

2. **Use descriptive names**: `feature/user-auth`, `fix/login-bug`

3. **Delete merged branches**: Clean repository

4. **Require PR reviews**: Code quality assurance

5. **Test before merge**: Automated CI/CD

6. **Document your strategy**: Team alignment

7. **Use feature flags**: For large features

8. **Automate where possible**: Reduce manual work

## Performance Considerations

- **Branch creation**: Fast, lightweight operation
- **Merge conflicts**: Resolve quickly to avoid delays
- **CI/CD**: Test each branch/PR
- **Repository size**: Avoid large binary files in branches
- **Pull request size**: Keep small for easier reviews

## Summary
Branching strategies are essential for managing code changes in teams. Choose a strategy based on your team size, release cadence, and deployment process. Common strategies include Git Flow, GitHub Flow, and trunk-based development. The key is consistency and team alignment.

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Monorepo](../28-Monorepo/)

## References & Learn More

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Git Documentation](https://git-scm.com/docs)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
