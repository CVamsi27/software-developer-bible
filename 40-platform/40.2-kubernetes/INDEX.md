# Kubernetes — Index

> **17 files** — Kubernetes orchestration from pods and replica sets to deployments, services, ingress, ConfigMaps, HPA, node autoscaling (Karpenter/Cluster Autoscaler), health checks, Helm, Kustomize, CRDs/operators, security, batch workloads, PDBs, resource quotas, admission injection, and interview questions.

[![Files](https://img.shields.io/badge/files-17-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Kubernetes:** The standard orchestrator for production container workloads. Mid-stage startups and large companies use K8s for everything. Senior interviews (especially at infra-heavy or scale-focused companies) test K8s architecture: pods, deployments, services, ingress, HPA, Helm, and the harder topics like PDBs, RBAC, and resource quotas.

---

## Category Map

| Category                  | Folder                                                                     | Files | What it covers                                                                       |
| ------------------------- | -------------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------ |
| Core Workloads            | [01-core-workloads/](01-core-workloads/INDEX.md)                           | 4     | Pods, ReplicaSets, Deployments, StatefulSets, DaemonSets, Jobs, CronJobs — what runs |
| Networking & Config       | [02-networking-and-config/](02-networking-and-config/INDEX.md)             | 3     | Services, Ingress, ConfigMaps, Secrets, PodPresets — traffic in, config in           |
| Scaling                   | [03-scaling/](03-scaling/INDEX.md)                                         | 2     | HPA, metrics pipeline, VPA, Cluster Autoscaler, Karpenter — capacity on demand       |
| Production Hardening      | [04-production-hardening/](04-production-hardening/INDEX.md)               | 4     | Health checks, PDBs, RBAC, NetworkPolicies, quotas — production concerns             |
| Packaging & Extensibility | [05-packaging-and-extensibility/](05-packaging-and-extensibility/INDEX.md) | 3     | Helm charts, Kustomize overlays, CRDs/operators/controller patterns                  |
| Interview Prep            | [06-interview-prep/](06-interview-prep/INDEX.md)                           | 1     | 50+ Qs                                                                               |

---

## Core Workloads

What runs in K8s. Read these first.

| #   | File                                                                                | Topics                                                                                      | Read time   |
| --: | ------                                                                              | --------                                                                                    | ----------: |
| 01  | [Pods & ReplicaSets](01-core-workloads/40.2.1.01-pods-replicasets.md)               | Pod lifecycle, init containers, sidecars, RS scaling                                        | 30 min      |
| 02  | [Deployments](01-core-workloads/40.2.1.02-deployments.md)                           | Rolling updates, rollbacks, strategy, status management                                     | 30 min      |
| 03  | [StatefulSets & DaemonSets](01-core-workloads/40.2.1.03-statefulsets-daemonsets.md) | Stateful workloads (databases), stable network IDs, node-level agents (logging, monitoring) | 25 min      |
| 04  | [Jobs & CronJobs](01-core-workloads/40.2.1.04-jobs-cronjobs.md)                     | Batch jobs, scheduled tasks, backoff, parallelism, completion mode                          | 25 min      |

---

## Networking & Config

How traffic and configuration get in.

| #   | File                                                                             | Topics                                                                                      | Read time   |
| --: | ------                                                                           | --------                                                                                    | ----------: |
| 05  | [Services & Ingress](02-networking-and-config/40.2.2.01-services-ingress.md)     | ClusterIP, NodePort, LoadBalancer, Ingress controllers, TLS, host-based routing             | 30 min      |
| 06  | [ConfigMaps & Secrets](02-networking-and-config/40.2.2.02-configmaps-secrets.md) | ConfigMaps, Secrets, mounting, env vars, encryption at rest                                 | 25 min      |
| 07  | [PodPresets](02-networking-and-config/40.2.2.03-podpresets.md)                   | Admission-time injection, env vars, volumes, secrets, label selectors, Kyverno alternatives | 15 min      |

---

## Scaling

| #   | File                                                                                             | Topics                                                                                                               | Read time   |
| --: | ------                                                                                           | --------                                                                                                             | ----------: |
| 08  | [HPA & Scaling](03-scaling/40.2.3.01-hpa-scaling.md)                                             | Horizontal pod autoscaling, metrics server, custom metrics, VPA                                                      | 30 min      |
| 09  | [Node Autoscaling & Cluster Capacity](03-scaling/40.2.3.02-node-autoscaling-cluster-capacity.md) | Cluster Autoscaler rules, Karpenter consolidation, node pools/taints, overprovisioning buffers, GPU/stateful caveats | 30 min      |

---

## Production Hardening

The senior-level reliability and security layer.

| #   | File                                                                                  | Topics                                                                              | Read time   |
| --: | ------                                                                                | --------                                                                            | ----------: |
| 10  | [Health Checks](04-production-hardening/40.2.4.01-health-checks.md)                   | Liveness, readiness, startup probes, probe configuration, failure modes             | 25 min      |
| 11  | [Pod Disruption Budgets](04-production-hardening/40.2.4.02-pod-disruption-budgets.md) | minAvailable, maxUnavailable, voluntary disruptions, node drainage, availability    | 20 min      |
| 12  | [RBAC & Network Policies](04-production-hardening/40.2.4.03-rbac-network-policies.md) | Roles, ClusterRoles, Bindings, ServiceAccounts, NetworkPolicies, micro-segmentation | 30 min      |
| 13  | [Resource Quotas](04-production-hardening/40.2.4.04-resource-quotas.md)               | ResourceQuota, LimitRange, multi-tenant isolation, priority classes, monitoring     | 25 min      |

---

## Packaging & Extensibility

| #   | File                                                                                                                    | Topics                                                                                                          | Read time   |
| --: | ------                                                                                                                  | --------                                                                                                        | ----------: |
| 14  | [Helm](05-packaging-and-extensibility/40.2.5.01-helm.md)                                                                | Charts, templates, values, releases, dependency management, helmfile                                            | 30 min      |
| 15  | [Kustomize Overlays](05-packaging-and-extensibility/40.2.5.02-kustomize-overlays-packaging-tradeoffs.md)                | Base/overlays, patches (strategic merge, JSON6902), generators, transformers, Helm vs Kustomize, secrets caveat | 25 min      |
| 16  | [CRDs, Operators & Controller Patterns](05-packaging-and-extensibility/40.2.5.03-crds-operators-controller-patterns.md) | CRD anatomy, reconcile loops, operator levels, ownerReferences/GC, when to build an operator, OLM               | 35 min      |

---

## Interview Prep

| #   | File                                                                      | Topics                             | Read time   |
| --: | ------                                                                    | --------                           | ----------: |
| 17  | [Interview Questions](06-interview-prep/40.2.6.01-interview-questions.md) | 50+ curated questions with answers | 3 hrs       |

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

## The Standard Production Manifest (memorize)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels: { app: my-app }
spec:
  replicas: 3
  selector:
    matchLabels: { app: my-app }
  template:
    metadata:
      labels: { app: my-app }
    spec:
      containers:
        - name: my-app
          image: my-app:1.2.3
          ports: [{ containerPort: 3000 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /health, port: 3000 }
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: 3000 }
            periodSeconds: 30
          envFrom:
            - configMapRef: { name: my-app-config }
            - secretRef: { name: my-app-secrets }
```

---

## Cross-References

- [Docker](../40.1-docker/INDEX.md) — K8s runs containers
- [CI/CD](../40.3-ci-cd/INDEX.md) — deploys to K8s
- [Observability](../40.4-observability/INDEX.md) — monitoring K8s workloads
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — K8s vs serverless

---

## Navigation

[← Previous: Docker](../40.1-docker/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: CI/CD →](../40.3-ci-cd/INDEX.md)
