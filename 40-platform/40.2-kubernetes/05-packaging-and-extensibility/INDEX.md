# Packaging & Extensibility

> **Study time:** ≈ 37 min of reading (4 files, ~9 min average).
> **4 files.** Distributing and extending Kubernetes itself: Helm charts and Kustomize overlays as the packaging layer, plus the extension surface (CRDs, controllers, operators) that turns Kubernetes into a platform for building platforms.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Packaging-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Packaging composes the objects to submit; controllers reconcile those objects into running behavior. Helm and Kustomize solve different composition needs. CRDs add API types, while an operator adds the repeated reconciliation needed to implement their lifecycle.

## Reading Passes

1. **Render a release:** inspect values, templates and release records in [Helm](40.2.5.01-helm.md), including what rollback cannot undo.
2. **Apply an environment difference:** trace base, patch, generator and final manifests in [Kustomize](40.2.5.02-kustomize-overlays-packaging-tradeoffs.md). Verify selectors and generated references rather than trusting a small patch.
3. **Add behavior only when needed:** follow desired versus observed state in [CRDs and operators](40.2.5.03-crds-operators-controller-patterns.md). Finish [revision](REVISION.md) after the learning chapters.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Helm](40.2.5.01-helm.md) | Charts, templates, values overrides, release revisions and rollback boundaries, dependencies, HTTP and OCI distribution | Optional | Specialized | 17 min |
| 02 | [Kustomize Overlays & Packaging Trade-offs](40.2.5.02-kustomize-overlays-packaging-tradeoffs.md) | Bases and overlays, strategic-merge and JSON Patch, generated ConfigMap rollouts, transformers, Helm integration and secret boundaries | Optional | Specialized | 8 min |
| 03 | [CRDs, Operators & Controller Patterns](40.2.5.03-crds-operators-controller-patterns.md) | CRD schema and versioning, reconciliation, controller ownership, garbage collection, finalizers and operator decision boundaries | Optional | Specialized | 10 min |

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — what gets packaged
- [CI/CD: GitOps](../../../40-platform/40.3-ci-cd/01-ci-platforms/INDEX.md) — Argo CD can render Helm charts and reconcile the resulting manifests; it does not operate Helm release records in the same way as a Helm CLI install

---

## Navigation

[← Production Hardening](../04-production-hardening/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Interview Prep →](../06-interview-prep/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet._ No Helm charts, Kustomize overlays, CRDs, or operators exist in the repo — the only packaging artifact is `apps/api/Dockerfile`, deployed by plain CI. [future]: if docita ever outgrows a single Fly app, I'd start with Kustomize-style env overlays before reaching for Helm.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
