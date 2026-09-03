# Packaging & Extensibility

> **3 files.** Distributing and extending Kubernetes itself: Helm charts and Kustomize overlays as the packaging layer, plus the extension surface (CRDs, controllers, operators) that turns Kubernetes into a platform for building platforms.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Packaging-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Nobody hand-writes 40 YAML files per release anymore — they install a Helm chart or apply a Kustomize overlay. And when your workload has custom logic ("make sure the Kafka topic exists before the app starts"), raw Deployments can't express it; CRDs and operators can. This category covers the packaging layer every team shares (Helm, Kustomize, and how to combine them) and the extensibility layer platform teams build on.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Helm](40.2.5.01-helm.md) | Charts, templates, values overrides, releases, rollback, dependency management, helmfile | 30 min |
| 02 | [Kustomize Overlays & Packaging Trade-offs](40.2.5.02-kustomize-overlays-packaging-tradeoffs.md) | Base/overlays, strategic merge + JSON6902 patches, configMapGenerator hash rollouts, transformers, Helm vs Kustomize decision table, hybrid pipelines, secrets caveat | 25 min |
| 03 | [CRDs, Operators & Controller Patterns](40.2.5.03-crds-operators-controller-patterns.md) | CRD anatomy, reconcile loops (desired vs observed), operator capability levels, ownerReferences/GC, controller skeletons, when to write an operator, OLM | 35 min |

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — what gets packaged
- [CI/CD: GitOps](../../../40-platform/40.3-ci-cd/01-ci-platforms/INDEX.md) — ArgoCD deploys Helm releases

---

## Navigation

[← Production Hardening](../04-production-hardening/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Interview Prep →](../06-interview-prep/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet._ No Helm charts, Kustomize overlays, CRDs, or operators exist in the repo — the only packaging artifact is `apps/api/Dockerfile`, deployed by plain CI. [future]: if docita ever outgrows a single Fly app, I'd start with Kustomize-style env overlays before reaching for Helm.
