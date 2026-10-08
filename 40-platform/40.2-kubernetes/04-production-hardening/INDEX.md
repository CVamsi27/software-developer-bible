# Production Hardening

> **Study time:** ≈ 47 min of reading (5 files, ~9 min average).
> **5 files.** The difference between a demo cluster and a production one: health probes, disruption budgets, RBAC + NetworkPolicies, and resource quotas. Every senior K8s interview drills into at least two of these.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Production%20Hardening-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

A running replica can still be unable to serve, maintenance can remove useful capacity, API grants and network paths can expose neighboring workloads, and unrestricted resource requests can exhaust a shared cluster. Read probes first because readiness feeds availability decisions; then eviction budgets, access/network boundaries, and namespace admission budgets. These mechanisms answer different questions and need to be tested together.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Health Checks](40.2.4.01-health-checks.md) | Liveness, readiness, startup probes; probe configuration; failure modes; probe-induced outages | Optional | Specialized | 9 min |
| 02 | [Pod Disruption Budgets](40.2.4.02-pod-disruption-budgets.md) | minAvailable/maxUnavailable, voluntary disruptions, node drains, availability during maintenance | Optional | Specialized | 6 min |
| 03 | [RBAC & Network Policies](40.2.4.03-rbac-network-policies.md) | Roles, ClusterRoles, Bindings, ServiceAccounts; default-deny networking; micro-segmentation | Optional | Specialized | 10 min |
| 04 | [Resource Quotas](40.2.4.04-resource-quotas.md) | ResourceQuota, LimitRange, multi-tenant isolation, priority classes, monitoring usage | Optional | Specialized | 20 min |

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — what you are hardening
- [Observability Stack](../../../40-platform/40.4-observability/INDEX.md) — monitoring hardened clusters
- [Infra: Health Checks & Graceful Shutdown](../../../30-architecture/30.3-infra-patterns/01-liveness-lifecycle/INDEX.md) — the application-side contract

---

## Navigation

[← Scaling](../03-scaling/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Packaging & Extensibility →](../05-packaging-and-extensibility/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet_ — no probes/PDBs/RBAC objects; hardening happens at app + platform edges:

| Topic | Docita evidence |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Health checks (probe analog) | Fly `[checks.health]` on `/api/health/live` (15s interval, 240s grace); app-side `health-check.controller.ts`, `prisma.health.ts` |
| Image/container scanning | `.github/workflows/container-scan.yml` |
| Tenant isolation (quota analog) | App-level: Postgres RLS (`shared/modules/rls/*`), ABAC authorization, tenant rate limiting — not cluster quotas |
| PDB / NetworkPolicy equivalents | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
