# Packaging & Extensibility

> **1 file.** Distributing and extending Kubernetes itself: Helm charts as the de facto packaging standard, plus the extension surface (CRDs, operators) that turns Kubernetes into a platform for building platforms.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Packaging-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-in--progress-yellow)](#)

---

## Why this category exists

Nobody hand-writes 40 YAML files per release anymore — they install a Helm chart. And when your workload has custom logic ("make sure the Kafka topic exists before the app starts"), raw Deployments can't express it; CRDs and operators can. This category covers the packaging layer every team shares and the extensibility layer platform teams build on.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Helm](40.2.5.01-helm.md) | Charts, templates, values overrides, releases, rollback, dependency management, helmfile | 30 min |

*Slots reserved: `40.2.5.02` Kustomize & packaging trade-offs, `40.2.5.03` CRDs/operators/controller patterns (upcoming chapters — no links yet).*

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — what gets packaged
- [CI/CD: GitOps](../../../40-platform/40.3-ci-cd/01-ci-platforms/INDEX.md) — ArgoCD deploys Helm releases

---

## Navigation

[← Production Hardening](../04-production-hardening/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Interview Prep →](../06-interview-prep/INDEX.md)
