# Kubernetes Interview Questions

## 30 Most Asked Kubernetes Interview Questions with Detailed Answers

---

### Question 1: What is Kubernetes and why is it used?

**Answer:**

Kubernetes (K8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Key Benefits:**
- **Self-healing**: Restarts failed containers, replaces and reschedules containers
- **Horizontal scaling**: Scale up/down automatically based on metrics
- **Service discovery**: DNS-based service discovery and load balancing
- **Automated rollouts**: Rolling updates with zero downtime
- **Storage orchestration**: Mount storage systems automatically
- **Secret management**: Manage sensitive configuration

---

### Question 2: What is a Pod in Kubernetes?

**Answer:**

A Pod is the smallest deployable unit in Kubernetes. It represents a single instance of a running process and can contain one or more containers that share:
- Network namespace (same IP address)
- Storage volumes
- Process namespace

**When to use multi-container Pods:**
- Sidecar pattern (log shipping, proxies)
- Ambassador pattern (service proxies)
- Adapter pattern (output formatting)

---

### Question 3: Explain the difference between a Deployment and a StatefulSet.

**Answer:**

| Aspect | Deployment | StatefulSet |
|---|---|---|
| Use case | Stateless apps | Stateful apps |
| Pod naming | Random | Ordered (pod-0, pod-1) |
| Scaling | Unordered | Ordered |
| Network | Any order | Stable DNS |
| Storage | Shared | Per-Pod persistent |
| Updates | Rolling | Ordered |

---

### Question 4: What are Kubernetes Services and their types?

**Answer:**

Services provide stable networking for Pods.

| Type | Description | Use Case |
|---|---|---|
| ClusterIP | Internal only | Default, internal services |
| NodePort | Expose on node IP | Development, testing |
| LoadBalancer | Cloud LB | Production external access |
| ExternalName | CNAME alias | External service reference |

---

### Question 5: How does Kubernetes handle service discovery?

**Answer:**

Kubernetes uses DNS for service discovery:

```text
Service Name: myservice
Namespace: production
FQDN: myservice.production.svc.cluster.local
```

**Methods:**
1. **DNS**: CoreDNS resolves service names to Cluster IPs
2. **Environment variables**: Injected into Pods at creation
3. **Headless Services**: Return Pod IPs directly

---

### Question 6: What is the difference between a ConfigMap and a Secret?

**Answer:**

| Aspect | ConfigMap | Secret |
|---|---|---|
| Data type | Non-sensitive | Sensitive |
| Encoding | Plain text | Base64 |
| Security | No encryption | Encryption at rest |
| Use case | App config | Passwords, tokens |

---

### Question 7: Explain HPA (Horizontal Pod Autoscaler).

**Answer:**

HPA automatically scales Pod replicas based on metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**Metrics used:**
- CPU utilization
- Memory utilization
- Custom metrics (requests/second)
- External metrics (queue length)

---

### Question 8: What are liveness and readiness probes?

**Answer:**

| Probe | Purpose | On Failure |
|---|---|---|
| Liveness | Is container alive? | Restart container |
| Readiness | Can container receive traffic? | Remove from Service |
| Startup | Is initialization complete? | Delay other probes |

**Probe Handlers:**
- `exec`: Run command
- `httpGet`: HTTP request
- `tcpSocket`: TCP connection
- `gRPC`: gRPC health check

---

### Question 9: How do you manage secrets in Kubernetes?

**Answer:**

```bash
# Create secret
kubectl create secret generic db-creds \
  --from-literal=password=secret123

# Use in Pod
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-creds
        key: password
```

**Best Practices:**
- Use external secret stores (Vault)
- Enable encryption at rest
- Use RBAC to restrict access
- Rotate secrets regularly

---

### Question 10: What is an Ingress in Kubernetes?

**Answer:**

Ingress manages external HTTP/HTTPS access to Services:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
spec:
  tls:
    - hosts:
        - myapp.example.com
      secretName: tls-secret
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /api
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

**Features:**
- TLS termination
- Host-based routing
- Path-based routing
- Rate limiting

---

### Question 11: What is the difference between `kubectl apply` and `kubectl create`?

**Answer:**

| Command | Behavior |
|---|---|
| `create` | Creates a new resource; fails if exists |
| `apply` | Creates or updates idempotently |

```bash
# Creates new resource
kubectl create -f pod.yaml

# Creates or updates
kubectl apply -f pod.yaml
```

---

### Question 12: Explain the Kubernetes control plane components.

**Answer:**

```text
+----------------------------------------------------------+
|                    Control Plane                           |
|  +----------------+  +----------------+  +----------+    |
|  |   API Server   |  |    Scheduler   |  |  etcd    |    |
|  |   (kube-api)   |  |                |  |          |    |
|  +----------------+  +----------------+  +----------+    |
|  +----------------+  +----------------+                  |
|  |  Controller    |  |   Cloud        |                  |
|  |  Manager       |  |   Controller   |                  |
|  +----------------+  +----------------+                  |
+----------------------------------------------------------+
```

| Component | Responsibility |
|---|---|
| API Server | RESTful API, authentication, authorization |
| etcd | Distributed key-value store for cluster state |
| Scheduler | Assigns Pods to nodes |
| Controller Manager | Maintains desired state |
| Cloud Controller Manager | Cloud provider integration |

---

### Question 13: What are Persistent Volumes and PVCs?

**Answer:**

**PersistentVolume (PV):** Cluster-level storage resource.

**PersistentVolumeClaim (PVC):** Request for storage by a Pod.

```yaml
# PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

# Use in Pod
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: my-pvc
```

---

### Question 14: How do you perform rolling updates in Kubernetes?

**Answer:**

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**Commands:**
```bash
# Update image
kubectl set image deployment/myapp myapp=myapp:2.0

# Monitor rollout
kubectl rollout status deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
```

---

### Question 15: What is a DaemonSet?

**Answer:**

A DaemonSet ensures a Pod runs on all (or specific) nodes.

**Use Cases:**
- Log collectors (Fluentd, Filebeat)
- Monitoring agents (Prometheus Node Exporter)
- Network plugins (Calico, Weave)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      app: log-collector
  template:
    spec:
      containers:
        - name: fluentd
          image: fluentd:latest
```

---

### Question 16: What is the difference between a Job and a CronJob?

**Answer:**

| Aspect | Job | CronJob |
|---|---|---|
| Execution | One-time | Scheduled |
| Restart | Optional | Based on schedule |
| Use case | Batch processing | Recurring tasks |

```yaml
# CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: backup:latest
          restartPolicy: OnFailure
```

---

### Question 17: How does Kubernetes handle networking?

**Answer:**

**Key Principles:**
1. Every Pod gets a unique IP
2. Pods can communicate without NAT
3. Agents on a node can communicate with all Pods

**Network Plugins (CNI):**
- Calico: Network policy
- Flannel: Simple overlay
- Cilium: eBPF-based networking

---

### Question 18: What is a Namespace in Kubernetes?

**Answer:**

Namespaces provide virtual cluster partitioning within a physical cluster.

```bash
# Create namespace
kubectl create namespace production

# Set context
kubectl config set-context --current --namespace=production

# List resources in namespace
kubectl get pods -n production
```

**Use Cases:**
- Environment isolation (dev, staging, prod)
- Resource quotas per team
- RBAC boundaries

---

### Question 19: What are Taints and Tolerations?

**Answer:**

**Taints** repel Pods from nodes.
**Tolerations** allow Pods to be scheduled on tainted nodes.

```bash
# Add taint to node
kubectl taint nodes node1 key=value:NoSchedule

# Toleration in Pod
tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
```

---

### Question 20: How do you troubleshoot a CrashLoopBackOff?

**Answer:**

```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
kubectl logs --previous <pod-name>

# Common causes:
# 1. Application crash
# 2. Missing environment variables
# 3. Failed health checks
# 4. Insufficient resources
# 5. Incorrect command/args
```

---

### Question 21: What is the difference between `docker-compose` and Kubernetes?

**Answer:**

| Aspect | Docker Compose | Kubernetes |
|---|---|---|
| Scale | Single host | Multi-host |
| Complexity | Simple | Complex |
| Self-healing | Limited | Full |
| Auto-scaling | No | Yes |
| Use case | Development | Production |

---

### Question 22: What is Helm and why use it?

**Answer:**

Helm is the package manager for Kubernetes.

**Benefits:**
- Packages multiple manifests into charts
- Manages releases and rollbacks
- Configurable via values files
- Version control for deployments

```bash
# Install chart
helm install myrelease ./mychart -f values.yaml

# Upgrade
helm upgrade myrelease ./mychart -f new-values.yaml

# Rollback
helm rollback myrelease 1
```

---

### Question 23: How do you implement network policies?

**Answer:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api
      ports:
        - port: 8080
```

---

### Question 24: What is RBAC in Kubernetes?

**Answer:**

Role-Based Access Control controls who can do what.

```yaml
# Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]

# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader
subjects:
  - kind: User
    name: jane
roleRef:
  kind: Role
  name: pod-reader
```

---

### Question 25: How do you handle multi-cluster management?

**Answer:**

**Tools:**
- **KubeFed**: Kubernetes-native federation
- **Rancher**: Multi-cluster management UI
- **Anthos**: Google's hybrid/multi-cloud platform
- **Azure Arc**: Azure's hybrid platform

**Strategies:**
- GitOps with Argo CD
- Service mesh (Istio, Linkerd)
- Centralized monitoring

---

### Question 26: What are init containers?

**Answer:**

Init containers run before main containers and must complete successfully.

```yaml
spec:
  initContainers:
    - name: init-db
      image: busybox
      command: ['sh', '-c', 'until nslookup db; do sleep 2; done']
  containers:
    - name: app
      image: myapp:1.0
```

**Use Cases:**
- Wait for dependencies
- Database migrations
- Configuration setup

---

### Question 27: How do you monitor Kubernetes?

**Answer:**

**Components:**
- **Metrics Server**: Basic CPU/memory metrics
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Jaeger**: Distributed tracing
- **ELK Stack**: Log aggregation

```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# View events
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

### Question 28: What is a Pod Disruption Budget?

**Answer:**

PDB limits voluntary disruptions during node maintenance.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

---

### Question 29: How do you implement GitOps with Kubernetes?

**Answer:**

**Tools:**
- **Argo CD**: GitOps continuous delivery
- **Flux**: GitOps toolkit

**Workflow:**
1. Store manifests in Git
2. Argo CD watches repository
3. Automatically syncs changes
4. Provides rollback via Git

---

### Question 30: What are the best practices for Kubernetes security?

**Answer:**

1. **RBAC**: Restrict access with roles
2. **Network Policies**: Limit pod-to-pod communication
3. **Pod Security Standards**: Run as non-root
4. **Image scanning**: Use Trivy/Clair
5. **Secrets management**: External secret stores
6. **Audit logging**: Monitor API access
7. **Resource quotas**: Prevent resource exhaustion
8. **Regular updates**: Keep K8s and images updated

---

## Summary

Kubernetes interview questions cover:
- Core concepts (Pods, Services, Deployments)
- Networking (Services, Ingress, Network Policies)
- Storage (PVs, PVCs, StorageClasses)
- Security (RBAC, Secrets, Pod Security)
- Operations (Monitoring, Troubleshooting, GitOps)

Focus on understanding the **why** behind each concept.

## Cheat Sheet

```bash
# Pods
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs <name> -f
kubectl exec -it <name> -- sh

# Deployments
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp
kubectl scale deployment/myapp --replicas=5

# Services
kubectl get svc
kubectl describe svc myapp
kubectl get endpoints myapp

# Debugging
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top pods
kubectl top nodes
```

---

## References & Learn More
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
