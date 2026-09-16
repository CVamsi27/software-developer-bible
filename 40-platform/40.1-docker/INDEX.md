# Docker — Index

> **Study time:** ≈ 2 h 22 m of reading (10 files, ~14 min average).
> **10 files** — Docker fundamentals from images and containers to volumes, networks, Compose, multi-stage builds, runtime internals (namespaces/cgroups), supply chain security (signing/SBOM), rootless & sandboxed runtimes, production patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
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
| [Interview Prep](#interview-prep) | 1 | 50+ Qs |

---

## Core Concepts

What Docker is and how it runs.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Images & Containers](40.1.01-images-containers.md) | Dockerfile, layers, CMD vs ENTRYPOINT, container lifecycle, image registry | 13 min |
| 02 | [Volumes & Networks](40.1.02-volumes-networks.md) | Bind mounts, volumes, tmpfs, bridge/host/overlay networks, port mapping | 15 min |

---

## Multi-Container & Build

Production workflows.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 03 | [Compose](40.1.03-compose.md) | Docker Compose, multi-container apps, service configuration, profiles | 21 min |
| 04 | [Multi-Stage Builds](40.1.04-multi-stage-builds.md) | Build stages, dependency caching, image size optimization | 13 min |

---

## Production & Security

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 05 | [Best Practices & Security](40.1.05-dockerfile-best-practices.md) | Layer caching, non-root users, distroless images, image scanning, labels | 6 min |
| 06 | [Production Patterns](40.1.06-production-patterns.md) | Multi-stage builds (advanced), Docker Compose in production, image optimization, container security checklist | 10 min |
| 07 | [Container Runtime Internals](40.1.07-container-runtime-internals-namespaces-cgroups.md) | Namespaces (pid/net/mnt/uts/ipc/user), cgroups v2 limits, OverlayFS copy-on-write layers, runc/containerd stack, container vs VM | 16 min |
| 08 | [Image Signing, SBOM & Supply Chain](40.1.08-image-signing-sbom-supply-chain.md) | Cosign signing + admission verification, SBOM (syft, BuildKit attestations), SLSA provenance levels, registry policy, CI gates | 13 min |
| 09 | [Rootless & Sandboxed Runtimes](40.1.09-rootless-sandboxed-runtimes.md) | Rootless mode (user namespaces, slirp4netns/pasta), gVisor vs Kata trade-offs, multi-tenant isolation, RuntimeClass | 13 min |

---

## Interview Prep

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 10 | [Interview Questions](40.1.10-interview-questions.md) | 50+ curated questions with answers | 22 min |

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
10. **Interview Questions** — final review

---

## Key Patterns (memorize)

### The Multi-Stage Dockerfile (the standard)

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

This produces a small, secure production image. The build dependencies (TypeScript, dev deps) don't ship to production.

### The Compose Stack

```yaml
# docker-compose.yml
version: '3.9'
services:
  app:
    build: .
    ports: ['3000:3000']
    depends_on: [db, redis]
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
      REDIS_URL: redis://redis:6379
  db:
    image: postgres:16-alpine
    volumes: ['pgdata:/var/lib/postgresql/data']
  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

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
| ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Dockerfile in production | `apps/api/Dockerfile` — the image Fly builds and runs (`fly.toml [build]`) |
| Compose for local/e2e | `docker-compose.yml`: API service + `postgres:15-alpine`; E2E tests run against this Postgres (`docita_test`) |
| Image scanning | `.github/workflows/container-scan.yml` scans the built API image |
| Rootless/runtimes/signing | Not configured — standard Docker runtime, no cosign/SBOM gates |
