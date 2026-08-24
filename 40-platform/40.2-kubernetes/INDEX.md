# Kubernetes — Index

> **14 files** — Kubernetes orchestration from pods and replica sets to deployments, services, ingress, ConfigMaps, HPA, health checks, Helm, security, batch workloads, PDBs, resource quotas, admission injection, and interview questions.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-ff7f00)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Kubernetes:** The standard orchestrator for production container workloads. Mid-stage startups and large companies use K8s for everything. Senior interviews (especially at infra-heavy or scale-focused companies) test K8s architecture: pods, deployments, services, ingress, HPA, Helm, and the harder topics like PDBs, RBAC, and resource quotas.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Workloads](#workloads) | 4 | Pods, ReplicaSets, Deployments, StatefulSets, DaemonSets — what runs |
| [Networking](#networking) | 1 | Services, Ingress — how traffic gets in |
| [Configuration & Scaling](#configuration--scaling) | 3 | ConfigMaps, Secrets, HPA — how to configure and scale |
| [Reliability](#reliability) | 2 | Health checks, PDBs — keeping the system healthy |
| Batch & Scheduling (see Workloads) | 1 | Jobs, CronJobs — batch workloads |
| [Security & Multi-tenancy](#security--multi-tenancy) | 2 | RBAC, Network Policies, Resource Quotas — production concerns |
| [Packaging](#packaging) | 1 | Helm — the K8s package manager |
| [Interview Prep](#interview-prep) | 1 | 50+ Qs |

---

## Workloads

What runs in K8s. Read these first.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Pods & ReplicaSets](40.2.01-pods-replicasets.md) | Pod lifecycle, init containers, sidecars, RS scaling | 30 min |
| 02 | [Deployments](40.2.02-deployments.md) | Rolling updates, rollbacks, strategy, status management | 30 min |
| 09 | [StatefulSets & DaemonSets](40.2.09-statefulsets-daemonsets.md) | Stateful workloads (databases), stable network IDs, node-level agents (logging, monitoring) | 25 min |
| 10 | [Jobs & CronJobs](40.2.10-jobs-cronjobs.md) | Batch jobs, scheduled tasks, backoff, parallelism, completion mode | 25 min |

---

## Networking

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Services & Ingress](40.2.03-services-ingress.md) | ClusterIP, NodePort, LoadBalancer, Ingress controllers, TLS, host-based routing | 30 min |

---

## Configuration & Scaling

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [ConfigMaps & Secrets](40.2.04-configmaps-secrets.md) | ConfigMaps, Secrets, mounting, env vars, encryption at rest | 25 min |
| 05 | [HPA & Scaling](40.2.05-hpa-scaling.md) | Horizontal pod autoscaling, metrics server, custom metrics, VPA | 30 min |
| 13 | [PodPresets](40.2.13-podpresets.md) | Admission-time injection, env vars, volumes, secrets, label selectors, Kyverno alternatives | 15 min |

---

## Reliability

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Health Checks](40.2.06-health-checks.md) | Liveness, readiness, startup probes, probe configuration, failure modes | 25 min |
| 12 | [Pod Disruption Budgets](40.2.12-pod-disruption-budgets.md) | minAvailable, maxUnavailable, voluntary disruptions, node drainage, availability | 20 min |

---

## Security & Multi-tenancy

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 11 | [RBAC & Network Policies](40.2.11-rbac-network-policies.md) | Roles, ClusterRoles, Bindings, ServiceAccounts, NetworkPolicies, micro-segmentation | 30 min |
| 14 | [Resource Quotas](40.2.14-resource-quotas.md) | ResourceQuota, LimitRange, multi-tenant isolation, priority classes, monitoring | 25 min |

---

## Packaging

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [Helm](40.2.07-helm.md) | Charts, templates, values, releases, dependency management, helmfile | 30 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 08 | [Interview Questions](40.2.08-interview-questions.md) | 50+ curated questions with answers | 3 hrs |

---

## Suggested Study Order

1. **Workloads** (Pods, Deployments) — must know
2. **Networking** (Services, Ingress) — must know
3. **ConfigMaps & Secrets** — must know
4. **Health Checks** — must know
5. **HPA & Scaling** — for production scale
6. **Helm** — for the package manager
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
