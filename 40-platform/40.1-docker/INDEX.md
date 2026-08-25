# Docker — Index

> **7 files** — Docker fundamentals from images and containers to volumes, networks, Compose, multi-stage builds, best practices, production patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Docker:** The unit of deployment for modern apps. Every senior backend interview expects you to write a Dockerfile, debug a container, and explain image optimization. Docker is also the foundation for Kubernetes, CI/CD, and serverless.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Core Concepts](#core-concepts) | 2 | Images, containers, Dockerfile — the foundation |
| [Storage & Networking](#storage--networking) | 1 | Volumes, networks — the runtime side |
| [Multi-Container & Build](#multi-container--build) | 2 | Compose, multi-stage builds — production patterns |
| [Production & Security](#production--security) | 2 | Best practices, production patterns, image hardening |

---

## Core Concepts

What Docker is and how it works.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Images & Containers](40.1.01-images-containers.md) | Dockerfile, layers, CMD vs ENTRYPOINT, container lifecycle, image registry | 25 min |
| 02 | [Volumes & Networks](40.1.02-volumes-networks.md) | Bind mounts, volumes, tmpfs, bridge/host/overlay networks, port mapping | 25 min |

---

## Storage & Networking

Persistent data and inter-container communication.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [Volumes & Networks](40.1.02-volumes-networks.md) | (See above) | 25 min |

---

## Multi-Container & Build

Production patterns.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Compose](40.1.03-compose.md) | Docker Compose, multi-container apps, service configuration, profiles | 25 min |
| 04 | [Multi-Stage Builds](40.1.04-multi-stage-builds.md) | Build stages, dependency caching, image size optimization | 20 min |

---

## Production & Security

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 05 | [Best Practices & Security](40.1.05-dockerfile-best-practices.md) | Layer caching, non-root users, distroless images, image scanning, labels | 25 min |
| 07 | [Production Patterns](40.1.06-production-patterns.md) | Multi-stage builds (advanced), Docker Compose in production, image optimization, container security checklist | 30 min |
| 06 | [Interview Questions](40.1.10-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## Suggested Study Order

1. **Images & Containers** — must know
2. **Volumes & Networks** — must know
3. **Compose** — for multi-container apps
4. **Multi-Stage Builds** — for production image size
5. **Best Practices & Security** — non-root, scanning, distroless
6. **Production Patterns** — senior level
7. **Interview Questions** — final review

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
