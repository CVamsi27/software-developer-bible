# Twelve-Factor App — Index

> **1 file** — The canonical cloud-native methodology. The vocabulary of modern DevOps, platform engineering, and senior backend interviews. Every Kubernetes, Heroku, Fly, Vercel, and Lambda deployment is built around these 12 factors.

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Twelve-Factor:** This is the **vocabulary** of modern cloud-native apps. When a senior interviewer says "is this app twelve-factor?" they mean: does it follow the principles that make cloud deployment work? Read this file once — it's the lingua franca of platform engineering.

---

## Factor Categories

The 12 (+3) factors classify into 4 conceptual families — the way to *recall* them under pressure.

| Category | Factors | The principle in one line |
|----------|---------|---------------------------|
| [Build & Ship](#factor-categories) | 1 Codebase · 2 Dependencies · 5 Build/Release/Run | One repo → deterministic build → immutable release |
| [Config & Bindings](#factor-categories) | 3 Config · 4 Backing services | Config lives in env; backing services are swappable attached resources |
| [Runtime Model](#factor-categories) | 6 Processes · 7 Port binding · 8 Concurrency · 9 Disposability | Stateless processes, self-port-binding, scale by process count, die gracefully |
| [Operational Parity](#factor-categories) | 10 Dev/prod parity · 11 Logs · 12 Admin processes | Same environments everywhere; logs are event streams; admin = one-off processes |
| *(15-factor extension)* | API first · Telemetry · Auth | The modern add-ons for API + observability + security concerns |

---

## The 12 Factors (memorize the names)

| # | Factor | One-line description |
|--:|--------|---------------------|
| 1 | **Codebase** | One codebase tracked in Git, many deploys |
| 2 | **Dependencies** | Explicitly declare and isolate dependencies |
| 3 | **Config** | Store config in the environment (env vars, not code) |
| 4 | **Backing services** | Treat backing services as attached resources |
| 5 | **Build, release, run** | Strictly separate build and run stages |
| 6 | **Processes** | Execute the app as one or more stateless processes |
| 7 | **Port binding** | Export services via port binding (no embedded web server) |
| 8 | **Concurrency** | Scale out via the process model |
| 9 | **Disposability** | Fast startup, graceful shutdown |
| 10 | **Dev/prod parity** | Keep dev, staging, and prod as similar as possible |
| 11 | **Logs** | Treat logs as event streams |
| 12 | **Admin processes** | Run admin/maintenance tasks as one-off processes |

**Plus the unofficial 15-factor extension:**
- **API first** — design the API contract before implementation
- **Telemetry** — instrument everything (metrics, traces, logs)
- **Auth** — authentication as a separate concern

---

## The File

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [The Twelve-Factor App](40.9.01-the-twelve-factor-app.md) | All 12 factors + the 15-factor extension, with examples, anti-patterns, and "how to comply" guidance | 60 min |

---

## When to read

- **Always** — once, before any cloud-native interview
- 60 min read
- Then reference back when discussing app architecture

---

## Common interview questions

- "Walk me through the 12 factors. Which ones does your app violate?"
- "How do you handle config in your app?" (Factor 3)
- "How do you handle database migrations in production?" (Factor 5 + Factor 12)
- "What does 'stateless processes' mean for your app?" (Factor 6)
- "How do you handle logs?" (Factor 11)

---

## Cross-References

- [Docker](../40.1-docker/INDEX.md) — Factor 2 (dependencies), Factor 6 (processes)
- [Kubernetes](../40.2-kubernetes/INDEX.md) — Factor 6 (processes), Factor 8 (concurrency)
- [CI/CD](../40.3-ci-cd/INDEX.md) — Factor 5 (build/release/run)
- [Observability](../40.4-observability/INDEX.md) — Factor 11 (logs)
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — Factor 4 (backing services)

---

## Navigation

[← Previous: Monorepo](../40.8-monorepo/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Quality →](../../50-quality/INDEX.md)
