# Docker — Index

> **Study time:** ≈ 2 h 1 m of reading (11 files, ~11 min average).
> **11 files** — Docker fundamentals from images and containers to volumes, networks, Compose, multi-stage builds, runtime internals (namespaces/cgroups), supply chain security (signing/SBOM), rootless & sandboxed runtimes, production patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Docker:** The unit of deployment for modern apps. Every senior backend interview expects you to write a Dockerfile, debug a container, and explain image optimization. Docker is also the foundation for Kubernetes, CI/CD, and serverless.

---

## Topic Categories

| Category | Files | Why it matters |
| -------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------- |
| [Core Concepts](#core-concepts) | 2 | Images, containers, volumes, networks — the foundation |
| [Multi-Container & Build](#multi-container--build) | 2 | Compose, multi-stage builds — production workflows |
| [Production & Security](#production--security) | 5 | Best practices, production patterns, runtime internals, supply chain, sandboxed runtimes |
| [Interview Prep](#interview-prep) | 1 | 30 questions |

---

## Core Concepts

What Docker is and how it runs.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Images & Containers](40.1.01-images-containers.md) | Dockerfile, layers, CMD vs ENTRYPOINT, container lifecycle, image registry | Important | Important | 13 min |
| 02 | [Volumes & Networks](40.1.02-volumes-networks.md) | Bind mounts, volumes, tmpfs, bridge/host/overlay networks, port mapping | Important | Important | 14 min |

---

## Multi-Container & Build

Production workflows.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 03 | [Compose](40.1.03-compose.md) | Docker Compose, multi-container apps, service configuration, profiles | Important | Important | 20 min |
| 04 | [Multi-Stage Builds](40.1.04-multi-stage-builds.md) | Build stages, dependency caching, image size optimization | Important | Important | 11 min |

---

## Production & Security

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Best Practices & Security](40.1.05-dockerfile-best-practices.md) | Layer caching, non-root users, distroless images, image scanning, labels | Important | Important | 10 min |
| 06 | [Production Patterns](40.1.06-production-patterns.md) | Multi-stage builds (advanced), Docker Compose in production, image optimization, container security checklist | Important | Important | 9 min |
| 07 | [Container Runtime Internals](40.1.07-container-runtime-internals-namespaces-cgroups.md) | Namespaces (pid/net/mnt/uts/ipc/user), cgroups v2 limits, OverlayFS copy-on-write layers, runc/containerd stack, container vs VM | Optional | Specialized | 14 min |
| 08 | [Image Signing, SBOM & Supply Chain](40.1.08-image-signing-sbom-supply-chain.md) | Cosign signing + admission verification, SBOM (syft, BuildKit attestations), SLSA provenance levels, registry policy, CI gates | Optional | Specialized | 11 min |
| 09 | [Rootless & Sandboxed Runtimes](40.1.09-rootless-sandboxed-runtimes.md) | Rootless mode (user namespaces, slirp4netns/pasta), gVisor vs Kata trade-offs, multi-tenant isolation, RuntimeClass | Optional | Specialized | 11 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 10 | [Interview Questions](40.1.10-interview-questions.md) | 30 curated questions with answers | Important | Important | 6 min |

---

## Suggested Study Order

1. **Images & Containers** — must know
2. **Volumes & Networks** — must know
3. **Compose** — for multi-container apps
4. **Multi-Stage Builds** — for production image size
5. **Best Practices & Security** — non-root, scanning, distroless
6. **Production Patterns** — senior level
7. **Container Runtime Internals** — namespaces/cgroups, the "what is a container" answer
8. **Image Signing & Supply Chain** — cosign, SBOM, SLSA
9. **Rootless & Sandboxed Runtimes** — gVisor/Kata, multi-tenancy
10. **Revision** — explain the source-linked mechanisms from memory using [the companion](REVISION.md)
11. **Interview Questions** — final practice

---

## Three Reading Passes

**Build and run:** Follow image contents, a container's process and writable layer, then connect volume lifetime and network paths. Reproduce a restart/removal case and explain why service DNS differs from localhost.

**Package and operate:** Build one application with separate compile/runtime dependencies. Explain cache inputs, secret injection, health versus restart behavior, and graceful shutdown before proposing a rollout.

**Choose trust boundaries:** Read namespaces/cgroups, signature/provenance verification and rootless/sandboxed runtimes. Distinguish observed runtime evidence from configuration sketches and unexecuted integrations. Then use the revision companion before interview practice.

---

## Cross-References

- [Kubernetes](../40.2-kubernetes/INDEX.md) — orchestrates Docker containers
- [CI/CD](../40.3-ci-cd/INDEX.md) — Docker build/deploy pipelines
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — services packaged as Docker images

---

## Navigation

[← Previous: Microservices](../../20-backend/20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Kubernetes →](../40.2-kubernetes/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — uses Docker for real.

| Topic | Docita evidence |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dockerfile in production | `apps/api/Dockerfile` — the image Fly builds and runs (`fly.toml [build]`) |
| Compose for local/e2e | `docker-compose.yml`: API service + `postgres:15-alpine`; E2E tests run against this Postgres (`docita_test`) |
| Image scanning | `.github/workflows/container-scan.yml` schedules Trivy filesystem scans (`scan-type: fs`) of apps/api and apps/worker; this is not a built-image scan |
| Rootless/runtimes/signing | No rootless/sandbox/cosign/SBOM setup established by these inspected Docker/Compose/scan files; verify the release configuration separately |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
