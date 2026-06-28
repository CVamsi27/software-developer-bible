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

## Interview Questions

### Beginner (5-10)
1. **What is a branching strategy?**
   - Framework for managing branches in version control.

2. **Why do we need branching strategies?**
   - To coordinate parallel development, manage releases, and maintain code quality.

3. **What is the difference between Git Flow and GitHub Flow?**
   - Git Flow has multiple branch types (feature, release, hotfix), GitHub Flow is simpler with feature branches and main.

4. **What is a feature branch?**
   - Temporary branch for developing new features, merged to main after review.

5. **What is a release branch?**
   - Branch used to prepare a new release, isolated from ongoing development.

6. **What is a hotfix branch?**
   - Quick fix for production issues, merged to both main and develop.

7. **How do you delete a branch in Git?**
   - `git branch -d branch-name` (local), `git push origin --delete branch-name` (remote).

8. **What is `--no-ff` in merge?**
   - Forces a merge commit, preserving branch history.

### Intermediate (5-10)
9. **When should you use Git Flow?**
   - For projects with scheduled releases, multiple versions, or strict release cycles.

10. **When should you use GitHub Flow?**
    - For continuous deployment, web applications, rapid iteration.

11. **What is trunk-based development?**
    - Development directly on main or short-lived branches, with frequent integration.

12. **How do you handle merge conflicts?**
    - Resolve locally, communicate with team, test thoroughly before pushing.

13. **What are feature flags?**
    - Code mechanisms to enable/disable features without deploying new code.

14. **How do you manage multiple parallel releases?**
    - Use release branches, cherry-pick commits, or version-specific branches.

15. **What is `git pull --rebase`?**
    - Rebase your changes on top of remote changes, creating linear history.

16. **How do you revert a merged branch?**
    - Use `git revert` to create undo commits, not `git reset`.

### Senior (10-15)
17. **How do you choose a branching strategy for a team?**
    - Consider: release cadence, team size, risk tolerance, deployment process.

18. **How do you implement trunk-based development safely?**
    - Feature flags, comprehensive testing, small changes, feature branches.

19. **What is the impact of branching strategy on CI/CD?**
    - Determines when tests run, how deployments happen, release frequency.

20. **How do you handle database migrations with branching?**
    - Separate migration files, backward-compatible changes, migration testing.

21. **What is the difference between merge, rebase, and squash?**
    - Merge: preserves history, creates merge commit. Rebase: linear history. Squash: combines commits.

22. **How do you manage branching for microservices?**
    - Independent branches per service, coordinated releases, API versioning.

23. **What is the role of code reviews in branching strategies?**
    - Quality assurance, knowledge sharing, catching issues early.

24. **How do you handle long-lived branches?**
    - Avoid when possible, rebase frequently, merge often.

### FAANG-style (5-10)
25. **Design a branching strategy for a team of 50 engineers across 5 services.**
    - Consider: service independence, coordinated releases, shared libraries, testing strategy.

26. **How would you implement continuous deployment with feature flags?**
    - Short-lived branches, feature flags, automated testing, gradual rollouts.

27. **What are the trade-offs between Git Flow and trunk-based development?**
    - Release flexibility vs complexity, safety vs speed, history vs simplicity.

28. **How do you handle branching for mobile app development?**
    - Release branches for app store, feature branches for development, beta testing.

29. **Design a branching strategy for a regulated industry (healthcare, finance).**
    - Audit trails, compliance requirements, release approvals, documentation.

### Follow-ups (5-10)
30. **How does branching strategy evolve as a team grows?**
    - From simple to more structured, add automation, documentation, training.

31. **What metrics indicate a good branching strategy?**
    - Low merge conflict rate, fast integration, quick releases, high code quality.

32. **How do you handle branching for open source projects?**
    - Fork-based workflow, PR reviews, contributor guidelines, release tagging.

33. **What is the impact of branching strategy on developer experience?**
    - Affects workflow complexity, merge frequency, release process.

34. **How do you migrate from one branching strategy to another?**
    - Gradual transition, team training, documentation, tooling updates.

## Summary
Branching strategies are essential for managing code changes in teams. Choose a strategy based on your team size, release cadence, and deployment process. Common strategies include Git Flow, GitHub Flow, and trunk-based development. The key is consistency and team alignment.

## References & Learn More
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Git Documentation](https://git-scm.com/docs)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)