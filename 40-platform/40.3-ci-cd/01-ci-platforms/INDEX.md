# CI Platforms

> **Study time:** ≈ 46 min of reading (5 files, ~9 min average).
> **5 files.** The four platforms you are most likely to meet: GitHub Actions, GitLab CI, Jenkins, and ArgoCD (GitOps). The concepts transfer; learn one deeply, map the others.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-CI%20Platforms-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Follow One Commit Into Production

Start with the platform your project uses, but keep the same questions throughout: what code executes, which checks observe it, which bytes are promoted, and where deployment authority becomes available? A pipeline definition schedules work; the application scripts and cloud/controller configuration supply the actual behavior.

## Pass 1 — Separate Verification From Promotion

[GitHub Actions](40.3.1.01-github-actions.md) traces a PR through verification and a trusted main build through identified-artifact promotion. Understand events, jobs/runners, artifacts and permissions before choosing reusable actions, matrices or caches.

## Pass 2 — Translate the Dependency and Credential Graph

[GitLab CI/CD](40.3.1.02-gitlab-ci.md) expresses ordering through stages and needs. [Jenkins](40.3.1.03-jenkins.md) adds operated controllers, agents and plugins. Read both as translations of the same data/authority boundaries, then check their distinct syntax and lifecycle requirements.

## Pass 3 — Let a Controller Reconcile the Declared State

[ArgoCD](40.3.1.04-argocd.md) continuously compares desired Git state with the cluster. Trace drift and synchronization separately from the build that produced the image, and separate manifest rollback from irreversible database/external effects.

## Finish With Revision, Then Practice

Close the chapters and complete [section revision questions](REVISION.md). Then use the separate [CI/CD interview bank](../04-interview-prep/40.3.4.01-interview-questions.md) to explain a concrete release decision.

---

## Cross-References

- [Build & Deploy](../02-build-and-deploy/INDEX.md) — what these platforms execute
- [Git Advanced](../../../40-platform/40.6-git-advanced/INDEX.md) — branch strategy drives pipeline design

---

## Navigation

[↑ CI/CD Home](../INDEX.md) · [Next: Build & Deploy →](../02-build-and-deploy/INDEX.md)

---

## Apply the Flow to Your Repository

Inspect current workflow files, build/deploy scripts and environment settings together. Trace a shared-package change and a failed deployment through their actual run evidence. A historical workflow count, file name or badge cannot establish required checks, cloud trust or readiness.
