# Twelve-Factor App — Index

> **Study time:** ≈ 16 min of reading (3 files, ~5 min average).
> **3 files** — Read the original twelve-factor methodology, then use its interview bank and revision guide to diagnose deployment inputs, durable resources, and replaceable processes. A community refresh is underway; this section distinguishes the original text from later proposals.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why study Twelve-Factor:** The original factors provide a shared vocabulary for discussing service portability, deployment inputs, attached resources, and process lifecycle. Use them to identify a design boundary and its trade-offs; they are not a compliance certificate. The original text remains published while its community refresh is in progress.

---

## Factor Categories

The original twelve factors are grouped here into four study categories. This grouping is editorial, not an extra part of the methodology.

| Category | Original factors | The principle in one line |
| ---------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Build & Ship](#factor-categories) | 1 Codebase · 2 Dependencies · 5 Build/Release/Run | One codebase per app; declare dependencies and separate build from release and run |
| [Config & Bindings](#factor-categories) | 3 Config · 4 Backing services | The original recommends env vars; bindings select compatible attached resources |
| [Runtime Model](#factor-categories) | 6 Processes · 7 Port binding · 8 Concurrency · 9 Disposability | Stateless processes, self-port-binding, scale by process count, die gracefully |
| [Operational Parity](#factor-categories) | 10 Dev/prod parity · 11 Logs · 12 Admin processes | Reduce relevant differences between environments; logs are event streams; admin = one-off processes |
| Optional book extensions | API first · Telemetry · Authentication and authorization | Additional concerns discussed in a 2016 book; not part of the original twelve or an official update |

---

## The 12 Factors (memorize the names)

| # | Factor | One-line description |
| --: | -------- | --------------------- |
| 1 | **Codebase** | One codebase tracked in Git, many deploys |
| 2 | **Dependencies** | Explicitly declare and isolate dependencies |
| 3 | **Config** | Store config in the environment (env vars, not code) |
| 4 | **Backing services** | Treat backing services as attached resources |
| 5 | **Build, release, run** | Strictly separate build and run stages |
| 6 | **Processes** | Execute the app as one or more stateless processes |
| 7 | **Port binding** | Export services via port binding (a self-contained server) |
| 8 | **Concurrency** | Scale out via the process model |
| 9 | **Disposability** | Fast startup, graceful shutdown |
| 10 | **Dev/prod parity** | Keep dev, staging, and prod as similar as possible |
| 11 | **Logs** | Treat logs as event streams |
| 12 | **Admin processes** | Run admin/maintenance tasks as one-off processes |

**Beyond the original factors:** Kevin Hoffman’s 2016 book discusses API first, telemetry, and authentication/authorization as additional concerns. They are useful topics, not an official replacement factor list. The [community refresh](https://github.com/twelve-factor/twelve-factor) remains in progress.

---

## The Files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [The Twelve-Factor App](40.9.01-the-twelve-factor-app.md) | Original factors, current status, operational examples, and clearly labeled later proposals | Important | Important | 9 min |
| — | [Section revision](REVISION.md) | Retrieval prompts for release identity, process replacement, configuration, logs, and operational boundaries | Important | Important | 2 min |
| 02 | [Twelve-Factor App Interview Questions](40.9.02-interview-questions.md) | Diagnostic Q&A: the factors as diagnosis (violation → incident → fix), build/release/run immutability, process-type scaling, migrations as one-off releases, K8s/serverless mapping, scenario drills (slow-boot autoscaling, MemoryStore incident, "is 12-factor obsolete?") | Important | Important | 5 min |

---

## Reading Passes

1. Trace a replacement failure, then read the factor groups and worker recovery example.
2. Close the chapter and use [section revision](REVISION.md). Explain the altered-condition questions before checking answers.
3. Attempt the [separate interview bank](40.9.02-interview-questions.md), using evidence from your own deployments.

---

## Common interview questions

The full bank with model answers: → [40.9.02 Interview Questions](40.9.02-interview-questions.md). The headlines:
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

---

## Docita Anchor

These existing [Docita](https://github.com/CVamsi27/docita) pointers locate related configuration and deployment code. They are investigation starting points; the paths alone do not establish production readiness or measured compliance.

| Topic | Docita evidence |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| III. Config in env | `apps/api/src/shared/modules/config/env-schema.ts` validates runtime env; `turbo.json` declares shared env inputs for task hashing and passthrough, with additional task-level inputs |
| IV. Backing services as attached resources | Swapped by env: `QUEUE_BACKEND=postgres`, `CACHE_BACKEND=memory`, `STORAGE_PROVIDER=r2` (fly.toml) |
| VI. Processes | Stateless API + separate worker app; inspect replacement and accepted-work recovery; `auto_stop_machines` alone does not prove disposability |
| V. Build/release/run | `turbo.json` defines build task inputs/outputs. `.github/workflows/deploy.yml` runs a `migrate-db` job before API/worker deployment; API deploy also depends on startup-smoke and latency gates. The separate migration-validation job in `ci.yml` is manually triggered. |
| XI. Logs | Pino defaults to stdout; its options disable automatic request logs and configure request serializers plus patient health information (PHI) redaction for payloads and errors in `apps/api/src/shared/modules/observability/`. This code does not establish collector durability or retention. |
| X. Dev/prod parity | `docker-compose.yml` provides local PostgreSQL 15 with `pg_stat_statements`; this does not prove parity. Compare the deployed database and test production-specific permissions, latency, scale, and failure behavior. |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
