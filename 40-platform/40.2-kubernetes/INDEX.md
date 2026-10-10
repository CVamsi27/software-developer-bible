# Kubernetes — Index

> **Study time:** ≈ 4 h 5 m of reading (22 files, ~11 min average).
> **22 files** — Kubernetes orchestration from pods and replica sets to deployments, services, ingress, ConfigMaps, HPA, node autoscaling (Karpenter/Cluster Autoscaler), health checks, Helm, Kustomize, CRDs/operators, security, batch workloads, PDBs, resource quotas, admission injection, and interview questions.

[![Files](https://img.shields.io/badge/files-22-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Kubernetes:** The standard orchestrator for production container workloads. It is useful when workload orchestration and platform control justify operating its API/controllers; simpler hosting can suit smaller deployments. Senior interviews (especially at infra-heavy or scale-focused companies) test K8s architecture: pods, deployments, services, ingress, HPA, Helm, and the harder topics like PDBs, RBAC, and resource quotas.

---

## Category Map

| Category | Folder | Files | What it covers |
| ------------------------- | -------------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------ |
| Core Workloads | [01-core-workloads/](01-core-workloads/INDEX.md) | 4 | Pods, ReplicaSets, Deployments, StatefulSets, DaemonSets, Jobs, CronJobs — what runs |
| Networking & Config | [02-networking-and-config/](02-networking-and-config/INDEX.md) | 3 | Services, Ingress, ConfigMaps, Secrets, PodPresets — traffic in, config in |
| Scaling | [03-scaling/](03-scaling/INDEX.md) | 2 | HPA, metrics pipeline, VPA, Cluster Autoscaler, Karpenter — capacity on demand |
| Production Hardening | [04-production-hardening/](04-production-hardening/INDEX.md) | 4 | Health checks, PDBs, RBAC, NetworkPolicies, quotas — production concerns |
| Packaging & Extensibility | [05-packaging-and-extensibility/](05-packaging-and-extensibility/INDEX.md) | 3 | Helm charts, Kustomize overlays, CRDs/operators/controller patterns |
| Interview Prep | [06-interview-prep/](06-interview-prep/INDEX.md) | 1 | Workload, networking, scaling and operations questions |

---

## Core Workloads

What runs in K8s. Read these first.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Pods & ReplicaSets](01-core-workloads/40.2.1.01-pods-replicasets.md) | Pod lifecycle, init containers, sidecars, RS scaling | Optional | 20 min | 21 min |
| 02 | [Deployments](01-core-workloads/40.2.1.02-deployments.md) | Rolling updates, rollbacks, strategy, status management | Optional | 25 min | 26 min |
| 03 | [StatefulSets & DaemonSets](01-core-workloads/40.2.1.03-statefulsets-daemonsets.md) | Stateful workloads (databases), stable network IDs, node-level agents (logging, monitoring) | Optional | 8 min | 10 min |
| 04 | [Jobs & CronJobs](01-core-workloads/40.2.1.04-jobs-cronjobs.md) | Batch jobs, scheduled tasks, backoff, parallelism, completion mode | Optional | 8 min | 9 min |

---

## Networking & Config

How traffic and configuration get in.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Services & Ingress](02-networking-and-config/40.2.2.01-services-ingress.md) | ClusterIP, NodePort, LoadBalancer, Ingress controllers, TLS, host-based routing | Optional | 8 min | 8 min |
| 06 | [ConfigMaps & Secrets](02-networking-and-config/40.2.2.02-configmaps-secrets.md) | ConfigMaps, Secrets, mounting, env vars, encryption at rest | Optional | 17 min | 10 min |
| 07 | [PodPresets](02-networking-and-config/40.2.2.03-podpresets.md) | Admission-time injection, env vars, volumes, secrets, label selectors, Kyverno alternatives | Optional | 5 min | 5 min |

---

