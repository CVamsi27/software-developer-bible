# Kubernetes Deployments

## Definition

A **Deployment** provides declarative updates for Pods and ReplicaSets. It manages the desired state of your application, enabling rolling updates, rollbacks, scaling, and self-healing. Deployments are the most common way to run stateless applications in Kubernetes.

Key concepts:
- **Deployment**: Manages ReplicaSets and Pods
- **Rolling Update**: Gradual replacement of Pods
- **Rollback**: Revert to previous Deployment revision
- **Strategy**: How updates are performed
- **Revision History**: Track of all Deployment changes

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Manual Pod management | Declarative desired state |
| Downtime during updates | Rolling updates |
| No rollback capability | Revision history |
| Manual scaling | `kubectl scale` |
| No self-healing | Automatic Pod replacement |
| No deployment history | Revision tracking |

## How It Works

### Deployment Architecture

```
+----------------------------------------------------------+
|                      Deployment                           |
|  name: myapp                                             |
|  replicas: 3                                             |
|  strategy: RollingUpdate                                 |
|  image: myapp:2.0                                        |
+----------------------------------------------------------+
                          |
                          v
+----------------------------------------------------------+
|                    ReplicaSet (new)                       |
|  name: myapp-abc123                                       |
|  replicas: 3                                             |
|  selector: app=myapp                                     |
+----------------------------------------------------------+
         |              |              |
         v              v              v
   +----------+  +----------+  +----------+
   |   Pod    |  |   Pod    |  |   Pod    |
   | myapp:2.0|  | myapp:2.0|  | myapp:2.0|
   +----------+  +----------+  +----------+

+----------------------------------------------------------+
|                    ReplicaSet (old)                       |
|  name: myapp-xyz789                                       |
|  replicas: 0                                             |
|  selector: app=myapp                                     |
+----------------------------------------------------------+
  (scaled to 0 during rolling update)
```

### Rolling Update Process

```
Step 1: Initial State
+--------+  +--------+  +--------+
| v1 Pod |  | v1 Pod |  | v1 Pod |
+--------+  +--------+  +--------+

Step 2: Create new Pod
+--------+  +--------+  +--------+  +--------+
| v1 Pod |  | v1 Pod |  | v1 Pod |  | v2 Pod |
+--------+  +--------+  +--------+  +--------+

Step 3: Terminate old Pod
+--------+  +--------+  +--------+
| v1 Pod |  | v1 Pod |  | v2 Pod |
+--------+  +--------+  +--------+

Step 4: Create another new Pod
+--------+  +--------+  +--------+  +--------+
| v1 Pod |  | v1 Pod |  | v2 Pod |  | v2 Pod |
+--------+  +--------+  +--------+  +--------+

Step 5: Terminate another old Pod
+--------+  +--------+  +--------+
| v1 Pod |  | v2 Pod |  | v2 Pod |
+--------+  +--------+  +--------+

Step 6: Complete
+--------+  +--------+  +--------+
| v2 Pod |  | v2 Pod |  | v2 Pod |
+--------+  +--------+  +--------+
```

## Code Examples

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
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

### Rolling Update Strategy

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max pods above desired count
      maxUnavailable: 0   # Min pods available during update
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0
```

### Recreate Strategy

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: Recreate  # Kill all old pods before creating new
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0
```

### Deployment with Probes and Lifecycle

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: myapp
          image: myapp:2.0.0

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
            periodSeconds: 15
            timeoutSeconds: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 10
            timeoutSeconds: 3

          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]

          resources:
            requests:
              memory: "256Mi"
              cpu: "500m"
            limits:
              memory: "512Mi"
              cpu: "1000m"

          env:
            - name: DB_HOST
              value: "db-service"
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password
```

### Managing Deployments

```bash
# Create deployment
kubectl apply -f deployment.yaml

# Check status
kubectl get deployments
kubectl rollout status deployment/myapp

# Scale
kubectl scale deployment/myapp --replicas=5

