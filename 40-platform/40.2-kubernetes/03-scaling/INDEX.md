# Scaling

> **2 files.** Matching capacity to load: HorizontalPodAutoscaling driven by metrics, plus node-level autoscaling (Cluster Autoscaler vs Karpenter) that gives pods somewhere to schedule.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Scaling-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Kubernetes' core promise is elastic scale — but HPA does nothing until the metrics server exists, resource requests are honest, and the cluster has room to schedule into. These chapters cover pod autoscaling end to end and the node-capacity picture it depends on: pending pods, scale-down safety rules, overprovisioning buffers, and GPU/stateful caveats.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [HPA & Scaling](40.2.3.01-hpa-scaling.md) | Horizontal pod autoscaling, metrics server, custom metrics, scaling policies, VPA comparison | 30 min |
| 02 | [Node Autoscaling & Cluster Capacity](40.2.3.02-node-autoscaling-cluster-capacity.md) | Cluster Autoscaler scale-up/down rules, Karpenter direct provisioning + consolidation, node pools/taints, overprovisioning buffers, GPU/stateful scale-from-zero | 30 min |

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
|-------|-----------------|
| HPA analog (per-machine concurrency) | `fly.toml [http_service.concurrency]` — soft 60 / hard 100 requests per machine |
| Scheduled scaling | `.github/workflows/scale-api-hours.yml` grows/shrinks machines with IST business hours |
| Scale-to-zero | ADR 0011: `auto_stop_machines='suspend'`, auto-start on request |
| Node autoscaling / VPA / Karpenter | _No direct docita implementation yet._ |
