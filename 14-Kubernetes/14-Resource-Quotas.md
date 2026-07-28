[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

# Resource Quotas

## Definition

**ResourceQuota** is a Kubernetes resource that provides constraints on aggregate resource consumption per namespace — limiting total CPU, memory, storage, and object counts (pods, services, configmaps, etc.) that can be used by all pods in a namespace. **LimitRange** complements ResourceQuota by setting default resource requests/limits and enforcing min/max constraints at the container level. Together they implement resource governance and multi-tenant isolation on a shared cluster.

## Why Do We Need It?

1. **Fair resource sharing** — Prevent one team/namespace from consuming all cluster resources
2. **Cost control** — Enforce resource budgets per namespace for chargeback/showback
3. **Capacity planning** — Predictable resource allocation across teams
4. **Quality of Service** — Ensure critical workloads get guaranteed resources
5. **Abuse prevention** — Stop runaway pods or deployments from exhausting cluster capacity

## How It Works

### Resource Quota Flow

```text
ResourceQuota Enforcement:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                   QUOTA ENFORCEMENT FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Before Pod Creation:                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. User creates Pod with requests: CPU=1, Memory=1Gi   │    │
│  │                                                          │    │
│  │  2. API Server checks ResourceQuota:                    │    │
│  │     ├── Quota: requests.cpu: 10 total                    │    │
│  │     ├── Used: 9.5                                        │    │
│  │     ├── Available: 0.5                                   │    │
│  │     ├── Requested: 1.0 (exceeds available!)             │    │
│  │     └── REJECTED: "exceeded quota"                       │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  3. User adjusts Pod: requests: CPU=500m, Memory=512Mi  │    │
│  │                                                          │    │
│  │  4. API Server checks ResourceQuota:                    │    │
│  │     ├── Available: 0.5 CPU, 2Gi Memory                   │    │
│  │     ├── Requested: 0.5 CPU, 512Mi Memory                │    │
│  │     └── ACCEPTED                                          │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

### ResourceQuota vs LimitRange

```text
Scope and Purpose:
═══════════════════════════════════════════════════════════════

ResourceQuota (Namespace scope):
├── Limits TOTAL resources in a namespace
├── CPU, Memory, Storage, PVC count, Pod count
├── Hard limits (can't be exceeded)
├── Applies to aggregate of all pods
└── Only applies when a resource is specified in the pod spec

LimitRange (Container scope):
├── Sets default requests/limits if not specified
├── Min/max constraints per container
├── Enforces ratio between request and limit
├── Applies per-container
└── Fills in gaps when pod doesn't specify resources

Example interaction:
├── LimitRange sets default: CPU limit=500m
├── Pod doesn't specify resources
├── LimitRange injects CPU limit=500m
├── ResourceQuota now counts this pod's CPU
└── Without LimitRange, pod would have unlimited CPU!

```

## Code Examples

### 1. Basic ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-a
spec:
  hard:
    # Compute resources
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"

    # Storage resources
    requests.storage: "100Gi"
    persistentvolumeclaims: "10"

    # Object counts
    pods: "50"
    services: "10"
    configmaps: "20"
    secrets: "20"
    services.loadbalancers: "2"
    services.nodeports: "5"
    replicationcontrollers: "20"
```

### 2. ResourceQuota with Scopes

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    limits.cpu: "40"
    limits.memory: "80Gi"
  scopes:
  - NotTerminating  # Excludes pods with activeDeadlineSeconds set
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: best-effort-quota
  namespace: production
spec:
  hard:
    pods: "10"
  scopes:
  - BestEffort  # Only applies to BestEffort QoS pods
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: burstable-quota
  namespace: production
spec:
  hard:
    pods: "30"
  scopes:
  - NotTerminating  # Includes Burstable and Guaranteed QoS
  - NotBestEffort
```

### 3. LimitRange with Defaults

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: container-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
    maxLimitRequestRatio:
      cpu: "4"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: pvc-limits
  namespace: team-a
spec:
  limits:
  - type: PersistentVolumeClaim
    max:
      storage: "100Gi"
    min:
      storage: "1Gi"
```

### 4. Multi-Tenant Quotas

```yaml
# Namespace for Team A
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "16"
    requests.memory: "32Gi"
    limits.cpu: "32"
    limits.memory: "64Gi"
    pods: "40"
    services: "10"
    persistentvolumeclaims: "20"
---
# Namespace for Team B
apiVersion: v1
kind: Namespace
metadata:
  name: team-b
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-b-quota
  namespace: team-b
spec:
  hard:
    requests.cpu: "8"
    requests.memory: "16Gi"
    limits.cpu: "16"
    limits.memory: "32Gi"
    pods: "20"
    services: "5"
    persistentvolumeclaims: "10"
---
# Unified LimitRange applied to both namespaces
apiVersion: v1
kind: LimitRange
metadata:
  name: team-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    default:
      cpu: "200m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    max:
      cpu: "4"
      memory: "16Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: team-limits
  namespace: team-b
spec:
  limits:
  - type: Container
    default:
      cpu: "200m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    max:
      cpu: "2"
      memory: "8Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
```

### 5. Priority Class Quotas

```yaml
# Priority classes for workload differentiation
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority workloads (critical production)"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 100
globalDefault: false
description: "Low priority workloads (batch, non-critical)"
---
# Quota scoped by priority class
apiVersion: v1
kind: ResourceQuota
metadata:
  name: high-priority-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    pods: "10"
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values:
      - high-priority
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: low-priority-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    pods: "40"
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values:
      - low-priority
```

### 6. Viewing Quota Usage

```bash
# View quotas in a namespace
kubectl get resourcequota -n team-a

# Detailed view
kubectl describe resourcequota team-quota -n team-a
# Name:         team-quota
# Namespace:    team-a
# Resource      Used  Hard
# --------      ---   ----
# requests.cpu  8.5   10
# requests.memory 15Gi  20Gi
# limits.cpu    16    20
# limits.memory 30Gi  40Gi
# pods          35    50
# services      5     10

# View limit ranges
kubectl get limitrange -n team-a
kubectl describe limitrange container-limits -n team-a

# Check quota usage across all namespaces
kubectl get resourcequota --all-namespaces

# Custom columns
kubectl get quota -n team-a -o custom-columns=\
  NAME:.metadata.name,\
  CPU-REQ:.status.hard.'requests\.cpu',\
  CPU-REQ-USED:.status.used.'requests\.cpu',\
  MEM-REQ:.status.hard.'requests\.memory',\
  MEM-REQ-USED:.status.used.'requests\.memory'
```

### 7. Pod Requesting Resources

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: quota-aware-pod
  namespace: team-a
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        cpu: "200m"
        memory: "512Mi"
      limits:
        cpu: "500m"
        memory: "1Gi"
  # Without these resource requests:
  # - LimitRange injects defaults
  # - ResourceQuota tracks them
```

### 8. Quota Enforcement Error

```bash
# Attempt to create a pod that exceeds quota
kubectl apply -f big-pod.yaml
# Error: 
#   Error from server (Forbidden): error when creating "big-pod.yaml":
#   pods "big-pod" is forbidden: exceeded quota:
#   team-quota, requested: requests.cpu=4,
#   used: requests.cpu=9.5, limited: requests.cpu=10
```

## Real-World Use Cases

| Scenario | ResourceQuota | LimitRange |
|----------|--------------|------------|
| **Multi-team cluster** | Per-team CPU/memory caps | Default container sizes |
| **Production vs staging** | Prod gets 3x resources | Staging gets smaller defaults |
| **CI/CD pipelines** | Job-specific quotas | Container max limits |
| **Free tier vs paid tier** | Tier-based resource budgets | Min resource guarantees |
| **Batch vs real-time** | Priority class quotas | QoS class defaults |

## Common Mistakes

### 1. No LimitRange with ResourceQuota

```text
// ❌ BAD: ResourceQuota without LimitRange
// Pods without resource requests DON'T count against quota
// A pod without requests can consume unlimited CPU!
ResourceQuota: requests.cpu = "10"
Pod: no requests specified → NOT counted!
10 such pods → uses unlimited CPU

// ✅ GOOD: Always pair with LimitRange
LimitRange: default requests.cpu = "100m"
Pod: no requests specified → LimitRange injects 100m → COUNTED!
```

### 2. Overly Restrictive Limits

```yaml
# ❌ BAD: Too tight — can't run any real workload
spec:
  hard:
    requests.cpu: "1"
    pods: "2"

# ✅ GOOD: Right-size based on actual needs
spec:
  hard:
    requests.cpu: "10"
    pods: "30"
    requests.memory: "20Gi"
```

### 3. Not Planning for Quota Headroom

```yaml
# ❌ BAD: No headroom — rolling update fails
spec:
  hard:
    pods: "3"
# Deployment with 3 replicas can't do rolling update
# (needs extra pod during update)

# ✅ GOOD: Account for deployment strategy
spec:
  hard:
    pods: "6"
# Can do rolling updates with 3 replicas + surge
```

### 4. Different Quotas for Different Priorities

```yaml
# ❌ BAD: Single quota — low-priority can starve high-priority
spec:
  hard:
    requests.cpu: "20"
    # All pods share 20 CPUs regardless of priority

# ✅ GOOD: Separate quotas by priority
apiVersion: v1
kind: ResourceQuota
metadata:
  name: high-priority
spec:
  hard:
    requests.cpu: "10"
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values: ["high"]
```

## Best Practices

1. **Always create LimitRange with ResourceQuota** — Otherwise pods without resource requests bypass quota

2. **Set default requests/limits** — LimitRange `default` and `defaultRequest` prevent unbounded pods

3. **Use priority classes for isolation** — Separate quotas for critical vs batch workloads

4. **Monitor quota utilization** — Alert when usage exceeds 80% of hard limits

5. **Plan headroom for deployments** — Account for surge during rolling updates

6. **Document quota decisions** — Why each namespace gets its specific limits

7. **Use namespaces for isolation** — One ResourceQuota per namespace

8. **Review and adjust regularly** — Quotas need tuning as workloads evolve

## Summary

- ResourceQuota sets aggregate limits on CPU, memory, storage, and object counts per namespace
- LimitRange sets per-container defaults and min/max constraints
- ResourceQuota without LimitRange is ineffective — pods without resource requests are not counted
- Use priority classes to differentiate critical vs best-effort workloads within the same namespace
- Monitor utilization and plan for headroom, especially for rolling updates

## Cheat Sheet

```yaml
# Basic ResourceQuota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-quota
  namespace: my-ns
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    pods: "30"
---
# Basic LimitRange
apiVersion: v1
kind: LimitRange
metadata:
  name: my-limits
  namespace: my-ns
spec:
  limits:
  - type: Container
    default:
      cpu: "200m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
```

```bash
# Commands
kubectl get quota -n <ns>
kubectl describe quota <name> -n <ns>
kubectl get limitrange -n <ns>
kubectl describe limitrange <name> -n <ns>
kubectl get quota --all-namespaces
```

```text
ResourceQuota Key Points:
├── Scope: Per-namespace aggregate limits
├── Resources: CPU, memory, storage, object counts
├── Enforcement: Admission controller rejects if exceeded
├── Pair with: LimitRange (defaults for missing specs)
├── Scopes: BestEffort, NotTerminating, PriorityClass
└── Monitor: Usage vs Hard limits (alert at 80%)

LimitRange Key Points:
├── Scope: Per-container (or per-PVC) constraints
├── Defaults: Fills in when pod doesn't specify resources
├── Min/Max: Rejects pods outside allowed range
├── Ratio: maxLimitRequestRatio prevents overcommit
└── Required for: Making ResourceQuota effective
```

---

## See Also

- [ConfigMaps & Secrets](04-ConfigMaps-Secrets.md)
- [HPA & Scaling](05-HPA-Scaling.md)
- [Interview Questions](08-Interview-Questions.md)
- [Pods & ReplicaSets](01-Pods-ReplicaSets.md)
- [RBAC & Network Policies](11-RBAC-Network-Policies.md)

## References & Learn More

- [K8s ResourceQuota Docs](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [K8s LimitRange Docs](https://kubernetes.io/docs/concepts/policy/limit-range/)
- [K8s Managing Resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Multi-Tenancy Best Practices](https://kubernetes.io/docs/concepts/security/multi-tenancy/)
- [Resource Quotas with Priority Classes](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scopes)
