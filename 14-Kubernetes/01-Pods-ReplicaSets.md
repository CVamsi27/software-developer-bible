# Kubernetes Pods & ReplicaSets

## Definition

A **Pod** is the smallest deployable unit in Kubernetes—a group of one or more containers that share storage, network, and a specification for how to run. A **ReplicaSet** ensures a specified number of Pod replicas are running at any given time. Pods are ephemeral; ReplicaSets maintain desired state.

Key concepts:

- **Pod**: Co-located, co-scheduled containers sharing network/storage
- **ReplicaSet**: Maintains stable set of replica Pods
- **Labels**: Key-value pairs attached to Pods for selection
- **Selectors**: Query mechanism to filter Pods by labels
- **Namespace**: Virtual cluster partitioning within a physical cluster

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Single-container limitation | Pods run multiple containers |
| Manual scaling | ReplicaSet maintains replica count |
| Self-healing | Failed Pods are automatically replaced |
| Service discovery | Pods get unique IP and DNS |
| Resource management | Pod-level resource requests/limits |
| Deployment strategy | ReplicaSet enables rolling updates |

## How It Works

### Pod Architecture

```text
+----------------------------------------------------------+

|                        Pod                                 |
|  +-------------------+  +-------------------+            |
|  |    Container 1    |  |    Container 2    |            |
|  |   (app server)    |  |   (sidecar)       |            |
|  |   Port: 8080      |  |   Port: 9090      |            |
|  +-------------------+  +-------------------+            |
|  |    Shared Network Namespace                             |
|  |    IP: 10.244.1.5                                      |
|  |    localhost: shared                                    |
|  +--------------------------------------------------------|
|  |    Shared Storage Volumes                               |
|  |    /data (emptyDir)                                    |
|  |    /config (configMap)                                 |
|  +--------------------------------------------------------|

+----------------------------------------------------------+

         |                    |

         v                    v
+------------------+  +------------------+

|   Node (Worker)  |  |   Node (Worker)  |
|   10.0.0.1       |  |   10.0.0.2       |

+------------------+  +------------------+

```

### ReplicaSet Architecture

```text
                    +------------------+

                    |   ReplicaSet     |
                    |  replicas: 3     |
                    |  selector:       |
                    |   app: web       |

                    +--------+---------+

                             |

              +--------------+--------------+

              |              |              |

              v              v              v
        +----------+  +----------+  +----------+

        |   Pod    |  |   Pod    |  |   Pod    |
        | 10.244.  |  | 10.244.  |  | 10.244.  |
        |  1.5     |  |  1.6     |  |  1.7     |

        +----------+  +----------+  +----------+
        Labels:        Labels:        Labels:
        app: web       app: web       app: web
        env: prod      env: prod      env: prod

If a Pod fails, ReplicaSet creates a new one to maintain count.

```

## Code Examples

### Basic Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
    environment: production
spec:
  containers:

    - name: myapp
      image: myapp:1.0.0
      ports:

        - containerPort: 8080
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "256Mi"
          cpu: "500m"

```

### Multi-Container Pod (Sidecar Pattern)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-with-sidecar
spec:
  containers:

    - name: app
      image: myapp:1.0.0
      ports:

        - containerPort: 8080

    - name: log-shipper
      image: fluentd:latest
      volumeMounts:

        - name: app-logs
          mountPath: /var/log/app

    - name: metrics
      image: prom/prometheus
      ports:

        - containerPort: 9090

  volumes:

    - name: app-logs
      emptyDir: {}

```

### ReplicaSet

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-rs
  labels:
    app: myapp
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        environment: production
    spec:
      containers:

        - name: myapp
          image: myapp:1.0.0
          ports:

            - containerPort: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"

```

### Pod Lifecycle

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-lifecycle
spec:
  initContainers:

    - name: init-db
      image: busybox
      command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done']

  containers:

    - name: myapp
      image: myapp:1.0.0

      lifecycle:
        postStart:
          exec:
            command: ["/bin/sh", "-c", "echo started > /tmp/started"]
        preStop:
          exec:
            command: ["/bin/sh", "-c", "nginx -s quit && sleep 5"]

  terminationGracePeriodSeconds: 30

```

### Pod with Probes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-probes
spec:
  containers:

    - name: myapp
      image: myapp:1.0.0

      startupProbe:
        httpGet:
          path: /health
          port: 8080
        failureThreshold: 30
        periodSeconds: 10

      livenessProbe:
        httpGet:
          path: /health
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 15
        timeoutSeconds: 3
        failureThreshold: 3

      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 10
        timeoutSeconds: 3

