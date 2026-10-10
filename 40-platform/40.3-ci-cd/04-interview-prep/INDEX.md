# Interview Prep — CI/CD

> **Study time:** ≈ 5 min of reading (1 files, ~5 min average).
> **1 file, An authored question bank with answers.** From "write a basic workflow" to "design a zero-downtime release process".

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

An authored question bank with answers. Do them after reading the content categories; the model answers reference those chapters.

---

## Navigation

[← Releases & Metrics](../03-releases-and-metrics/INDEX.md) · [↑ CI/CD Home](../INDEX.md)

---

## Docita Anchor

Current source inspection on 2026-10-10 found deploy triggers commented out. Use historical measured release evidence with its date; configuration files do not establish current production health or successful delivery.

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — gives me true stories for these answers.

| Topic | Docita evidence |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| "Design a pipeline" | GitHub Actions configuration around a turbo monorepo (`ci.yml`, `api-e2e.yml`, `db-migrations.yml`…) |
| "Zero-downtime deploy?" | Configured Fly checks, worker started-state canary settling and migration ordering; not proof of current zero downtime |
| "How do you keep CI fast?" | Pre-push husky subset of gates; full `verify:standard` reserved for merge; turbo task caching |
| "Release metrics?" | Latency-budget scripts and dated release evidence; synthetic workflow records a historical manually-disabled note |
| GitOps / ArgoCD stories | _No direct docita implementation yet._ |
