# Core Workloads

> **Study time:** ≈ 55 min of reading (4 files, ~14 min average).
> **4 files.** What actually runs in a Kubernetes cluster: pods and ReplicaSets, Deployments on top, StatefulSets/DaemonSets for special cases, Jobs/CronJobs for batch. Read these before anything else in the K8s stack.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Workloads-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Every Kubernetes object you will ever touch is either one of these workload types or configures one of them. Interviews start here: "what's a pod?", "Deployment vs StatefulSet?", "how do you run something nightly?". Fluent answers to those questions are table stakes for any K8s JD.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Pods & ReplicaSets](40.2.1.01-pods-replicasets.md) | Pod lifecycle, init containers, sidecars, labels/selectors, RS scaling | 20 min |
| 02 | [Deployments](40.2.1.02-deployments.md) | Rolling updates, rollbacks, strategies, revision history, status management | 25 min |
| 03 | [StatefulSets & DaemonSets](40.2.1.03-statefulsets-daemonsets.md) | Stateful workloads (databases), stable network IDs, ordered rollout, node-level agents (logging, monitoring) | 5 min |
| 04 | [Jobs & CronJobs](40.2.1.04-jobs-cronjobs.md) | Batch jobs, scheduled tasks, backoff, parallelism, completion modes, concurrency policy | 5 min |

---

## Cross-References

- [Networking & Config](../02-networking-and-config/INDEX.md) — how traffic reaches these workloads
- [Production Hardening](../04-production-hardening/INDEX.md) — keeping them healthy under disruption

---

## Navigation

[↑ Kubernetes Home](../INDEX.md) · [Next: Networking & Config →](../02-networking-and-config/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet_ — the API runs as long-running Fly.io machines, not Kubernetes. Honest analogs only:

| Topic | Docita evidence |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| Machine ≈ pod replica | `fly.toml [[vm]]` — one 2GB machine, `min_machines_running` floor instead of a ReplicaSet |
| Deployment-like rollout | CI-driven deploys (`.github/workflows/deploy.yml`) against `apps/api/Dockerfile` with health-gated grace period |
| CronJob analog | Nest `@Cron` schedulers in the worker app, gated by `cron-heartbeat.ts` so only one instance fires |
| StatefulSet / DaemonSet | _No direct docita implementation yet._ |
