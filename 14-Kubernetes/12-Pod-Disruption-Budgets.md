# Pod Disruption Budgets

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

limits the number of pods that can be unavailable simultaneously during **voluntary disruptions** — intentional actions like node maintenance, cluster upgrades, autoscaling down, or draining nodes for repairs. PDBs ensure that a minimum number or percentage of pods remain available during these operations, protecting application availability.

## Why Do We Need It?

1. **Availability guarantees** — Ensure minimum pods stay up during maintenance
2. **Safe cluster operations** — Node upgrades, kernel patches without app downtime
3. **Controlled scaling down** — Prevent HPA or Cluster Autoscaler from taking down too many pods
4. **SLA compliance** — Meet uptime requirements during planned disruptions
5. **Graceful eviction** — Pods get `PreStop` hooks time to shut down cleanly

## How It Works

### Voluntary vs Involuntary Disruptions

```text
Disruption Types:
═══════════════════════════════════════════════════════════════

Voluntary Disruptions (PDB-protectable):
├── Draining a node for maintenance
├── Cluster upgrade (kubelet, k8s version)
├── Pod eviction by Cluster Autoscaler
├── Reducing Deployment replica count
├── Descheduling (e.g., descheduler DaemonSet)
└── Node reboot for kernel update

Involuntary Disruptions (NOT PDB-protectable):
├── Hardware failure (disk, memory, CPU)
├── Network partition
├── Node power outage
├── Out-of-memory / Out-of-disk kills
└── Node crashes

```

### PDB Mechanics

```text
PDB Evaluation:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                  PDB ENFORCEMENT FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User/Admin initiates voluntary disruption                │
│     (e.g., kubectl drain node-1)                            │
│                                                              │
│  2. K8s checks PDB for pods on that node                    │
│                                                              │
│  3. PDB calculates:                                          │
│     ├── Allowed disruptions = max(0, current - minAvailable) │
│     │   OR                                                    │
│     └── Already disrupted = ...                              │
│                                                              │
│  4. If disruption allowed:                                   │
│     ├── Pod gets evicted                                      │
│     ├── PreStop hook runs (graceful shutdown)                │
│     └── Replacement pod scheduled elsewhere                  │
│                                                              │
│  5. If disruption NOT allowed:                               │
│     ├── Eviction fails with error                            │
│     ├── Node drain pauses or fails                           │
│     └── Pod remains running                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### PDB Calculation

```text
PDB Math:
═══════════════════════════════════════════════════════════════

Scenario: 3 replicas, maxUnavailable=1

Allowed evictions:
├── Current replicas: 3
├── Already disrupted: 0
├── Max unavailable: 1
├── Can evict: min(1, 3 - 0) = 1 ✅
└── After eviction: 2 running, 1 unavailable

Next eviction attempt:
├── Current replicas: 3
├── Already disrupted: 1
├── Max unavailable: 1
├── Can evict: min(1, 3 - 1) = 1 ✅
└── After eviction: 1 running, 2 unavailable
    (Wait, replica count catches up...)

With Deployment controller:
├── Deployment ensures desired replicas
├── When one pod evicted, replacement already coming
├── So effective availability stays high
└── PDB prevents too many concurrent evictions

```

## Code Examples

### 1. Basic PDB with maxUnavailable

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: web
```

### 2. PDB with minAvailable

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: api
```

### 3. PDB with Percentage

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: worker-pdb
spec:
  minAvailable: "50%"
  selector:
    matchLabels:
      app: worker
```

### 4. Multiple PDBs for Different Tiers

```yaml
# Frontend — high availability, can lose some pods
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: frontend-pdb
spec:
  maxUnavailable: "25%"
  selector:
    matchLabels:
      tier: frontend
---
# Database — critical, must keep most available
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: database-pdb
spec:
  minAvailable: 3
  selector:
    matchLabels:
      app: postgres
---
# Batch jobs — can be disrupted entirely
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: batch-pdb
spec:
  maxUnavailable: 100%
  selector:
    matchLabels:
      app: batch-processor
```

### 5. PDB with StatefulSet

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: kafka-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: kafka

# For StatefulSets, PDB ensures ordered disruption:
# - Pod kafka-0 must remain first, then kafka-1, etc.
# - This preserves quorum for distributed systems
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: zookeeper-pdb
spec:
  minAvailable: 3  # Keep ZK quorum of 3 out of 5
  selector:
    matchLabels:
      app: zookeeper
```

### 6. Checking PDB Status

```bash
# Check PDB status
kubectl get pdb web-pdb -o yaml

