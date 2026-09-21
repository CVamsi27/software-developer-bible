{% raw %}
# CI/CD — Index

> **Study time:** ≈ 2 h 47 m of reading (11 files, ~15 min average).
> **11 files** — CI/CD pipeline fundamentals from GitHub Actions and Jenkins to GitLab CI, ArgoCD, Docker build/deploy, artifact registries with release promotion, supply-chain security (SLSA), blue-green/canary deployments, DORA metrics, pipeline patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why CI/CD:** Every senior engineer owns their pipeline. You must know how to set up GitHub Actions (or GitLab CI), build a Docker image, push to a registry, and deploy to a target. Blue-green and canary deployments are the senior-level patterns. GitOps (ArgoCD) is increasingly common.

---

## Category Map

| Category | Folder | Files | What it covers |
| ------------------ | ------------------------------------------------------------ | ----: | ----------------------------------------------------------------------------------------------------- |
| CI Platforms | [01-ci-platforms/](01-ci-platforms/INDEX.md) | 4 | GitHub Actions, GitLab CI, Jenkins, ArgoCD — pick the one your company uses |
| Build & Deploy | [02-build-and-deploy/](02-build-and-deploy/INDEX.md) | 4 | Docker build/deploy, pipeline patterns, artifact registries + promotion, supply-chain security (SLSA) |
| Releases & Metrics | [03-releases-and-metrics/](03-releases-and-metrics/INDEX.md) | 2 | Blue-green, canary — plus DORA metrics for delivery performance |
| Interview Prep | [04-interview-prep/](04-interview-prep/INDEX.md) | 1 | 50+ Qs |

---

## CI Platforms

Pick the one your company uses — the patterns are similar.

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 01 | [GitHub Actions](01-ci-platforms/40.3.1.01-github-actions.md) | Workflows, actions, runners, matrix builds, caching, secrets | Most common — GitHub repos | 21 min |
| 02 | [GitLab CI/CD](01-ci-platforms/40.3.1.02-gitlab-ci.md) | `.gitlab-ci.yml`, multi-project pipelines, Auto DevOps | GitLab repos | 10 min |
| 03 | [Jenkins CI/CD](01-ci-platforms/40.3.1.03-jenkins.md) | Declarative/scripted pipelines, shared libraries, plugins | Legacy enterprise | 11 min |
| 04 | [ArgoCD (GitOps)](01-ci-platforms/40.3.1.04-argocd.md) | GitOps, ApplicationSets, sync policies, rollback | K8s + GitOps | 8 min |

---

## Build & Deploy

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 05 | [Docker Build & Deploy](02-build-and-deploy/40.3.2.01-docker-build-deploy.md) | Docker build pipelines, registry (ECR/GCR/DockerHub), deployment strategies | 17 min |
| 06 | [Pipeline Patterns](02-build-and-deploy/40.3.2.02-pipeline-patterns.md) | GitHub Actions CI/CD, GitLab CI, deployment pipelines, deployment strategies (rolling, blue-green, canary, feature flags) | 15 min |
| 07 | [Artifact Registries & Release Promotion](02-build-and-deploy/40.3.2.03-artifact-registries-release-promotion.md) | GHCR/ECR/Artifactory/NPM, immutable digests, build-once promotion dev->staging->prod, changelog automation, retention, pull-through caches | 19 min |
| 08 | [Pipeline Supply-Chain Security & SLSA](02-build-and-deploy/40.3.2.04-pipeline-supply-chain-security-slsa.md) | Pipeline attack surface, SolarWinds/Codecov/xz, SLSA levels, SHA pinning + Dependabot, OIDC federation, provenance attestations | 17 min |

---

## Releases & Metrics

Senior-level patterns for zero-downtime deploys.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 09 | [Blue-Green & Canary](03-releases-and-metrics/40.3.3.01-blue-green-canary.md) | Zero-downtime deployments, traffic shifting, rollback, feature flags | 20 min |
| 10 | [DORA Metrics & Delivery Performance](03-releases-and-metrics/40.3.3.02-dora-metrics-delivery-performance.md) | Four keys (DF, lead time, MTTR, CFR), honest instrumentation, benchmarks, gaming pitfalls, error budgets | 17 min |

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
| --: | ------ | -------- | ----------: |
| 11 | [Interview Questions](04-interview-prep/40.3.4.01-interview-questions.md) | 50+ curated questions with answers | 12 min |

---

## Suggested Study Order

1. **GitHub Actions** (or GitLab CI if your JD requires) — must know
2. **Docker Build & Deploy** — must know
3. **Pipeline Patterns** — senior level
4. **Artifact Registries & Release Promotion** — senior level
5. **Pipeline Supply-Chain Security & SLSA** — staff differentiator
6. **Blue-Green & Canary** — for senior roles
7. **DORA Metrics & Delivery Performance** — staff/lead conversations
8. **Jenkins / ArgoCD** — as relevant
9. **Interview Questions** — final review

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
{% endraw %}
