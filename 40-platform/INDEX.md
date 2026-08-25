# Platform Stack

> **Docker, Kubernetes, CI/CD, Observability, Build Tools, Git, Serverless, Monorepo, 12-Factor, Reverse Proxy** — shared by both the [indian-sde-faang lane](../81-lanes-indian-sde-faang/INDEX.md) and the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> 88 files across 11 sub-stacks — the "how it runs" layer of the bible.

[![Files](https://img.shields.io/badge/files-88-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-11-green)](#the-11-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this stack matters

Senior interviews test platform knowledge. Even for "full-stack" roles, you must:
- Containerize an app with Docker (write a `Dockerfile`, use multi-stage builds)
- Explain Kubernetes architecture (pods, deployments, services, ingress)
- Set up CI/CD (GitHub Actions, blue-green, canary)
- Know observability (logging, metrics, tracing, OpenTelemetry)
- Understand build tools (Webpack vs Vite vs Turbopack)
- Use Git fluently (rebase, cherry-pick, bisect, submodules)

This stack is the canonical reference. Each sub-stack has its own INDEX with detailed categorization and interview Q&A.

---

## The 11 Sub-Stacks (in study order)

| Order | Sub-stack | Files | Topics |
|------:|-----------|------:|--------|
| 1 | [Docker](40.1-docker/INDEX.md) | 10 | Images, containers, volumes, networks, compose, multi-stage builds, production patterns |
| 2 | [Kubernetes](40.2-kubernetes/INDEX.md) | 17 | Pods, deployments, services, ingress, ConfigMaps, HPA, Helm, RBAC |
| 3 | [CI/CD](40.3-ci-cd/INDEX.md) | 11 | GitHub Actions, Docker build/deploy, blue-green/canary, Jenkins, GitLab CI, ArgoCD |
| 4 | [Observability](40.4-observability/INDEX.md) | 11 | Logging, monitoring, tracing, OpenTelemetry, error tracking, SLI/SLO/SLA, alerting |
| 5 | [Build Tools](40.5-build-tools/INDEX.md) | 10 | Webpack, Vite, Turbopack, Rspack, ESBuild, SWC, Babel |
| 6 | [Git Advanced](40.6-git-advanced/INDEX.md) | 10 | Internals (objects/refs/packfiles), branching, rebase, hooks, archaeology, LFS/partial clones, signed commits |
| 7 | [Serverless & Edge](40.7-serverless-edge/INDEX.md) | 8 | Lambda, Vercel Edge, serverless patterns, SAM/CDK/SST, durable execution (Temporal/Inngest) |
| 8 | [Monorepo](40.8-monorepo/INDEX.md) | 6 | Turborepo, Nx, pnpm, Rush, Bazel, versioning & publishing strategies |
| 9 | [Twelve-Factor App](40.9-twelve-factor/INDEX.md) | 1 | The canonical cloud-native methodology — codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes |
| 10 | [CDN & Edge](40.10-cdn/INDEX.md) | 3 | CDN caching strategies, invalidation, edge functions, multi-CDN steering, media optimization at the edge, PHI-at-edge considerations |
| 11 | [Reverse Proxy](40.11-reverse-proxy/INDEX.md) | 1 | Nginx internals: C10K, master–worker + epoll event loop, config contexts, sendfile vs proxy_pass, upstream LB algorithms, health checks, TLS termination, buffering, rate limiting, proxy_cache, zero-downtime reload, nginx vs HAProxy vs Envoy vs ALB |

---

## Category Map (high-level)

The platform stack is organized into 4 conceptual layers. Read in this order.

### Containers & Orchestration (read first)
- **Docker** — the unit of deployment
- **Kubernetes** — the orchestrator (if JD requires)

### Delivery & Operations (read second)
- **CI/CD** — build, test, deploy pipelines
- **Observability** — logs, metrics, traces, errors
- **Serverless & Edge** — alternative deployment models
- **CDN** — caching at the edge
- **Reverse Proxy** — nginx at the front door (TLS, LB, limits)

### Development Workflow (read third)
- **Build Tools** — bundlers, compilers, transpilers
- **Git Advanced** — branching, history rewriting, archaeology
- **Monorepo** — multi-package repos

### Methodology (skim)
- **Twelve-Factor App** — the canonical cloud-native principles

---

## Suggested Study Order

### Path A — Full-stack senior, 1-week prep
1. **Docker TL;DR + Dockerfile + Compose** (1.5 hrs) — must know
2. **Kubernetes TL;DR + Pods + Services** (2 hrs) — for K8s JDs
3. **CI/CD TL;DR + GitHub Actions** (1.5 hrs) — must know
4. **Observability TL;DR + OTel** (1.5 hrs) — must know
5. **Git Advanced TL;DR** (1 hr) — must know
6. Skim: Build Tools, Serverless, Monorepo, 12-Factor

### Path B — DevOps-focused, deep dive (2-3 weeks)
1. Docker: full (4-5 hrs)
2. Kubernetes: full (8-10 hrs)
3. CI/CD: full (4-5 hrs)
4. Observability: full (5-6 hrs)
5. Serverless, Build Tools, Git, Monorepo — as needed

### Path C — Interview tomorrow
- Docker: re-read Dockerfile + Multi-stage + Compose
- K8s: re-read Pods + Services + Deployments
- CI/CD: re-read GitHub Actions workflow
- Observability: re-read SLI/SLO + OpenTelemetry
- Git: re-read Rebase + Cherry-pick + Bisect

---

## Cross-References

- [Backend Stack](../20-backend/INDEX.md) — services that run on this platform
- [Architecture Stack](../30-architecture/INDEX.md) — architecture decisions involving platform
- [Quality Stack](../50-quality/INDEX.md) — testing, performance, production engineering

---

## Navigation

[← Previous: Backend](../20-backend/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Quality →](../50-quality/INDEX.md)
