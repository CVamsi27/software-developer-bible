[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

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

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Docker](../13-Docker/)
- [Observability](../22-Observability/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
