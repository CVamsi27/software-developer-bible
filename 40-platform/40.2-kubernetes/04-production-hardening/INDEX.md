# Production Hardening

> **4 files.** The difference between a demo cluster and a production one: health probes, disruption budgets, RBAC + NetworkPolicies, and resource quotas. Every senior K8s interview drills into at least two of these.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Production%20Hardening-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Out of the box, a Deployment is fragile and insecure: no probes (traffic hits unready pods), no PDBs (node drains take out every replica at once), no RBAC (everything runs as the same service account), no quotas (one tenant starves the cluster). These four chapters close each gap with the standard production mechanism.

---

## File Index

| Order | File                                                          | Topics                                                                                           | Read time |
| --   :  | ------                                                          | --------                                                                                           | ----------: |
| 01    | [Health Checks](40.2.4.01-health-checks.md)                   | Liveness, readiness, startup probes; probe configuration; failure modes; probe-induced outages   | 25 min    |
| 02    | [Pod Disruption Budgets](40.2.4.02-pod-disruption-budgets.md) | minAvailable/maxUnavailable, voluntary disruptions, node drains, availability during maintenance | 20 min    |
| 03    | [RBAC & Network Policies](40.2.4.03-rbac-network-policies.md) | Roles, ClusterRoles, Bindings, ServiceAccounts; default-deny networking; micro-segmentation      | 30 min    |
| 04    | [Resource Quotas](40.2.4.04-resource-quotas.md)               | ResourceQuota, LimitRange, multi-tenant isolation, priority classes, monitoring usage            | 25 min    |

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

| Topic                           | Docita evidence                                                                                                                   |
| -------                           | -----------------                                                                                                                   |
| Health checks (probe analog)    | Fly `[checks.health]` on `/api/health/live` (15s interval, 240s grace); app-side `health-check.controller.ts`, `prisma.health.ts` |
| Image/container scanning        | `.github/workflows/container-scan.yml`                                                                                            |
| Tenant isolation (quota analog) | App-level: Postgres RLS (`shared/modules/rls/*`), ABAC authorization, tenant rate limiting — not cluster quotas                   |
| PDB / NetworkPolicy equivalents | _No direct docita implementation yet._                                                                                            |
