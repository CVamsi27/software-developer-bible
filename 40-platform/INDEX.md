# Platform Stack

> **Study time:** ≈ 13 h 19 m of reading (118 files, ~7 min average).
> **Docker, Kubernetes, CI/CD, Observability, Build Tools, Git, Serverless, Monorepo, 12-Factor, CDN, Reverse Proxy, IaC** — shared by both the [indian-sde-faang lane](../81-lanes-indian-sde-faang/INDEX.md) and the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> 118 files across 12 sub-stacks — the "how it runs" layer of the bible.

[![Files](https://img.shields.io/badge/files-118-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-12-green)](#the-12-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this stack matters

Platform questions connect application behavior to finite resources, release safety and recovery. Match depth to the role, then practice these concrete operations:
- Containerize an app with Docker (write a `Dockerfile`, use multi-stage builds)
- Explain Kubernetes architecture (pods, deployments, services, ingress)
- Set up CI/CD (GitHub Actions, blue-green, canary)
- Know observability (logging, metrics, tracing, OpenTelemetry)
- Understand build tools (Webpack vs Vite vs Turbopack)
- Use Git fluently (rebase, cherry-pick, bisect, submodules)

Each sub-stack establishes prerequisites, learning chapters, separate revision and interview practice. Explain what takes an input, which runtime/controller acts, and what observable evidence shows the result.

---

## The 12 Sub-Stacks (in study order)

| Order | Sub-stack | Files | Topics |
| ----: | -------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | [Docker](40.1-docker/INDEX.md) | 10 | Images, containers, volumes, networks, compose, multi-stage builds, production patterns |
| 2 | [Kubernetes](40.2-kubernetes/INDEX.md) | 17 | Pods, deployments, services, ingress, ConfigMaps, HPA, Helm, RBAC |
| 3 | [CI/CD](40.3-ci-cd/INDEX.md) | 11 | GitHub Actions, Docker build/deploy, blue-green/canary, Jenkins, GitLab CI, ArgoCD |
| 4 | [Observability](40.4-observability/INDEX.md) | 11 | Logging, monitoring, tracing, OpenTelemetry, error tracking, SLI/SLO/SLA, alerting |
| 5 | [Build Tools](40.5-build-tools/INDEX.md) | 10 | Webpack, Vite, Turbopack, Rspack, ESBuild, SWC, Babel |
| 6 | [Git Advanced](40.6-git-advanced/INDEX.md) | 10 | Internals (objects/refs/packfiles), branching, rebase, hooks, archaeology, LFS/partial clones, signed commits |
| 7 | [Serverless & Edge](40.7-serverless-edge/INDEX.md) | 10 | Lambda, Vercel Edge, serverless patterns, SAM/CDK/SST, durable execution (Temporal/Inngest) |
| 8 | [Monorepo](40.8-monorepo/INDEX.md) | 6 | Turborepo, Nx, pnpm, Rush, Bazel, versioning & publishing strategies |
| 9 | [Twelve-Factor App](40.9-twelve-factor/INDEX.md) | 2 | The canonical cloud-native methodology — codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes |
| 10 | [CDN & Edge](40.10-cdn/INDEX.md) | 4 | CDN caching strategies, invalidation, edge functions, multi-CDN steering, media optimization at the edge, PHI-at-edge considerations |
| 11 | [Reverse Proxy](40.11-reverse-proxy/INDEX.md) | 2 | Nginx internals: C10K, master–worker + epoll event loop, config contexts, sendfile vs proxy_pass, upstream LB algorithms, health checks, TLS termination, buffering, rate limiting, proxy_cache, zero-downtime reload, nginx vs HAProxy vs Envoy vs ALB |
| 12 | [IaC & Terraform](40.12-iac/INDEX.md) | 2 | Infrastructure as Code, HCL, state & drift, plan/apply, backends & locking, modules, workspaces, brownfield import, OpenTofu/Pulumi/CDKTF, IaC in CI/CD |

---

## Category Map (high-level)

Use these four layers to connect development, release and operation. The numbered sequence is a default; follow the role paths below when time is limited.

### Containers & Orchestration (read first)
- **Docker** — the unit of deployment
- **Kubernetes** — the orchestrator (if JD requires)

### Delivery & Operations (read second)
- **CI/CD** — build, test, deploy pipelines
- **Observability** — logs, metrics, traces, errors
- **IaC & Terraform** — how the infrastructure itself is provisioned and changed
- **Serverless & Edge** — alternative deployment models
- **CDN** — caching at the edge
- **Reverse Proxy** — nginx at the front door (TLS, LB, limits)

### Development Workflow (read third)
- **Build Tools** — bundlers, compilers, transpilers
- **Git Advanced** — branching, history rewriting, archaeology
- **Monorepo** — multi-package repos

### Methodology (connect to the deployment)
- **Twelve-Factor App** — connect configuration, process lifecycle and backing services to the application you actually operate

---

## Suggested Study Order

### Path A — Full-stack senior, 1-week prep
1. **Docker core: Dockerfile + Compose** (1.5 hrs) — must know
2. **Kubernetes core: Pods + Services** (2 hrs) — for K8s JDs
3. **CI/CD core: GitHub Actions** (1.5 hrs) — must know
4. **Observability core: signals + OpenTelemetry** (1.5 hrs) — must know
5. **Git Advanced essentials** (1 hr) — must know
6. **IaC essentials: plan, apply + state** (45 min) — for platform/DevOps-flavored JDs
7. Choose Build Tools, Serverless, Monorepo and Twelve-Factor chapters that match the job description.
8. Use each chosen category’s `REVISION.md`, then its interview bank. The time boxes are practice budgets; they do not replace the generated reading estimates.

### Path B — Platform-focused, deep dive (2-3 weeks)
1. Docker: full (4-5 hrs), including image provenance and runtime limits.
2. Kubernetes: full (8-10 hrs), including scheduling, rollout, disruption and recovery behavior.
3. CI/CD and GitOps: full (4-5 hrs), including artifact identity, promotion and rollback boundaries.
4. Observability: full (5-6 hrs), including signal design, alerting and incident evidence.
5. IaC and reverse proxies: trace state, plans, trusted proxy hops, TLS and safe configuration rollout.
6. CDN and edge: compare cache keys, invalidation, failover and the provider-specific execution model.
7. Serverless and Twelve-Factor: follow runtime limits, durable work, configuration and process lifecycle.
8. Build tools, Git and monorepos: choose the chapters that match the delivery architecture, then complete each selected section's revision and interview practice.

### Path C — Interview tomorrow

Use each selected stack’s revision companion first. Reopen a chapter only when you cannot explain its mechanism or a changed condition; then practice its interview questions.
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

[← Previous: Architecture](../30-architecture/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Quality →](../50-quality/INDEX.md)

---

## Docita Anchor

The local [Docita](https://github.com/CVamsi27/docita) source inspected on 10 October 2026 provides Docker, Fly.io configuration, GitHub Actions, monorepo tooling, Workers deployment and application-telemetry examples. Read the [dated evidence walkthrough](../projects/docita/INDEX.md) before using them in an interview or resume. Configuration presence does not prove deployment, service-objective achievement or every intended release gate.

In particular, the inspected deployment workflow has commented triggers; filesystem vulnerability scanning is not a scan of the built image, and CI latency budgets are not a measured production error budget. Explain the actual evidence and its limitations instead of repeating a broad production claim.

Kubernetes, Helm, GitOps, DORA dashboards and multi-CDN operation have no direct Docita implementation claim. They remain learning material for roles that require those decisions. Category anchors can point to a related mechanism without claiming the hypothetical exercise is deployed in Docita.