## Scaling

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [HPA & Scaling](03-scaling/40.2.3.01-hpa-scaling.md) | Horizontal pod autoscaling, metrics server, custom metrics, VPA | Optional | 20 min | 14 min |
| 09 | [Node Autoscaling & Cluster Capacity](03-scaling/40.2.3.02-node-autoscaling-cluster-capacity.md) | Cluster Autoscaler rules, Karpenter consolidation, node pools/taints, overprovisioning buffers, GPU/stateful caveats | Optional | 14 min | 17 min |

---

## Production Hardening

The senior-level reliability and security layer.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 10 | [Health Checks](04-production-hardening/40.2.4.01-health-checks.md) | Liveness, readiness, startup probes, probe configuration, failure modes | Optional | 18 min | 9 min |
| 11 | [Pod Disruption Budgets](04-production-hardening/40.2.4.02-pod-disruption-budgets.md) | minAvailable, maxUnavailable, voluntary disruptions, node drainage, availability | Optional | 5 min | 6 min |
| 12 | [RBAC & Network Policies](04-production-hardening/40.2.4.03-rbac-network-policies.md) | Roles, ClusterRoles, Bindings, ServiceAccounts, NetworkPolicies, micro-segmentation | Optional | 7 min | 10 min |
| 13 | [Resource Quotas](04-production-hardening/40.2.4.04-resource-quotas.md) | ResourceQuota, LimitRange, multi-tenant isolation, priority classes, monitoring | Optional | 19 min | 21 min |

---

## Packaging & Extensibility

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 14 | [Helm](05-packaging-and-extensibility/40.2.5.01-helm.md) | Charts, templates, values, releases, dependency management, helmfile | Optional | 17 min | 19 min |
| 15 | [Kustomize Overlays](05-packaging-and-extensibility/40.2.5.02-kustomize-overlays-packaging-tradeoffs.md) | Base/overlays, patches (strategic merge, JSON6902), generators, transformers, Helm vs Kustomize, secrets caveat | Optional | 12 min | 13 min |
| 16 | [CRDs, Operators & Controller Patterns](05-packaging-and-extensibility/40.2.5.03-crds-operators-controller-patterns.md) | CRD anatomy, reconcile loops, operator levels, ownerReferences/GC, when to build an operator, OLM | Optional | 13 min | 16 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 17 | [Interview Questions](06-interview-prep/40.2.6.01-interview-questions.md) | Curated questions with answers | Optional | 20 min | 21 min |

---

## Suggested Study Order

1. **Workloads** (Pods, Deployments) — must know
2. **Networking** (Services, Ingress) — must know
3. **ConfigMaps & Secrets** — must know
4. **Health Checks** — must know
5. **HPA & Node Autoscaling** — for production scale
6. **Helm + Kustomize + Operators** — for the packaging/extension layer
7. **StatefulSets, Jobs, PDBs, RBAC, Resource Quotas** — as relevant to JD
8. **Interview Questions** — final review

---

## Connect the learning passes

Start with the [Deployment trace](01-core-workloads/40.2.1.02-deployments.md) to separate desired, scheduled, and available replicas. Then follow [traffic](02-networking-and-config/40.2.2.01-services-ingress.md) and [configuration delivery](02-networking-and-config/40.2.2.02-configmaps-secrets.md). Add [probes](04-production-hardening/40.2.4.01-health-checks.md) before reasoning about autoscaling and maintenance, because a running container is not necessarily useful capacity.

Use each category's revision companion after its chapters, then attempt the interview bank after all learning passes. The role-priority labels affect when to study a topic, not whether its control and failure boundaries exist. A copied “production manifest” cannot substitute for these application contracts; complete examples stay in their owning chapters.

---

## Cross-References

- [Docker](../40.1-docker/INDEX.md) — K8s runs containers
- [CI/CD](../40.3-ci-cd/INDEX.md) — deploys to K8s
- [Observability](../40.4-observability/INDEX.md) — monitoring K8s workloads
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — K8s vs serverless

---

## Navigation

[← Previous: Docker](../40.1-docker/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: CI/CD →](../40.3-ci-cd/INDEX.md)