# Update image
kubectl set image deployment/myapp myapp=myapp:2.0.0

# Rollback
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2

# View history
kubectl rollout history deployment/myapp

# Pause/resume
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp
```

### Deployment with HPA

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0
          resources:
            requests:
              memory: "256Mi"
              cpu: "500m"
            limits:
              memory: "512Mi"
              cpu: "1000m"

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Real-World Use Cases

### 1. Zero-Downtime Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: web:2.0
          ports:
            - containerPort: 80

          readinessProbe:
            httpGet:
              path: /ready
              port: 80
            periodSeconds: 5

          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]
```

### 2. Canary Deployment

```yaml
# Stable version
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable
  template:
    metadata:
      labels:
        app: myapp
        track: stable
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0

---
# Canary version
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0
```

### 3. Blue-Green Deployment

```yaml
# Blue (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0

---
# Green (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0

---
# Service (switch selector between blue/green)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to green for new version
  ports:
    - port: 80
      targetPort: 8080
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| No readiness probe | Add readiness probe for zero-downtime |
| maxUnavailable=1 | Set maxUnavailable=0 for HA |
| No resource limits | Always set requests and limits |
| No liveness probe | Add liveness for self-healing |
| Using `latest` tag | Pin specific image versions |
| No PodDisruptionBudget | Add PDB for critical workloads |
| No revision history limit | Set revisionHistoryLimit |

## Best Practices

```yaml
# GOOD: Production Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  revisionHistoryLimit: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      terminationGracePeriodSeconds: 60
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
            periodSeconds: 15
            timeoutSeconds: 3
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 10
            timeoutSeconds: 3

          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]

          resources:
            requests:
              memory: "256Mi"
              cpu: "500m"
            limits:
              memory: "512Mi"
              cpu: "1000m"

          env:
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: db-host

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - myapp
                topologyKey: kubernetes.io/hostname
```

1. **Use RollingUpdate with maxUnavailable=0** — zero-downtime deployments
2. **Add all three probe types** — startup, liveness, readiness
3. **Set resource requests and limits** — enable scheduling and prevent OOM
4. **Use pod anti-affinity** — distribute across nodes
5. **Set revisionHistoryLimit** — manage revision history
6. **Use preStop hooks** — allow graceful shutdown
7. **Pin image versions** — never use `latest`
8. **Add PodDisruptionBudget** — protect during node maintenance
9. **Use namespaces** — isolate environments
10. **Monitor rollout status** — `kubectl rollout status`

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| maxSurge | Resource overhead | Set appropriate value |
| maxUnavailable | Availability | Set to 0 for critical apps |
| Startup probe timeout | Deployment speed | Tune failureThreshold |
| PreStop sleep time | Grace period | Balance with terminationGracePeriod |
| Anti-affinity rules | Scheduling speed | Use preferredDuringScheduling |

```bash
# Monitor deployment
kubectl rollout status deployment/myapp
kubectl get events -w

# Check resource usage
kubectl top pods -l app=myapp

