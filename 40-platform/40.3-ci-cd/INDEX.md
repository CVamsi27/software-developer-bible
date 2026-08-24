# CI/CD — Index

> **8 files** — CI/CD pipeline fundamentals from GitHub Actions and Jenkins to GitLab CI, ArgoCD, Docker build/deploy, blue-green/canary deployments, pipeline patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why CI/CD:** Every senior engineer owns their pipeline. You must know how to set up GitHub Actions (or GitLab CI), build a Docker image, push to a registry, and deploy to a target. Blue-green and canary deployments are the senior-level patterns. GitOps (ArgoCD) is increasingly common.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [CI Tools](#ci-tools) | 4 | GitHub Actions, Jenkins, GitLab CI, ArgoCD — pick the one your company uses |
| [Build & Deploy](#build--deploy) | 2 | Docker build/deploy, pipeline patterns — the runtime |
| [Deployment Strategies](#deployment-strategies) | 1 | Blue-green, canary, rolling — the senior-level patterns |
| [Interview Prep](#interview-prep) | 1 | 50+ Qs |

---

## CI Tools

Pick the one your company uses — the patterns are similar.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 01 | [GitHub Actions](40.3.01-github-actions.md) | Workflows, actions, runners, matrix builds, caching, secrets | Most common — GitHub repos | 30 min |
| 04 | [Jenkins CI/CD](40.3.04-jenkins.md) | Declarative/scripted pipelines, shared libraries, plugins | Legacy enterprise | 25 min |
| 05 | [GitLab CI/CD](40.3.05-gitlab-ci.md) | `.gitlab-ci.yml`, multi-project pipelines, Auto DevOps | GitLab repos | 25 min |
| 06 | [ArgoCD (GitOps)](40.3.06-argocd.md) | GitOps, ApplicationSets, sync policies, rollback | K8s + GitOps | 25 min |

---

## Build & Deploy

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [Docker Build & Deploy](40.3.02-docker-build-deploy.md) | Docker build pipelines, registry (ECR/GCR/DockerHub), deployment strategies | 30 min |
| 08 | [Pipeline Patterns](40.3.08-pipeline-patterns.md) | GitHub Actions CI/CD, GitLab CI, deployment pipelines, deployment strategies (rolling, blue-green, canary, feature flags) | 30 min |

---

## Deployment Strategies

Senior-level patterns for zero-downtime deploys.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Blue-Green & Canary](40.3.03-blue-green-canary.md) | Zero-downtime deployments, traffic shifting, rollback, feature flags | 25 min |

**Decision:**

```text
Need zero-downtime deployment?
├── Big-bang deploy is OK? ──→ Rolling update (default)
├── Need instant rollback? ──→ Blue-green
├── Want gradual risk reduction? ──→ Canary
└── Want to test in production? ──→ Feature flags
```

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [Interview Questions](40.3.07-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## Suggested Study Order

1. **GitHub Actions** (or GitLab CI if your JD requires) — must know
2. **Docker Build & Deploy** — must know
3. **Pipeline Patterns** — senior level
4. **Blue-Green & Canary** — for senior roles
5. **Jenkins / ArgoCD** — as relevant
6. **Interview Questions** — final review

---

## The Standard Pipeline (memorize)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/myorg/myapp:${{ github.sha }}
      - run: kubectl set image deployment/myapp myapp=ghcr.io/myorg/myapp:${{ github.sha }}
```

---

## Cross-References

- [Docker](../40.1-docker/INDEX.md) — what CI/CD builds and deploys
- [Kubernetes](../40.2-kubernetes/INDEX.md) — common deploy target
- [Git Advanced](../40.6-git-advanced/INDEX.md) — branch strategy affects CI/CD

---

## Navigation

[← Previous: Kubernetes](../40.2-kubernetes/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Observability →](../40.4-observability/INDEX.md)
