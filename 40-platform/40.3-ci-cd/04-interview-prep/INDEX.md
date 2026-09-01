# Interview Prep — CI/CD

> **1 file, 50+ curated questions with answers.** From "write a basic workflow" to "design a zero-downtime release process".

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview%20Prep-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What's here

Questions spanning all three content categories: platform mechanics (Actions/GitLab/Jenkins/ArgoCD), build-and-deploy substance, and release strategies.

- **Easy** — trigger a workflow on PR, cache dependencies, store a secret
- **Medium** — matrix builds, registry auth, promote an artifact across environments
- **Hard** — design a canary rollout with automated rollback, GitOps drift reconciliation, pipeline security

---

## File Index

### [CI/CD Interview Questions](40.3.4.01-interview-questions.md)

50+ curated questions with answers. Do them after reading the content categories; the model answers reference those chapters.

---

## Navigation

[← Releases & Metrics](../03-releases-and-metrics/INDEX.md) · [↑ CI/CD Home](../INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — gives me true stories for these answers.

| Topic                      | Docita evidence                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| "Design a pipeline"        | 11-workflow GitHub Actions suite around a turbo monorepo (`ci.yml`, `api-e2e.yml`, `db-migrations.yml`…) |
| "Zero-downtime deploy?"    | Health-gated Fly deploys + canaried worker rollout + migration-before-deploy ordering                    |
| "How do you keep CI fast?" | Pre-push husky subset of gates; full `verify:standard` reserved for merge; turbo task caching            |
| "Release metrics?"         | Latency-SLO budgets enforced in CI, synthetic monitoring, filled release-evidence docs                   |
| GitOps / ArgoCD stories    | _No direct docita implementation yet._                                                                   |
