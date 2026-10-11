{% raw %}
# CI/CD — Index

> **Study time:** ≈ 1 h 51 m of reading (14 files, ~8 min average).
> **14 files** — a release path from GitHub Actions, GitLab CI/CD, Jenkins or Argo CD through build, artifact verification, production exposure and delivery measurement, followed by interview practice.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why CI/CD:** Senior engineers need to trace how a change becomes a production release: which code runs, which checks block it, which artifact is promoted, who can authorize deployment and how recovery is verified. The platform syntax varies; those boundaries carry across GitHub Actions, GitLab CI/CD, Jenkins and Argo CD.

---

## Category Map

| Category | Folder | Files | What it covers |
| ------------------ | ------------------------------------------------------------ | ----: | -------------------------------------------------------------------------------------------------------- |
| CI Platforms | [01-ci-platforms/](01-ci-platforms/INDEX.md) | 4 | GitHub Actions, GitLab CI/CD, Jenkins, and Argo CD — compare their event, execution and authority models |
| Build & Deploy | [02-build-and-deploy/](02-build-and-deploy/INDEX.md) | 4 | Docker build/deploy, pipeline patterns, artifact registries + promotion, supply-chain security (SLSA) |
| Releases & Metrics | [03-releases-and-metrics/](03-releases-and-metrics/INDEX.md) | 2 | Blue-green, canary — plus DORA metrics for delivery performance |
| Interview Prep | [04-interview-prep/](04-interview-prep/INDEX.md) | 1 | Authored interview drill |

---

## CI Platforms

Start with the event, job graph and credential model of one platform. Compare the same release contract in the others, including the controller model when Argo CD owns cluster reconciliation.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [GitHub Actions](01-ci-platforms/40.3.1.01-github-actions.md) | Workflows, actions, runners, matrix builds, caching, secrets | Most common — GitHub repos | Important | Important | 12 min |
| 02 | [GitLab CI/CD](01-ci-platforms/40.3.1.02-gitlab-ci.md) | `.gitlab-ci.yml`, multi-project pipelines, Auto DevOps | GitLab repos | Important | Important | 9 min |
| 03 | [Jenkins CI/CD](01-ci-platforms/40.3.1.03-jenkins.md) | Declarative/scripted pipelines, shared libraries, plugins | Legacy enterprise | Important | Important | 7 min |
| 04 | [Argo CD (GitOps)](01-ci-platforms/40.3.1.04-argocd.md) | GitOps, ApplicationSets, sync policies and recovery boundaries | Kubernetes + GitOps | Important | Important | 11 min |

---

## Build & Deploy

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Docker Build & Deploy](02-build-and-deploy/40.3.2.01-docker-build-deploy.md) | Docker build pipelines, registry (ECR/GCR/DockerHub), deployment strategies | Important | Important | 7 min |
| 06 | [Pipeline Patterns](02-build-and-deploy/40.3.2.02-pipeline-patterns.md) | GitHub Actions CI/CD, GitLab CI, deployment pipelines, deployment strategies (rolling, blue-green, canary, feature flags) | Important | Important | 6 min |
| 07 | [Artifact Registries & Release Promotion](02-build-and-deploy/40.3.2.03-artifact-registries-release-promotion.md) | GHCR/ECR/Artifactory/NPM, immutable digests, build-once promotion dev->staging->prod, changelog automation, retention, pull-through caches | Important | Important | 11 min |
| 08 | [Pipeline Supply-Chain Security & SLSA](02-build-and-deploy/40.3.2.04-pipeline-supply-chain-security-slsa.md) | Pipeline attack surface, SolarWinds/Codecov/xz, SLSA levels, SHA pinning + Dependabot, OIDC federation, provenance attestations | Important | Important | 14 min |

---

## Releases & Metrics

Controlled exposure, measured outcomes and compatible recovery.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 09 | [Blue-Green & Canary](03-releases-and-metrics/40.3.3.01-blue-green-canary.md) | Zero-downtime deployments, traffic shifting, rollback, feature flags | Important | Important | 7 min |
| 10 | [DORA Metrics & Delivery Performance](03-releases-and-metrics/40.3.3.02-dora-metrics-delivery-performance.md) | Five delivery measures including deployment rework rate, honest instrumentation, benchmarks, gaming pitfalls, error budgets | Important | Important | 16 min |

**Decision:** Choose exposure based on routing capability, traffic/sample size, capacity and state compatibility. Rolling replacement, retained blue-green capacity and analyzed canaries solve different constraints; none alone promises zero downtime or instant recovery.

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 11 | [Interview Questions](04-interview-prep/40.3.4.01-interview-questions.md) | Authored question bank | Important | Important | 5 min |

---

## Suggested Study Order

1. **GitHub Actions** (or GitLab CI if your JD requires) — must know
2. **Docker Build & Deploy** — must know
3. **Pipeline Patterns** — senior level
4. **Artifact Registries & Release Promotion** — senior level
5. **Pipeline Supply-Chain Security & SLSA** — staff differentiator
6. **Blue-Green & Canary** — for senior roles
7. **DORA Metrics & Delivery Performance** — staff/lead conversations
8. **Jenkins / Argo CD** — as relevant
9. **Category REVISION companions** — explain mechanisms from memory
10. **Interview Questions** — separate final practice

---

## Trace the Actual Release Contract

Use the complete [GitHub Actions](01-ci-platforms/40.3.1.01-github-actions.md) workflow and [image pipeline](02-build-and-deploy/40.3.2.01-docker-build-deploy.md). Explain the event/ref, real checks, output producer, artifact identity, scoped credentials, deployment target and recovery evidence. Do not memorize an incomplete deploy fragment as if it supplies registry login, cluster trust and an approved build automatically.

---

## Cross-References

- [Docker](../40.1-docker/INDEX.md) — what CI/CD builds and deploys
- [Kubernetes](../40.2-kubernetes/INDEX.md) — common deploy target
- [Git Advanced](../40.6-git-advanced/INDEX.md) — branch strategy affects CI/CD

---

## Navigation

[← Previous: Kubernetes](../40.2-kubernetes/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Observability →](../40.4-observability/INDEX.md)
{% endraw %}