```

### Managing Pods and ReplicaSets

```bash
# Create resources
kubectl apply -f pod.yaml
kubectl apply -f replicaset.yaml

# List pods
kubectl get pods
kubectl get pods -l app=myapp
kubectl get pods --all-namespaces

# Describe pod
kubectl describe pod myapp-pod

# View logs
kubectl logs myapp-pod
kubectl logs myapp-pod -c sidecar  # specific container
kubectl logs -f myapp-pod  # follow

# Execute in pod
kubectl exec -it myapp-pod -- sh

# Delete
kubectl delete pod myapp-pod
kubectl delete replicaset myapp-rs

```

## Real-World Use Cases

### 1. Web Application Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
  labels:
    app: web
    tier: frontend
spec:
  containers:

    - name: nginx
      image: nginx:1.25-alpine
      ports:

        - containerPort: 80
      volumeMounts:

        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf

  volumes:

    - name: nginx-config
      configMap:
        name: nginx-config

```

### 2. Database Pod with Persistent Storage

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: postgres-rs
spec:
  replicas: 1
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
          image: postgres:15-alpine
          env:

            - name: POSTGRES_DB
              value: mydb

            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password
          volumeMounts:

            - name: pg-data
              mountPath: /var/lib/postgresql/data

      volumes:

        - name: pg-data
          persistentVolumeClaim:
            claimName: pg-pvc

```

### 3. Batch Job Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-processor
  labels:
    app: batch
    job: data-process
spec:
  restartPolicy: Never
  containers:

    - name: processor
      image: myapp/data-processor:1.0
      command: ["python", "process.py"]
      env:

        - name: INPUT_PATH
          value: "s3://bucket/input/"

        - name: OUTPUT_PATH
          value: "s3://bucket/output/"

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using bare Pods | Use ReplicaSets or Deployments |
| Hardcoding Pod labels | Use consistent label strategy |
| No resource requests | Always set requests and limits |
| Missing health checks | Add startup/liveness/readiness probes |
| No init containers | Use init for dependency initialization |
| Running as root | Set securityContext |
| No pod disruption budgets | Set PDB for critical workloads |

## Best Practices

```yaml
# GOOD: Production-ready Pod
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-rs
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000

      initContainers:

        - name: init-db
          image: busybox:1.36
          command: ['sh', '-c', 'until nslookup db; do sleep 2; done']

      containers:

        - name: myapp
          image: myapp:1.0.0
          ports:

            - containerPort: 8080

          resources:
            requests:
              memory: "256Mi"
              cpu: "500m"
            limits:
              memory: "512Mi"
              cpu: "1000m"

          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10

          env:

            - name: DB_HOST
              value: "db"

            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password

      terminationGracePeriodSeconds: 60

```

1. **Never use bare Pods** — always use ReplicaSets or Deployments

2. **Set resource requests and limits** — enable scheduling and prevent OOM

3. **Add health checks** — enable self-healing

4. **Use labels consistently** — enable service discovery and monitoring

5. **Run as non-root** — security best practice

6. **Use init containers** — for dependency initialization

7. **Set terminationGracePeriodSeconds** — allow graceful shutdown

8. **Use PodDisruptionBudgets** — protect during voluntary disruptions

9. **Limit pod size** — smaller pods enable better scheduling
10. **Use namespaces** — isolate workloads

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Pod size | Scheduling speed | Keep pods small |
| Resource requests | Scheduling accuracy | Set realistic requests |
| Init containers | Startup time | Minimize init logic |
| Container count | Resource overhead | Use sidecars sparingly |
| Node affinity | Distribution | Use pod anti-affinity |

```bash
# View pod resource usage
kubectl top pods
kubectl top pods --sort-by=memory

# Check scheduling
kubectl describe pod myapp | grep -A 5 "Events"

# View pod density on nodes
kubectl get pods --all-namespaces -o wide | awk '{print $8}' | sort | uniq -c