# Expected output:
# status:
#   conditions:
#   - observedGeneration: 1
#   currentHealthy: 3
#   desiredHealthy: 2
#   disruptionsAllowed: 1
#   expectedPods: 3

# List all PDBs
kubectl get pdb --all-namespaces

# Check if node drain will succeed (dry run)
kubectl drain node-1 --dry-run=server

# Force drain (ignore PDBs — CAUTION!)
kubectl drain node-1 --disable-eviction=true
```

### 7. Eviction API

```bash
# Manual eviction with PDB check
kubectl evict pod web-abc123

# Programmatic eviction via API
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"apiVersion": "policy/v1", "kind": "Eviction", "metadata": {"name": "web-abc123", "namespace": "default"}}' \
  http://localhost:8001/api/v1/namespaces/default/pods/web-abc123/eviction
```

### 8. PDB with Cluster Autoscaler

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-pdb
spec:
  minAvailable: "80%"  # Cluster Autoscaler won't scale down below 80%
  selector:
    matchLabels:
      app: critical
```

### 9. PDB Configuration Strategies

```yaml
# Strategy 1: Conservative — maxUnavailable: 1
# Best for: StatefulSets, databases, stateful workloads
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: conservative-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: stateful-app

# Strategy 2: Balanced — minAvailable: "50%"
# Best for: Stateless apps with moderate redundancy
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: balanced-pdb
spec:
  minAvailable: "50%"
  selector:
    matchLabels:
      app: stateless-app

# Strategy 3: Liberal — maxUnavailable: "100%"
# Best for: Batch jobs, async workers, non-critical
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: liberal-pdb
spec:
  maxUnavailable: "100%"
  selector:
    matchLabels:
      app: batch-worker
```

### 10. PDB with Pod Topology Spread Constraints

```yaml
# Combined PDB + Topology Spread to maximize availability
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 6
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: web
      containers:
      - name: web
        image: nginx
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: web
```

## Real-World Use Cases

### 1. Cluster Upgrades

```bash
# Rolling upgrade of node pools
# PDB ensures no more than N pods go down per deployment

# Drain nodes one at a time
for node in $(kubectl get nodes -l pool=workers -o name); do
  kubectl drain $node --ignore-daemonsets --delete-emptydir-data
  # PDB will block if disruption would exceed limits
  kubectl upgrade node $node
  kubectl uncordon $node
done
```

### 2. Spot Instance Interruption

```yaml
# For AWS/GCP spot/preemptible instances
# PDB ensures enough pods survive interruptions
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: spot-worker-pdb
spec:
  minAvailable: 3  # Keep at least 3 pods even during interruptions
  selector:
    matchLabels:
      app: worker
      instance-type: spot
```

### 3. Database Maintenance

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: postgres-pdb
spec:
  minAvailable: 2  # PostgreSQL quorum: 2/3 replicas
  selector:
    matchLabels:
      app: postgres

# During maintenance:
# - Can only drain 1 postgres pod at a time
# - Remaining 2 maintain read quorum (no writes)
# - When replacement is ready, can drain another
```

## PDB Selection Strategies

| Strategy | Example | Use Case |
|----------|---------|----------|
| `maxUnavailable: "25%"` | Can lose 25% of pods | Stateless web services |
| `minAvailable: 2` | Always keep 2 pods | Stateful services, databases |
| `minAvailable: "50%"` | Keep half the pods | General purpose |
| `maxUnavailable: 1` | Only lose 1 at a time | Conservative, critical apps |
| `maxUnavailable: "100%"` | All can be disrupted | Batch jobs, non-critical |

## Common Mistakes

### 1. Not Creating PDBs for Critical Workloads

```yaml
# ❌ BAD: No PDB — node drain takes all pods down simultaneously
# Result: Complete downtime during maintenance

# ✅ GOOD: PDB prevents total downtime
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: critical
```

### 2. PDB That Blocks All Disruptions

```yaml
# ❌ BAD: 5 replicas, minAvailable: 5
# Result: Blocked — can never disrupt any pod
# This makes cluster maintenance impossible!
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: bad-pdb
spec:
  minAvailable: 5
  selector:
    matchLabels:
      app: web
---
# ✅ GOOD: Allow some disruption
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: good-pdb
spec:
  minAvailable: 4
  selector:
    matchLabels:
      app: web
# With 5 replicas, allows 1 disruption at a time
```

### 3. Misaligned PDB and Replica Count

```yaml
# ❌ BAD: 2 replicas, minAvailable: 2
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: bad-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web
---
# Can never drain — always need 2 pods, but only 2 exist
# Node drain will fail until a pod replacement arrives

