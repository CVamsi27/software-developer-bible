# Scaling

> **1 file.** Matching capacity to load: HorizontalPodAutoscaling driven by metrics, plus the cluster-capacity picture (nodes, overprovisioning) it depends on.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Scaling-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-in--progress-yellow)](#)

---

## Why this category exists

Kubernetes' core promise is elastic scale — but HPA does nothing until the metrics server exists, resource requests are honest, and the cluster has room to schedule into. This chapter covers pod autoscaling end to end and sets up the mental model for node-level capacity.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [HPA & Scaling](40.2.3.01-hpa-scaling.md) | Horizontal pod autoscaling, metrics server, custom metrics, scaling policies, VPA comparison | 30 min |

*Slot reserved: `40.2.3.02` node autoscaling & cluster capacity (upcoming chapter — no link yet).*

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — what gets scaled
- [Resource Quotas](../04-production-hardening/INDEX.md) — scaling within tenant limits

---

## Navigation

[← Networking & Config](../02-networking-and-config/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Production Hardening →](../04-production-hardening/INDEX.md)
