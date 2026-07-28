---
section: Kubernetes
category: DevOps
tags: [concept]
---

# StatefulSets & DaemonSets

## Definition

**StatefulSets** manage stateful applications with unique network identities, stable persistent storage, and ordered deployment/scaling (e.g., databases, message queues). **DaemonSets** ensure all (or select) nodes run a copy of a pod — used for cluster-wide services like log collectors, monitoring agents, and network plugins.

## Why Do We Need It?

1. **StatefulSets**: Stable Pod identities (DNS), ordered graceful deployment, persistent storage per Pod, required for databases (PostgreSQL, Cassandra, Kafka)
2. **DaemonSets**: Node-level agents (Fluentd for logs, Prometheus Node Exporter, Calico/Cilium networking, kube-proxy)

## Code Examples

### StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      storageClassName: standard
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

## Key Differences

| Feature | StatefulSet | DaemonSet | Deployment |
|---------|:-----------:|:---------:|:----------:|
| Pod identity | Stable ordinal | Per-node | Random |
| Storage | Persistent per Pod | HostPath/emptyDir | Shared PVC |
| Scaling | Ordered | By node count | Arbitrary |
| Update strategy | Rolling/Custom | RollingOnDelete | Rolling/Rollback |

---

### See Also

- [ConfigMaps & Secrets](04-ConfigMaps-Secrets.md)
- [Deployments](02-Deployments.md)
- [HPA & Scaling](05-HPA-Scaling.md)
- [Interview Questions](08-Interview-Questions.md)
- [Pods & ReplicaSets](01-Pods-ReplicaSets.md)

## References & Learn More

- [Kubernetes StatefulSet Docs](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Kubernetes DaemonSet Docs](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
