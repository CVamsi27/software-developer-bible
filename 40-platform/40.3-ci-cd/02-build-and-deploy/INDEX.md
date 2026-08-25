# Build & Deploy

> **2 files.** The runtime of every pipeline: building and shipping Docker images, and the pipeline shapes (stages, gates, strategies) that take a commit to production safely.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Build%20%26%20Deploy-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

CI platforms differ in syntax but not in substance: check out, build image, push to registry, deploy to target. This category teaches that substance once — registries, tags, deploy targets, and the pipeline patterns (trunk-based promotion, environment gates, rollback hooks) you will be asked to whiteboard.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Docker Build & Deploy](40.3.2.01-docker-build-deploy.md) | Build pipelines, layer caching in CI, registries (ECR/GCR/DockerHub), tagging strategy, deployment targets | 30 min |
| 02 | [Pipeline Patterns](40.3.2.02-pipeline-patterns.md) | End-to-end CI/CD pipelines, stage design, deployment strategies (rolling, blue-green, canary, feature flags) | 30 min |

---

## Cross-References

- [Releases & Metrics](../03-releases-and-metrics/INDEX.md) — the deploy strategies in depth
- [Docker Stack](../../../40-platform/40.1-docker/INDEX.md) — image fundamentals
- [Infra: Zero-Downtime Deployments](../../../30-architecture/30.3-infra-patterns/05-shipping-and-evolution/INDEX.md) — architecture-level view of the same patterns

---

## Navigation

[← CI Platforms](../01-ci-platforms/INDEX.md) · [↑ CI/CD Home](../INDEX.md) · [Next: Releases & Metrics →](../03-releases-and-metrics/INDEX.md)
