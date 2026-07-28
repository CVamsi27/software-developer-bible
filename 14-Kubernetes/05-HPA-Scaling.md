# Kubernetes HPA & Scaling

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

umber of Pod replicas based on observed metrics (CPU, memory, custom). **Vertical Pod Autoscaler (VPA)** adjusts resource requests/limits. Together, they enable dynamic capacity management.

Key concepts:

- **HPA**: Scales Pod count horizontally
- **VPA**: Adjusts Pod resource requests vertically
- **Metrics**: CPU, memory, custom metrics, external metrics
- **Scaling policy**: Controls scale-up/down speed
- **Cluster Autoscaler**: Scales node count

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Static replica count | HPA scales based on load |
| Over-provisioning | VPA right-sizes resources |
| Traffic spikes | Auto-scaling handles bursts |
| Cost optimization | Scale down during low traffic |
| Manual intervention | Automated scaling |
| Resource waste | Dynamic resource allocation |

## How It Works

### HPA Architecture

```text
                    +------------------+

                    |  Metrics Server  |
                    |  (CPU, Memory)   |

                    +--------+---------+

                             |

                             v
                    +------------------+

                    |       HPA        |
                    | Controller       |

                    +--------+---------+

                             |

              +--------------+--------------+

              |              |              |

              v              v              v
        +----------+  +----------+  +----------+

        |   Pod    |  |   Pod    |  |   Pod    |
        | (target) |  | (target) |  | (target) |

        +----------+  +----------+  +----------+

If CPU > 70%:  Scale UP   (add Pods)
If CPU < 30%:  Scale DOWN (remove Pods)

```

### Scaling Flow

```text
+----------------------------------------------------------+

|                    Scaling Decision                        |
|                                                           |
|  1. Collect metrics every 15s (default)                   |
|  2. Calculate desired replicas:                           |
|     desiredReplicas = ceil(                               |
|       currentReplicas * (currentMetric / targetMetric)    |
|     )                                                    |
|  3. Apply scaling policy (min/max, surge/down)            |
|  4. Update Deployment replica count                       |

+----------------------------------------------------------+

Example:
  Current: 3 replicas, 80% CPU
  Target: 50% CPU
  Desired: ceil(3 * 80/50) = ceil(4.8) = 5 replicas

```

## Code Examples

### Basic HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
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

### HPA with Memory

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 20
  metrics:

    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

```

### HPA with Custom Metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 50
  metrics:

    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"

```

### HPA with Scaling Policy

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 20
  metrics:

    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:

        - type: Pods
          value: 4
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:

        - type: Percent
          value: 10
          periodSeconds: 60

```

### VPA (Vertical Pod Autoscaler)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:

      - containerName: myapp
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2000m
          memory: 4Gi
        controlledResources: ["cpu", "memory"]

```

### Deployment with Resource Requests

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
          image: myapp:1.0.0
          resources:
            requests:
              memory: "256Mi"
              cpu: "500m"
            limits:
              memory: "512Mi"
              cpu: "1000m"

```

### Cluster Autoscaler

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      containers:

        - name: cluster-autoscaler
          image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.28.0
          command:

            - ./cluster-autoscaler
            - --v=4
            - --cloud-provider=aws
            - --skip-nodes-with-local-storage=false
            - --expander=least-waste
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster

```

### Managing HPA

```bash
# Create HPA
kubectl apply -f hpa.yaml

# Check HPA status
kubectl get hpa
kubectl describe hpa myapp-hpa

# View metrics
kubectl top pods
kubectl top nodes

# Manual scaling (overrides HPA)
kubectl scale deployment/myapp --replicas=5

# Delete HPA
kubectl delete hpa myapp-hpa

```

## Real-World Use Cases

### 1. Web Application with Traffic Spikes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
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
          image: web:1.0
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 50
  metrics:

    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:

        - type: Percent
          value: 100
          periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:

        - type: Percent
          value: 10
          periodSeconds: 60

```

### 2. API with Custom Metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 5
  maxReplicas: 100
  metrics:

    - type: Pods
      pods:
        metric:
          name: requests_per_second
        target:
          type: AverageValue
          averageValue: "500"

    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

```

### 3. Batch Processing with Queue Length

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: worker
  minReplicas: 1
  maxReplicas: 20
  metrics:

    - type: External
      external:
        metric:
          name: sqs_queue_length
          selector:
            matchLabels:
              queue: "my-queue"
        target:
          type: AverageValue
          averageValue: "10"

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| No resource requests | Always set requests for HPA to work |
| Too aggressive scaling | Use stabilization windows |
| No min/max replicas | Always set bounds |
| Memory-based scaling only | Use CPU as primary metric |
| No scaling policy | Define scale-up/down policies |
| Not monitoring HPA | Watch HPA metrics and events |
| Ignoring VPA | Use VPA for right-sizing |

## Best Practices

```yaml
# GOOD: Production HPA
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
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:

        - type: Pods
          value: 4
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:

        - type: Percent
          value: 10
          periodSeconds: 120

```

1. **Always set resource requests** — required for HPA to calculate utilization

2. **Use CPU as primary metric** — most responsive for scaling

3. **Set min/max replicas** — prevent over/under scaling

4. **Use stabilization windows** — prevent flapping

5. **Define scaling policies** — control scale-up/down speed

6. **Monitor HPA status** — check events and metrics

7. **Use VPA for right-sizing** — optimize resource requests

8. **Test scaling behavior** — load test before production

9. **Combine HPA with PDB** — protect during scaling
10. **Use Cluster Autoscaler** — scale nodes when needed

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Metrics collection interval | Response time | Default 15s is usually fine |
| Stabilization window | Scaling delay | Tune per use case |
| Resource requests accuracy | Scaling accuracy | Use VPA recommendations |
| Max replicas | Cost | Set realistic maximum |
| Scaling policy aggressiveness | Stability | Use conservative policies |

```bash
# Check HPA status
kubectl get hpa -w

# View HPA events
kubectl describe hpa myapp-hpa

# Check current metrics
kubectl top pods -l app=myapp

# Manually trigger scaling test
kubectl run load-test --image=busybox --rm -it -- \
  sh -c "while true; do wget -qO- http://myapp:80; done"

```

## Summary

HPA enables automatic scaling based on metrics. VPA optimizes resource requests. Combined with Cluster Autoscaler, they provide full-stack auto-scaling. Proper resource requests, scaling policies, and stabilization windows are essential for reliable scaling.

## Cheat Sheet
```bash
# HPA
kubectl autoscale deployment myapp --cpu-percent=70 --min=2 --max=10
kubectl get hpa
kubectl describe hpa myapp-hpa
kubectl delete hpa myapp-hpa

# Metrics
kubectl top pods
kubectl top nodes

# VPA
kubectl apply -f vpa.yaml
kubectl get vpa

# Manual scale
kubectl scale deployment myapp --replicas=5

# Cluster Autoscaler
kubectl get nodes
kubectl describe node <name>

```

---

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Docker](../13-Docker/)
- [Observability](../22-Observability/)
- [Pod Disruption Budgets](12-Pod-Disruption-Budgets.md)
- [Resource Quotas](14-Resource-Quotas.md)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