```

## Interview Questions

### Beginner (5-10)

1. **What is a Pod?**
   The smallest deployable unit in Kubernetes. One or more containers sharing network/storage.

2. **What is a ReplicaSet?**
   Ensures a specified number of Pod replicas are running at any time.

3. **What are labels in Kubernetes?**
   Key-value pairs attached to resources for identification and selection.

4. **How do you list all Pods?**
   `kubectl get pods --all-namespaces`

5. **What is the difference between a Pod and a container?**
   A Pod can contain multiple containers. A container is a single runtime instance.

6. **How do you delete a Pod?**
   `kubectl delete pod <name>` or `kubectl delete -f pod.yaml`

7. **What happens when a Pod dies?**
   If managed by a ReplicaSet, a new Pod is created to replace it.

8. **How do you view Pod logs?**
   `kubectl logs <pod-name>`

9. **What is a Namespace?**
   A virtual cluster partition for resource isolation.

10. **What is the difference between kubectl apply and kubectl create?**
    `create` creates a new resource; `apply` creates or updates idempotently.

### Intermediate (5-10)

11. **What are the Pod states?**
    Pending, Running, Succeeded, Failed, Unknown.

12. **What is a multi-container Pod?**
    A Pod with multiple containers sharing network/storage, used for sidecars, ambassadors, or adapters.

13. **What are init containers?**
    Containers that run before main containers, used for initialization tasks.

14. **How does Kubernetes schedule Pods?**
    The scheduler matches Pod resource requests to node available resources.

15. **What is Pod affinity/anti-affinity?**
    Rules that constrain which nodes Pods can be scheduled on based on other Pods' labels.

16. **What are tolerations and taints?**
    Taints repel Pods from nodes; tolerations allow Pods to be scheduled on tainted nodes.

17. **How do you debug a pending Pod?**
    `kubectl describe pod <name>` to see events and scheduling constraints.

18. **What is a Pod disruption budget?**
    Limits voluntary disruptions (node drain, upgrades) to protect availability.

19. **What are resource requests vs limits?**
    Requests: minimum resources guaranteed. Limits: maximum resources allowed.

20. **How do you exec into a Pod?**
    `kubectl exec -it <pod> -- sh` or `kubectl exec -it <pod> -c <container> -- sh`

### Senior (10-15)

21. **Explain the Pod lifecycle hooks.**
    `postStart`: runs after container starts. `preStop`: runs before container stops. Used for initialization and graceful shutdown.

22. **How does Kubernetes handle Pod networking?**
    Each Pod gets a unique IP. Containers in a Pod share the network namespace. Pods communicate via IP or DNS.

23. **What is the difference between a ReplicaSet and a Deployment?**
    ReplicaSet maintains replicas. Deployment adds rolling updates, rollbacks, and history.

24. **How do you implement zero-downtime deployments?**
    Use Deployments with rolling updates, readiness probes, and PodDisruptionBudgets.

25. **Explain Pod topology spread constraints.**
    Distribute Pods across zones/nodes based on labels to ensure high availability.

### FAANG-style (5-10)

26. **Design a Pod scheduling strategy for a latency-sensitive application.**
    Use node affinity for specific hardware, Pod anti-affinity for HA, topology spread constraints, and resource overcommitment controls.

27. **How would you handle a Pod that keeps crashing (CrashLoopBackOff)?**
    Check logs, examine events, verify resource limits, check health probe configuration, review init containers.

28. **Design a sidecar pattern for a microservice mesh.**
    Envoy proxy sidecar for traffic management, Fluentd for logging, Prometheus exporter for metrics.

29. **How would you optimize Pod density on a node?**
    Right-size resource requests, use Pod overhead calculations, consider vertical scaling.

30. **Describe a strategy for managing Pod security at scale.**
    Pod Security Standards (restricted/baseline/privileged), OPA/Gatekeeper policies, image scanning, runtime security.

### Follow-ups (5-10)

31. **What is the difference between emptyDir and hostPath?**
    `emptyDir`: empty at Pod start, shared between containers. `hostPath`: mounts host filesystem.

32. **How do you handle DNS resolution in Pods?**
    Kubernetes provides DNS via CoreDNS. Pods use `<service-name>.<namespace>.svc.cluster.local`.

33. **What is the maximum number of Pods per node?**
    Default is 110, configurable via kubelet `--max-pods` flag.

34. **How do you handle Pod-to-Pod communication across namespaces?**
    Use fully qualified domain name: `<service>.<namespace>.svc.cluster.local`.

35. **What is the difference between Pod and Node affinity?**
    Pod affinity: schedule based on other Pods. Node affinity: schedule based on node properties.

## Summary

Pods are Kubernetes' atomic units. ReplicaSets ensure desired replica count. Mastering Pod lifecycle, multi-container patterns, scheduling constraints, and resource management is essential for Kubernetes operations.

## Cheat Sheet

```bash
# Pods
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs <name> -f
kubectl exec -it <name> -- sh
kubectl delete pod <name>

# ReplicaSets
kubectl get rs
kubectl scale rs/myapp-rs --replicas=5
kubectl describe rs <name>

# Labels
kubectl get pods -l app=myapp
kubectl label pod <name> env=prod

# Debugging
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top pods
kubectl top nodes

# Apply
kubectl apply -f pod.yaml
kubectl diff -f pod.yaml

```

---

## References & Learn More

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
