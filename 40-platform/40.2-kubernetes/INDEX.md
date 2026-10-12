# Kubernetes — Index

> **Study time:** ≈ 3 h 53 m of reading (22 files, ~11 min average).
> **22 files** — Kubernetes orchestration from pods and replica sets to deployments, services, ingress, ConfigMaps, HPA, node autoscaling (Karpenter/Cluster Autoscaler), health checks, Helm, Kustomize, CRDs/operators, security, batch workloads, PDBs, resource quotas, admission injection, and interview questions.

[![Files](https://img.shields.io/badge/files-22-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Kubernetes:** Choose it when a shared control plane for scheduling and reconciling workloads is worth operating. It adds API, networking, upgrade and on-call responsibilities; a simpler application platform can be a better fit when those controls are unnecessary. Senior interviews test whether you can explain these mechanisms, their failure boundaries and the operational trade-offs.

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
| 01 | [Pods & ReplicaSets](01-core-workloads/40.2.1.01-pods-replicasets.md) | Pod lifecycle, init containers, sidecars, RS scaling | Optional | Specialized | 22 min |
| 02 | [Deployments](01-core-workloads/40.2.1.02-deployments.md) | Rolling updates, rollbacks, strategy, status management | Optional | Specialized | 9 min |
| 03 | [StatefulSets & DaemonSets](01-core-workloads/40.2.1.03-statefulsets-daemonsets.md) | Stateful workloads (databases), stable network IDs, node-level agents (logging, monitoring) | Optional | Specialized | 10 min |
| 04 | [Jobs & CronJobs](01-core-workloads/40.2.1.04-jobs-cronjobs.md) | Batch jobs, scheduled tasks, backoff, parallelism, completion mode | Optional | Specialized | 8 min |

---

## Networking & Config

How traffic and configuration get in.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Services & Ingress](02-networking-and-config/40.2.2.01-services-ingress.md) | ClusterIP, NodePort, LoadBalancer, Ingress controllers, TLS, host-based routing | Optional | Specialized | 9 min |
| 06 | [ConfigMaps & Secrets](02-networking-and-config/40.2.2.02-configmaps-secrets.md) | ConfigMaps, Secrets, mounting, env vars, encryption at rest | Optional | Specialized | 10 min |
| 07 | [PodPresets](02-networking-and-config/40.2.2.03-podpresets.md) | Admission-time injection, env vars, volumes, secrets, label selectors, Kyverno alternatives | Optional | Specialized | 5 min |

---

## Scaling

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [HPA & Scaling](03-scaling/40.2.3.01-hpa-scaling.md) | Horizontal pod autoscaling, metrics server, custom metrics, VPA | Optional | Specialized | 16 min |
| 09 | [Node Autoscaling & Cluster Capacity](03-scaling/40.2.3.02-node-autoscaling-cluster-capacity.md) | Cluster Autoscaler rules, Karpenter consolidation, node pools/taints, overprovisioning buffers, GPU/stateful caveats | Optional | Specialized | 17 min |

---

## Production Hardening

The senior-level reliability and security layer.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 10 | [Health Checks](04-production-hardening/40.2.4.01-health-checks.md) | Liveness, readiness, startup probes, probe configuration, failure modes | Optional | Specialized | 9 min |
| 11 | [Pod Disruption Budgets](04-production-hardening/40.2.4.02-pod-disruption-budgets.md) | minAvailable, maxUnavailable, voluntary disruptions, node drainage, availability | Optional | Specialized | 6 min |
| 12 | [RBAC & Network Policies](04-production-hardening/40.2.4.03-rbac-network-policies.md) | Roles, ClusterRoles, Bindings, ServiceAccounts, NetworkPolicies, micro-segmentation | Optional | Specialized | 11 min |
| 13 | [Resource Quotas](04-production-hardening/40.2.4.04-resource-quotas.md) | ResourceQuota, LimitRange, multi-tenant isolation, priority classes, monitoring | Optional | Specialized | 21 min |

---

## Packaging & Extensibility

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 14 | [Helm](05-packaging-and-extensibility/40.2.5.01-helm.md) | Chart templates and values, release revisions, rollback limits, dependencies, HTTP and OCI distribution | Optional | Specialized | 19 min |
| 15 | [Kustomize Overlays](05-packaging-and-extensibility/40.2.5.02-kustomize-overlays-packaging-tradeoffs.md) | Bases and overlays, strategic merge and JSON Patch, generators, transformers, Helm integration and secret handling | Optional | Specialized | 13 min |
| 16 | [CRDs, Operators & Controller Patterns](05-packaging-and-extensibility/40.2.5.03-crds-operators-controller-patterns.md) | CRD schema and versioning, reconciliation, ownership and garbage collection, finalizers, operator decision boundaries | Optional | Specialized | 17 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 17 | [Interview Questions](06-interview-prep/40.2.6.01-interview-questions.md) | Curated questions with answers | Optional | Specialized | 21 min |

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

- [Docker](../40.1-docker/INDEX.md) — build and run container images before Kubernetes schedules them
- [CI/CD](../40.3-ci-cd/INDEX.md) — verify and promote manifests and images into a cluster
- [Observability](../40.4-observability/INDEX.md) — distinguish service health from Kubernetes object state and resource signals
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — K8s vs serverless

---

## Navigation

[← Previous: Docker](../40.1-docker/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: CI/CD →](../40.3-ci-cd/INDEX.md)
