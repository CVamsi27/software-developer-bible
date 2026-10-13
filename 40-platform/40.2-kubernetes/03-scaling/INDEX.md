# Scaling

> **Study time:** ≈ 26 min of reading (3 files, ~9 min average).
> **3 files.** Matching capacity to load: HorizontalPodAutoscaling driven by metrics, plus node-level autoscaling (Cluster Autoscaler vs Karpenter) that gives pods somewhere to schedule.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Scaling-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Workload autoscaling needs a reliable metric and honest resource requests; node autoscaling needs a Pod that cannot currently schedule and a feasible provider capacity option. These chapters trace both control loops, their interaction, and the safety and latency constraints that shape scale-up and scale-down.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [HPA & Scaling](40.2.3.01-hpa-scaling.md) | Horizontal Pod Autoscaling, resource and external metrics, scale-to-zero, scaling policies, VPA comparison | Optional | Specialized | 15 min |
| 02 | [Node Autoscaling & Cluster Capacity](40.2.3.02-node-autoscaling-cluster-capacity.md) | Cluster Autoscaler and Karpenter, placement and provisioning, node pools, disruption, overprovisioning, GPU and stateful workloads | Optional | Specialized | 9 min |

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — what gets scaled
- [Resource Quotas](../04-production-hardening/INDEX.md) — scaling within tenant limits

---

## Navigation

[← Networking & Config](../02-networking-and-config/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Production Hardening →](../04-production-hardening/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet_ — no HPA/Karpenter; scaling is deliberate Fly.io mechanics:

| Topic | Docita evidence |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fly Proxy request concurrency | `fly.toml [http_service.concurrency]` sets soft 60 / hard 100 requests per machine. Proxy concurrency helps route requests and start an existing stopped machine; it does not create machines or implement an HPA control loop. [Fly Proxy autostop/autostart](https://fly.io/docs/reference/fly-proxy-autostop-autostart/) |
| Scheduled scaling | `.github/workflows/scale-api-hours.yml` defines 8:30 AM/PM IST cron runs, but GitHub's Actions API reported `disabled_manually` on 2026-10-12; the configured schedule is not active. |
| Idle suspend and wake | `fly.toml` sets `auto_stop_machines='suspend'`, `auto_start_machines=true`, and `min_machines_running=0`; Fly Proxy suspends and wakes existing machines based on traffic, but does not create or destroy machines. |
| Node autoscaling / VPA / Karpenter | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
