# Core Workloads

> **Study time:** ≈ 33 min of reading (5 files, ~7 min average).
> **5 files.** What actually runs in a Kubernetes cluster: pods and ReplicaSets, Deployments on top, StatefulSets/DaemonSets for special cases, Jobs/CronJobs for batch. Read these before anything else in the K8s stack.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Workloads-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

These chapters explain how declared workloads become running processes or completed batch work. Start by tracing a Pod request through API storage, reconciliation, scheduling, node execution, and readiness; then follow the workload-specific guarantees. Those responsibilities stay separate even when one user command triggers the whole path.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Pods & ReplicaSets](40.2.1.01-pods-replicasets.md) | Control-plane request path, Pod lifecycle, init containers, sidecars, selectors, and replacement | Optional | Specialized | 8 min |
| 02 | [Deployments](40.2.1.02-deployments.md) | Trace template change through readiness; compare rollout strategies, HPA ownership and recovery | Optional | Specialized | 9 min |
| 03 | [StatefulSets & DaemonSets](40.2.1.03-statefulsets-daemonsets.md) | Stateful workloads (databases), stable network IDs, ordered rollout, node-level agents (logging, monitoring) | Optional | Specialized | 7 min |
| 04 | [Jobs & CronJobs](40.2.1.04-jobs-cronjobs.md) | Batch jobs, scheduled tasks, backoff, parallelism, completion modes, concurrency policy | Optional | Specialized | 7 min |

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
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Machine as replica analogy | `fly.toml [[vm]]` defines a 512 MB API machine and `min_machines_running = 0`; Fly machine scaling is not a Kubernetes ReplicaSet. The worker is a separate 256 MB app. |
| Deployment-like rollout | CI-driven deploys (`.github/workflows/deploy.yml`) against `apps/api/Dockerfile` with health-gated grace period |
| CronJob analog | The worker app enables Nest `@Cron` handlers; the API disables them. `CronHeartbeat` records outcomes for observability, but does not elect one worker or prevent duplicate execution. |
| StatefulSet / DaemonSet | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
