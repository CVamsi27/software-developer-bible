---
section: Kubernetes
category: DevOps
tags: [concept]
---

# Kubernetes Health Checks

## Definition

**Health checks** in Kubernetes verify that containers are running correctly. There are three types: **startup probes** (initialization), **liveness probes** (ongoing health), and **readiness probes** (traffic readiness). They enable self-healing and traffic management.

Key concepts:

- **Startup Probe**: Runs once at container startup, disables other probes until success
- **Liveness Probe**: Checks if container is alive; restarts on failure
- **Readiness Probe**: Checks if container can receive traffic; removes from Service on failure
- **Probe Handler**: exec, httpGet, tcpSocket, or gRPC

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Crashed containers continue receiving traffic | Readiness probe removes from Service |
| Stuck containers never restart | Liveness probe triggers restart |
| Slow-starting containers killed too early | Startup probe delays other probes |
| No traffic draining | Readiness probe enables graceful removal |
| No self-healing | Liveness probe enables automatic restart |
| No dependency waiting | Startup probe waits for dependencies |

## How It Works

### Probe Architecture

```text
                    kubelet

                      |

         +------------+------------+

         |            |            |

         v            v            v
  +------------+ +------------+ +------------+

  |  Startup   | |  Liveness  | |  Readiness |
  |   Probe    | |   Probe    | |   Probe    |
  |            | |            | |            |
  |  Runs:     | |  Runs:     | |  Runs:     |
  |  once at   | |  periodic  | |  periodic  |
  |  startup   | |  after     | |  after     |
  |            | |  startup   | |  startup   |

  +-----+------+ +-----+------+ +-----+------+

        |              |              |

        v              v              v
  +------------+ +------------+ +------------+

  |  Success:  | |  Failure:  | |  Failure:  |
  |  Enable    | |  Restart   | |  Remove    |
  |  liveness  | |  container | |  from svc  |
  |  & ready   | |            | |            |

  +------------+ +------------+ +------------+

```

### Probe Timeline

```text
Container Start

      |

      v
[Startup Probe] -----> Success -----> [Liveness Probe] -----> [Readiness Probe]

      |                    |                    |                      |
      |                    |                    |                      |

      v                    v                    v                      v
   Failure             Failure              Failure                Failure
   (restart)           (restart)           (restart)              (remove from svc)

```

## Code Examples

### All Three Probes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:

    - name: myapp
      image: myapp:1.0.0
      ports:

        - containerPort: 8080

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
        failureThreshold: 3

```

### Exec Probe

```yaml
livenessProbe:
  exec:
    command:

      - cat
      - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 10

```

### TCP Socket Probe

```yaml
livenessProbe:
  tcpSocket:
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10

```

### gRPC Probe

```yaml
livenessProbe:
  grpc:
    port: 50051
  initialDelaySeconds: 10
  periodSeconds: 10

```

### Startup Probe with Failure Threshold

```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
  # 30 * 10s = 300s max startup time

```

### Deployment with Probes

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
          ports:

            - containerPort: 8080

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
            failureThreshold: 3

```

### Health Check Endpoint Example

```javascript
// Node.js health check endpoints
const express = require('express');
const app = express();

// Startup: is the app initialized?
app.get('/health', (req, res) => {
  if (app.isReady) {
    res.status(200).json({ status: 'ok' });
  } else {
    res.status(503).json({ status: 'starting' });
  }
});

// Readiness: can the app receive traffic?
app.get('/ready', (req, res) => {
  if (app.dbConnected && app.cacheConnected) {
    res.status(200).json({ status: 'ready' });
  } else {
    res.status(503).json({ status: 'not ready' });
  }
});

// Liveness: is the app alive?
app.get('/alive', (req, res) => {
  res.status(200).json({ status: 'alive' });
});

```

## Real-World Use Cases

### 1. Database Application

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
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
          ports:

            - containerPort: 5432

          startupProbe:
            exec:
              command:

                - pg_isready
                - -U
                - postgres
            failureThreshold: 30
            periodSeconds: 10

          livenessProbe:
            exec:
              command:

                - pg_isready
                - -U
                - postgres
            periodSeconds: 15
            timeoutSeconds: 5

          readinessProbe:
            exec:
              command:

                - pg_isready
                - -U
                - postgres
            periodSeconds: 10
            timeoutSeconds: 5

```

### 2. Microservice with Dependencies

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:

        - name: api
          image: api:1.0
          ports:

            - containerPort: 8080

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
            successThreshold: 1
            failureThreshold: 3

```

### 3. Worker Process

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: worker
  template:
    metadata:
      labels:
        app: worker
    spec:
      containers:

        - name: worker
          image: worker:1.0

          livenessProbe:
            exec:
              command:

                - cat
                - /tmp/healthy
            periodSeconds: 30
            timeoutSeconds: 5
            failureThreshold: 3

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| No startup probe | Add startup probe for slow-starting apps |
| Too aggressive liveness | Increase failureThreshold and periodSeconds |
| Same path for all probes | Use different endpoints for health/ready |
| No timeoutSeconds | Always set timeout |
| Checking external dependencies in liveness | Only check self-health in liveness |
| Not implementing health endpoints | Implement /health, /ready, /alive |

## Best Practices

```yaml
# GOOD: Production health checks
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
  failureThreshold: 3
  successThreshold: 1

```

1. **Implement all three probe types** — startup, liveness, readiness

2. **Use different endpoints** — /health, /ready, /alive

3. **Set appropriate timeouts** — prevent hanging probes

4. **Use startup probe for slow apps** — prevent premature liveness failures

5. **Don't check external deps in liveness** — only check self-health

6. **Check dependencies in readiness** — ensure traffic readiness

7. **Tune failure thresholds** — balance between responsiveness and stability

8. **Monitor probe results** — track probe failures in metrics

9. **Use exec for simple checks** — cat file, pg_isready
10. **Use httpGet for web apps** — standard health check pattern

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Probe frequency | Resource overhead | Tune periodSeconds |
| Probe timeout | Latency | Set reasonable timeouts |
| Health endpoint complexity | Response time | Keep health checks lightweight |
| Failure threshold | Recovery time | Balance with stability |
| Startup probe duration | Deployment speed | Set appropriate failureThreshold |

```bash
# Check pod health status
kubectl get pods
kubectl describe pod myapp | grep -A 10 "Conditions"

# View probe events
kubectl get events --field-selector reason=Unhealthy

# Check probe configuration
kubectl get pod myapp -o jsonpath='{.spec.containers[*].livenessProbe}'

```


## Summary

Health checks enable self-healing and traffic management. Startup probes handle initialization, liveness probes ensure ongoing health, and readiness probes control traffic routing. Proper probe configuration is essential for production reliability.

## Cheat Sheet
```bash
# Check pod status
kubectl get pods
kubectl describe pod myapp | grep -A 10 "Conditions"

# View probe events
kubectl get events --field-selector reason=Unhealthy

# Check probe configuration
kubectl get pod myapp -o jsonpath='{.spec.containers[*].livenessProbe}'

# Restart pod (trigger liveness probe)
kubectl delete pod myapp

# View health endpoint
kubectl exec -it myapp -- curl http://localhost:8080/health

```

---

---

## See Also
- [Docker](../13-Docker/)
- [CI/CD](../15-CI-CD/)
- [Observability](../22-Observability/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