# ✅ GOOD: 3+ replicas or lower minAvailable
```

### 4. Not Using Percentage with Large Deployments

```yaml
# ❌ BAD: Hardcoded number doesn't scale with replicas
spec:
  maxUnavailable: 2
# If replicas grow from 10 to 100, still only allows 2

# ✅ GOOD: Percentage scales automatically
spec:
  maxUnavailable: "25%"
# Scales: 10→2, 100→25, etc.
```

### 5. PDB and Autoscaling Conflicts

```yaml
# ❌ BAD: PDB blocks Cluster Autoscaler from scaling down
spec:
  minAvailable: "100%"
# Autoscaler can never evict pods → can't downscale

# ✅ GOOD: Allow Headroom for Autoscaler
spec:
  minAvailable: "80%"
# Autoscaler can evict up to 20% of pods
```

## Best Practices

1. **Always create PDBs for production workloads** — Essential for safe maintenance

2. **Use percentage-based PDBs** — `minAvailable: "50%"` scales with replicas

3. **Don't set `minAvailable` equal to replicas** — Leaves no room for disruption

4. **Use `maxUnavailable: 1` for StatefulSets** — Preserves ordering and quorum

5. **Test PDB enforcement** — `kubectl drain --dry-run=server` validates

6. **Monitor PDB status** — Track `disruptionsAllowed` in monitoring

7. **Use PDBs with PDBs** — Different tiers get different budgets

8. **Combine with Topology Spread Constraints** — Spread pods across nodes for best resilience

9. **Configure Pod Disruption Budget for HPA** — Ensure scale-down respects PDB

10. **Document PDB strategy** — Clarify which apps have which disruption tolerance

## Performance Considerations

```text
PDB Impact on Operations:

Cluster Upgrade Speed:
├── No PDB: Upgrade all nodes at once (fast but risky)
├── Conservative PDB: 1 pod at a time (slow but safe)
└── Balanced PDB: 25% at a time (reasonable)

Autoscaling:
├── No PDB: Instant scale down
├── With PDB: Scale down limited by budget
└── Must balance: Aggressive scaling vs availability

Node Drain Duration:
├── No PDB: Seconds per node
├── With PDB: Depends on pod replacement speed
└── Each PDB must allow at least 1 pod eviction

```

## Summary

- PodDisruptionBudgets protect application availability during voluntary disruptions like node maintenance and cluster upgrades
- Use `maxUnavailable` to cap how many pods can be down, or `minAvailable` to enforce minimum running pods
- Percentage-based budgets scale automatically with replica count and are preferred for dynamic workloads
- PDBs can block operations entirely if misconfigured — always leave room for at least one disruption
- Combine PDBs with Topology Spread Constraints and Pod Anti-Affinity for maximum availability

## Cheat Sheet

```yaml
# Basic PDB — maxUnavailable
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: web
---
# Basic PDB — minAvailable (absolute)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: db-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: postgres
---
# Basic PDB — minAvailable (percentage)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: worker-pdb
spec:
  minAvailable: "50%"
  selector:
    matchLabels:
      app: worker
```

```text
PDB Key Points:
├── Protects against: Voluntary disruptions only
├── Does NOT protect: Node failures, hardware crashes
├── minAvailable: Minimum pods that must stay up
├── maxUnavailable: Max pods that can be down
├── Both: Accept absolute numbers or percentages
└── Selector: Must match pod labels (like a Service)

Commands:
├── kubectl get pdb
├── kubectl describe pdb <name>
├── kubectl drain <node> --dry-run=server
├── kubectl evict pod <name>
└── kubectl drain <node> --disable-eviction (force)

Common Patterns:
├── Critical apps: maxUnavailable: 1
├── Stateless apps: minAvailable: "50%"
├── Stateful workloads: maxUnavailable: 1
├── Batch jobs: maxUnavailable: "100%"
├── Databases: minAvailable: quorum size
└── Autoscaled: minAvailable: "80%"
```

---

## See Also
- [Deployments](02-Deployments.md)
- [Health Checks](06-Health-Checks.md)
- [HPA & Scaling](05-HPA-Scaling.md)
- [Interview Questions](08-Interview-Questions.md)
- [Pods & ReplicaSets](01-Pods-ReplicaSets.md)
- [Services & Ingress](03-Services-Ingress.md)
- [StatefulSets & DaemonSets](09-StatefulSets-DaemonSets.md)

## References & Learn More

- [K8s PodDisruptionBudget Docs](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)
- [K8s Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
- [K8s Drain](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)
- [K8s Cluster Autoscaler & PDB](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#how-does-cluster-autoscaler-work-with-poddisruptionbudget)
- [Managing Voluntary Disruptions](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)
