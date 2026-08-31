# CI Platforms

> **4 files.** The four platforms you are most likely to meet: GitHub Actions, GitLab CI, Jenkins, and ArgoCD (GitOps). The concepts transfer; learn one deeply, map the others.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-CI%20Platforms-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Every senior engineer owns a pipeline, and the pipeline lives on a platform. Job postings name the tool ("GitHub Actions required", "GitOps with ArgoCD"), but interviews test the concepts: triggers, caching, secrets, matrix builds. Read your company's platform first, then skim the rest so you can translate.

---

## File Index

| Order | File                                          | Topics                                                                                   | Read time |
| --   :  | ------                                          | --------                                                                                   | ----------: |
| 01    | [GitHub Actions](40.3.1.01-github-actions.md) | Workflows, actions, runners, matrix builds, caching, secrets, environments               | 30 min    |
| 02    | [GitLab CI/CD](40.3.1.02-gitlab-ci.md)        | `.gitlab-ci.yml`, stages, multi-project pipelines, Auto DevOps                           | 25 min    |
| 03    | [Jenkins CI/CD](40.3.1.03-jenkins.md)         | Declarative vs scripted pipelines, shared libraries, plugins, controller/agent model     | 25 min    |
| 04    | [ArgoCD (GitOps)](40.3.1.04-argocd.md)        | GitOps model, Applications and ApplicationSets, sync policies, drift detection, rollback | 25 min    |

---

## Cross-References

- [Build & Deploy](../02-build-and-deploy/INDEX.md) — what these platforms execute
- [Git Advanced](../../../40-platform/40.6-git-advanced/INDEX.md) — branch strategy drives pipeline design

---

## Navigation

[↑ CI/CD Home](../INDEX.md) · [Next: Build & Deploy →](../02-build-and-deploy/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — runs CI for real (GitHub Actions).

| Topic                     | Docita evidence                                                                                                                                                                          |
| -------                     | -----------------                                                                                                                                                                          |
| GitHub Actions suite      | `.github/workflows/ci.yml` + 10 more: `api-e2e`, `db-migrations`, `deploy`, `container-scan`, `frontend-critical-e2e`, `frontend-e2e-weekly`, `synthetic-monitoring`, `scale-api-hours`… |
| CI hygiene                | `workflow-staleness.yml` + `check-workflow-staleness.mjs` keep workflows from rotting                                                                                                    |
| Local pre-CI layer        | Husky pre-push runs the cheap subset of standard gates so bad commits die before wasting a CI run                                                                                        |
| GitLab / Jenkins / ArgoCD | _No direct docita implementation yet._                                                                                                                                                   |
