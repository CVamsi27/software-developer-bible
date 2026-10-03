# Build & Deploy

> **Study time:** ≈ 1 h 5 m of reading (5 files, ~13 min average).
> **5 files.** The runtime of every pipeline: building and shipping Docker images, the pipeline shapes (stages, gates, strategies) that take a commit to production safely, artifact registries with digest-based promotion, and supply-chain security for the pipeline itself.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Build%20%26%20Deploy-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

CI platforms differ in syntax but not in substance: check out, build image, push to registry, deploy to target. This category teaches that substance once — registries, tags, deploy targets, and the pipeline patterns (trunk-based promotion, environment gates, rollback hooks) you will be asked to whiteboard.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Docker Build & Deploy](40.3.2.01-docker-build-deploy.md) | Build pipelines, layer caching in CI, registries (ECR/GCR/DockerHub), tagging strategy, deployment targets | Important | Important | 16 min |
| 02 | [Pipeline Patterns](40.3.2.02-pipeline-patterns.md) | End-to-end CI/CD pipelines, stage design, deployment strategies (rolling, blue-green, canary, feature flags) | Important | Important | 14 min |
| 03 | [Artifact Registries & Release Promotion](40.3.2.03-artifact-registries-release-promotion.md) | GHCR/ECR/Artifactory/NPM, immutable tags + digests, build-once promotion dev->staging->prod, changelog automation (release-please/changesets), retention, pull-through caches | Important | Important | 17 min |
| 04 | [Pipeline Supply-Chain Security & SLSA](40.3.2.04-pipeline-supply-chain-security-slsa.md) | Pipeline as attack surface, SolarWinds/Codecov/xz lessons, SLSA levels, SHA pinning + Dependabot, OIDC federation, provenance attestations, workflow branch protection | Important | Important | 15 min |

---

## Cross-References

- [Releases & Metrics](../03-releases-and-metrics/INDEX.md) — the deploy strategies in depth
- [Docker Stack](../../../40-platform/40.1-docker/INDEX.md) — image fundamentals
- [Infra: Zero-Downtime Deployments](../../../30-architecture/30.3-infra-patterns/05-shipping-and-evolution/INDEX.md) — architecture-level view of the same patterns

---

## Navigation

[← CI Platforms](../01-ci-platforms/INDEX.md) · [↑ CI/CD Home](../INDEX.md) · [Next: Releases & Metrics →](../03-releases-and-metrics/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — builds and deploys for real.

| Topic | Docita evidence |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Docker build in CI | API image built from `apps/api/Dockerfile`; Fly `[build]` consumes it; scanned by `container-scan.yml` |
| Deploy pipeline | `deploy.yml` + `scripts/deploy/fly-deploy-in-primary-region.sh` (pins deploys to primary region `sin`) |
| DB migration gate | `db-migrations.yml` + `verify-db-schema-sync.sh` before rollout |
| Canary deploy | `scripts/deploy/worker-canary-deploy.sh` for the worker app |
| Supply-chain checks | `osv-scanner.toml`, `pnpm audit --audit-level=high` gate, workflow script-ref checks |
| Artifact registries / SLSA attestations | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
