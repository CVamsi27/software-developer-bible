# Monorepo Interview Questions

## Definition
This comprehensive guide covers 20 interview questions on monorepo architecture, from fundamentals to advanced system design.

## Why Do We Need It?
- **Technical Interviews**: Monorepo is a modern development strategy
- **System Design**: Understanding monorepo architecture is crucial
- **Team Collaboration**: Monorepo impacts team workflows
- **Build Optimization**: Performance is a key interview topic

## How It Works

```text
Interview Question Categories:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Fundamentals│  │   Tooling   │  │      System Design      │ │
│  │             │  │             │  │                         │ │
│  │ • Concepts  │  │ • Turborepo │  │ • Architecture          │ │
│  │ • Benefits  │  │ • Nx        │  │ • Migration             │ │
│  │ • Trade-offs│  │ • Lerna     │  │ • Scaling               │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Common Interview Answer Patterns

```typescript
// Pattern 1: Concept → Benefits → Challenges → Trade-offs
function answerPattern(concept: string): string {
  return `
    1. Concept: What ${concept} is
    2. Benefits: Why we use it
    3. Challenges: What makes it difficult
    4. Trade-offs: What we gain vs lose
  `;
}

// Pattern 2: Problem → Solution → Implementation
function solutionPattern(problem: string): string {
  return `
    1. Problem: ${problem}
    2. Solution: Monorepo approach
    3. Implementation: Tools and patterns
    4. Considerations: Performance, team, scale
  `;
}
```

## Interview Questions

### Beginner (5)

**Q1: What is a monorepo?**
- **Answer**: A software development strategy where code for multiple projects is stored in a single repository, enabling code sharing, atomic changes, and consistent dependencies.

**Q2: What are the benefits of a monorepo?**
- **Answer**: Code sharing, atomic changes, consistent dependencies, simplified refactoring, better code review, unified CI/CD.

**Q3: What is the difference between monorepo and polyrepo?**
- **Answer**: Monorepo stores all code in one repository with shared dependencies; polyrepo stores each project in separate repositories with independent dependencies.

**Q4: What are npm/yarn/pnpm workspaces?**
- **Answer**: Package manager features that enable managing multiple packages in a single repository with shared dependencies and hoisting.

**Q5: What is the workspace protocol?**
- **Answer**: Using `workspace:*` in package.json to reference local packages instead of published versions, enabling development without publishing.

### Intermediate (5)

**Q6: How do you structure a monorepo?**
- **Answer**:
  - `packages/` - Shared libraries
  - `apps/` - Deployable applications
  - `tools/` - Build tools and configurations
  - Clear naming conventions and package boundaries

**Q7: What are the challenges of monorepos?**
- **Answer**: Build performance, tooling complexity, team coordination, CI/CD complexity, code ownership, and learning curve.

**Q8: How do you handle versioning in a monorepo?**
- **Answer**: Use Changesets for coordinated versioning, or independent versioning per package. Consider semantic versioning and release strategies.

**Q9: What is the difference between Turborepo and Nx?**
- **Answer**:
  - Turborepo: Lightweight, focuses on caching and parallelization
  - Nx: Full-featured with generators, affected analysis, and plugins

**Q10: How do you manage dependencies in a monorepo?**
- **Answer**: Use workspace protocol for local packages, hoist common dependencies, maintain consistent versions, and avoid circular dependencies.

### Senior (10)

**Q11: How do you optimize build performance in a monorepo?**
- **Answer**:
  - Use caching (Turborepo/Nx)
  - Parallelize independent tasks
  - Incremental builds
  - Affected commands
  - Remote caching

**Q12: How do you handle circular dependencies?**
- **Answer**:
  - Restructure packages
  - Extract shared code to new package
  - Use dependency injection
  - Refactor to break the cycle

**Q13: What is the strangler fig pattern in monorepo migration?**
- **Answer**: Gradually migrating from polyrepo to monorepo by moving packages incrementally while maintaining both systems during transition.

**Q14: How do you enforce architectural boundaries?**
- **Answer**:
  - Use tags (Nx) or directory structure
  - Configure linting rules
  - Use dependency constraints
  - Regular dependency graph reviews

**Q15: How do you handle code ownership in a monorepo?**
- **Answer**: Use CODEOWNERS file, package-level ownership, clear documentation, and team boundaries.

**Q16: How do you handle database migrations in a monorepo?**
- **Answer**: Shared migration directory, version-controlled schemas, coordinated migrations, and migration tooling.

**Q17: How do you test in a monorepo?**
- **Answer**:
  - Unit tests per package
  - Integration tests across packages
  - End-to-end tests for apps
  - Use affected commands for efficiency

**Q18: How do you handle different TypeScript versions?**
- **Answer**: Use a shared TypeScript version, or isolate packages with their own TypeScript configurations and tooling.

**Q19: How do you handle monorepo in distributed teams?**
- **Answer**:
  - Clear ownership with CODEOWNERS
  - Documentation and onboarding
  - Automated tooling
  - Communication guidelines

**Q20: How do you migrate from Lerna to Turborepo/Nx?**
- **Answer**:
  - Keep package structure
  - Replace Lerna commands
  - Configure new tooling
  - Update CI/CD
  - Test thoroughly

### FAANG-style (5)

**Q21: Design a monorepo architecture for a large organization**
- **Answer**:
  - Package structure with clear boundaries
  - Tooling (Turborepo/Nx) with remote caching
  - CI/CD with affected-based builds
  - Monitoring and alerting
  - Developer documentation

**Q22: How would you migrate from polyrepo to monorepo?**
- **Answer**:
  - Phase 1: Set up monorepo structure
  - Phase 2: Move shared packages
  - Phase 3: Migrate applications
  - Phase 4: Update CI/CD
  - Phase 5: Deprecate old repositories

**Q23: Explain monorepo at scale**
- **Answer**:
  - Thousands of packages
  - Hundreds of developers
  - Multiple programming languages
  - Distributed builds
  - Advanced caching strategies

**Q24: How do you handle monorepo security?**
- **Answer**:
  - Dependency scanning
  - Secret management
  - Access control per package
  - Audit logging
  - Vulnerability detection

**Q25: Design a CI/CD pipeline for a monorepo**
- **Answer**:
  - Detect changes (affected packages)
  - Run tests for affected packages
  - Build with caching
  - Deploy only changed applications
  - Coordinate releases

### Follow-ups (5)

**Q26: How do you handle monorepo with multiple programming languages?**
- **Answer**: Use language-agnostic tooling, separate build systems per language, shared configuration where possible.

**Q27: What is the impact of monorepo on developer experience?**
- **Answer**: Single clone, easy code navigation, atomic changes, but potential complexity with tooling and learning curve.

**Q28: How do you handle monorepo in distributed teams?**
- **Answer**: Clear ownership, documentation, CODEOWNERS, automated testing, and communication guidelines.

**Q29: What are the alternatives to monorepo?**
- **Answer**: Polyrepo, multi-repo, or hybrid approaches with shared packages via npm/registry.

**Q30: How do you optimize monorepo for large teams?**
- **Answer**: Clear package boundaries, ownership, documentation, automated tooling, and effective communication.

## Best Practices for Interview Answers

### Structure Your Answer
```text
1. Definition (1-2 sentences)
2. Benefits (2-3 bullet points)
3. Challenges (2-3 bullet points)
4. Implementation (tools and patterns)
5. Trade-offs (what we gain vs lose)
```

### Key Concepts to Master

| Concept | Key Points |
|---------|------------|
| Workspaces | Package manager feature for monorepos |
| Caching | Turborepo/Nx computation caching |
| Affected | Only run tasks for changed packages |
| Generators | Code scaffolding tools |
| Dependency Graph | Visualization of project relationships |
| Versioning | Coordinated or independent versioning |
| CI/CD | Affected-based pipelines |

### Common Follow-up Questions
- "How would you implement this in production?"
- "What are the cost implications?"
- "How do you handle failures?"
- "What are the alternatives?"
- "How do you test this?"

## Summary

Monorepo provides a unified approach to managing multiple projects with shared code and dependencies. Master the concepts, tools, and trade-offs to excel in interviews.

## References & Learn More

- [Turborepo Documentation](https://turborepo.org/docs)
- [Nx Documentation](https://nx.dev/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Yarn Workspaces](https://classic.yarnpkg.com/en/docs/workspaces)
- [Monorepo by Example](https://monorepo.tools/)