# View rollout history
kubectl rollout history deployment/myapp
```

## Interview Questions

### Beginner (5-10)

1. **What is a Deployment?**
   Manages ReplicaSets and Pods, providing rolling updates and rollbacks.

2. **What is the difference between a Deployment and a ReplicaSet?**
   Deployment adds deployment strategy, rollbacks, and history on top of ReplicaSet.

3. **What is a rolling update?**
   Gradually replaces old Pods with new ones without downtime.

4. **How do you rollback a Deployment?**
   `kubectl rollout undo deployment/myapp`

5. **What is maxSurge?**
   Maximum number of Pods above desired count during update.

6. **What is maxUnavailable?**
   Minimum number of Pods unavailable during update.

7. **How do you scale a Deployment?**
   `kubectl scale deployment/myapp --replicas=5`

8. **How do you update the image?**
   `kubectl set image deployment/myapp myapp=myapp:2.0.0`

9. **What is the default update strategy?**
   RollingUpdate.

10. **How do you view Deployment history?**
    `kubectl rollout history deployment/myapp`

### Intermediate (5-10)

11. **What is the difference between RollingUpdate and Recreate?**
    RollingUpdate gradually replaces Pods. Recreate terminates all old Pods before creating new ones.

12. **How does Kubernetes know when a new Pod is ready?**
    Readiness probe must return success. Traffic is routed only to ready Pods.

13. **What is a revision in a Deployment?**
    A snapshot of the Deployment's Pod template. Each update creates a new revision.

14. **How do you pause a Deployment?**
    `kubectl rollout pause deployment/myapp` — allows multiple changes without creating revisions.

15. **What happens if a Pod fails during a rolling update?**
    The Deployment controller retries based on the progressDeadlineSeconds.

16. **How do you set a Deployment to only use specific nodes?**
    Use nodeSelector or node affinity in the Pod template.

17. **What is the minimum number of Pods during a rolling update?**
    Desired replicas minus maxUnavailable.

18. **How do you check if a Deployment is healthy?**
    `kubectl get deployment myapp` — check READY and AVAILABLE columns.

19. **What is a progressive delivery?**
    Advanced deployment strategies like canary, blue-green, or feature flags.

20. **How do you handle environment-specific configurations?**
    Use ConfigMaps and Secrets, or separate YAML files per environment.

### Senior (10-15)

21. **How do you implement zero-downtime deployments?**
    Use RollingUpdate with maxUnavailable=0, readiness probes, and preStop hooks.

22. **What is the difference between maxSurge and maxUnavailable?**
    maxSurge controls how many extra Pods can exist. maxUnavailable controls how many can be missing.

23. **How do you handle database schema changes in a Deployment?**
    Run migrations as a separate Job before updating the Deployment.

24. **Explain Deployment progressDeadlineSeconds.**
    Maximum time for a Deployment to progress before it's considered failed.

25. **How do you implement canary deployments in Kubernetes?**
    Deploy a small number of new Pods with a different label, use Service selector to route traffic.

### FAANG-style (5-10)

26. **Design a deployment pipeline for 100+ microservices.**
    Use Argo CD or Flux for GitOps, automated rollbacks, canary analysis, and progressive delivery.

27. **How would you handle a failed deployment at 3 AM?**
    Implement automatic rollback on failure, alerting, and runbook automation.

28. **Design a multi-region deployment strategy.**
    Use regional Deployments with PodDisruptionBudgets, cross-region service mesh, and traffic shifting.

29. **How would you optimize deployment speed?**
    Use image pre-pulling, init containers, and parallel rollouts across namespaces.

30. **Describe a deployment strategy for a stateful application.**
    Use StatefulSets with ordered deployment, persistent volumes, and readiness gates.

### Follow-ups (5-10)

31. **What is the difference between a Deployment and a StatefulSet?**
    Deployment: stateless, unordered. StatefulSet: stateful, ordered, stable network/storage.

32. **How do you handle secret rotation in a Deployment?**
    Update the Secret, then rolling restart the Deployment.

33. **What is a canary analysis?**
    Monitoring metrics after a canary deployment to decide to promote or rollback.

34. **How do you handle multi-container deployments?**
    Define multiple containers in the Pod template with shared volumes/network.

35. **What is the maximum number of revisions a Deployment keeps?**
    Default is 10, configurable via revisionHistoryLimit.

## Summary

Deployments are the standard way to manage stateless applications in Kubernetes. They provide rolling updates, rollbacks, and self-healing. Proper probe configuration, resource limits, and update strategies are essential for production reliability.

## Cheat Sheet

```bash
# Deployment
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl describe deployment myapp

# Updates
kubectl set image deployment/myapp myapp=myapp:2.0.0
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2

# Scale
kubectl scale deployment/myapp --replicas=5
kubectl autoscale deployment/myapp --min=3 --max=20 --cpu-percent=70

# Pause/Resume
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp

# Restart (rolling)
kubectl rollout restart deployment/myapp
```

---

## References & Learn More
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
