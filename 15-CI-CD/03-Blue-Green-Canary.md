# Blue-Green & Canary Deployments

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

## Definition

**Blue-Green Deployment** maintains two identical environments (blue and green). One serves production traffic while the other is updated. Traffic switches instantly after validation. **Canary Deployment** gradually rolls out changes to a small subset of users before full deployment.

Key concepts:

- **Blue-Green**: Two identical environments, instant traffic switch
- **Canary**: Gradual rollout to small user subset
- **Rolling Update**: Gradual replacement of instances
- **Feature Flags**: Control feature visibility without deployment
- **Rollback**: Revert to previous version

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Downtime during deployments | Zero-downtime strategies |
| Risk of bad releases | Gradual rollout with validation |
| Slow rollback | Instant switch (blue-green) |
| No A/B testing | Canary for user-based testing |
| Complex deployment process | Automated strategies |
| No traffic control | Fine-grained routing |

## How It Works

### Blue-Green Architecture

```text
                    Load Balancer

                         |

                         v
            +------------------------+

            |    Traffic Router      |
            |   (current: blue)      |

            +------------------------+

                    |           |

                    v           v
            +-----------+ +-----------+

            |   BLUE    | |   GREEN   |
            | (current) | |   (new)   |
            |           | |           |
            | v1.0.0    | | v2.0.0   |

            +-----------+ +-----------+

                 |              |

                 v              v
            +-----------+ +-----------+

            | Database  | | Database  |
            | (shared)  | | (shared)  |

            +-----------+ +-----------+

Step 1: Blue serves traffic (v1.0.0)
Step 2: Deploy v2.0.0 to Green
Step 3: Test Green
Step 4: Switch traffic to Green
Step 5: Blue becomes standby (or rollback target)

```

### Canary Architecture

```text
                    Load Balancer

                         |

                         v
            +------------------------+

            |    Traffic Router      |
            |   (canary: 10%)        |

            +------------------------+

                    |           |

                    v           v
            +-----------+ +-----------+

            |  STABLE   | |  CANARY   |
            |   (90%)   | |   (10%)   |
            |           | |           |
            | v1.0.0    | | v2.0.0   |
            | 9 pods    | | 1 pod     |

            +-----------+ +-----------+

Step 1: Deploy v2.0.0 to 1 pod (10%)
Step 2: Monitor metrics (errors, latency)
Step 3: If healthy, increase to 20%, 50%, 100%
Step 4: If unhealthy, rollback immediately

```

### Rolling Update Architecture

```text
Initial:     [v1] [v1] [v1] [v1] [v1]

Step 1:      [v1] [v1] [v1] [v1] [v2]
Step 2:      [v1] [v1] [v1] [v2] [v2]
Step 3:      [v1] [v1] [v2] [v2] [v2]
Step 4:      [v1] [v2] [v2] [v2] [v2]
Step 5:      [v2] [v2] [v2] [v2] [v2]

```

## Code Examples

### Blue-Green with Kubernetes

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    version: blue
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
          ports:

            - containerPort: 8080

---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    app: myapp
    version: green
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
          ports:

            - containerPort: 8080

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

### Canary with Kubernetes

```yaml
# Stable version (90%)
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
# Canary version (10%)
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

---
# Service (routes to both stable and canary)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:

    - port: 80
      targetPort: 8080

```

### Canary with Ingress (Nginx)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  ingressClassName: nginx
  rules:

    - host: myapp.example.com
      http:
        paths:

          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-canary
                port:
                  number: 80

```

### Feature Flags

```javascript
// Feature flag implementation
const featureFlags = {
  newCheckout: process.env.FEATURE_NEW_CHECKOUT === 'true',
  darkMode: process.env.FEATURE_DARK_MODE === 'true',
};

// Usage
if (featureFlags.newCheckout) {
  return newCheckoutFlow();
} else {
  return legacyCheckoutFlow();
}

```

### Blue-Green Switch Script

```bash
#!/bin/bash
# blue-green-switch.sh

CURRENT_VERSION=$(kubectl get svc myapp -o jsonpath='{.spec.selector.version}')
NEW_VERSION=$([ "$CURRENT_VERSION" = "blue" ] && echo "green" || echo "blue")

echo "Switching from $CURRENT_VERSION to $NEW_VERSION"

# Update service selector
kubectl patch svc myapp -p '{"spec":{"selector":{"version":"'$NEW_VERSION'"}}}'

# Wait for rollout
kubectl rollout status deployment/myapp-$NEW_VERSION

echo "Deployment complete. New version: $NEW_VERSION"

```

### Canary Promotion Script

```bash
#!/bin/bash
# canary-promote.sh

CURRENT_WEIGHT=10
NEW_WEIGHT=$((CURRENT_WEIGHT + 10))

if [ $NEW_WEIGHT -ge 100 ]; then
  echo "Promoting canary to stable"
  kubectl set image deployment/myapp-stable myapp=myapp:2.0.0
  kubectl scale deployment/myapp-canary --replicas=0
else
  echo "Increasing canary weight to $NEW_WEIGHT%"
  kubectl annotate ingress myapp-ingress \
    nginx.ingress.kubernetes.io/canary-weight="$NEW_WEIGHT" \
    --overwrite
fi

```

## Real-World Use Cases

### 1. Blue-Green with AWS ELB

```yaml
# Blue target group
apiVersion: v1
kind: Service
metadata:
  name: myapp-blue
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-target-group-arn: "arn:aws:..."
spec:
  type: LoadBalancer
  selector:
    app: myapp
    version: blue
  ports:

    - port: 80

---
# Green target group
apiVersion: v1
kind: Service
metadata:
  name: myapp-green
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-target-group-arn: "arn:aws:..."
spec:
  type: LoadBalancer
  selector:
    app: myapp
    version: green
  ports:

    - port: 80

```

### 2. Canary with Istio

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:

    - myapp
  http:

    - route:
        - destination:
            host: myapp
            subset: stable
          weight: 90

        - destination:
            host: myapp
            subset: canary
          weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:

    - name: stable
      labels:
        track: stable

    - name: canary
      labels:
        track: canary

```

### 3. Feature Flags with LaunchDarkly

```yaml
# Environment variable for feature flag
env:

  - name: LAUNCHDARKLY_SDK_KEY
    valueFrom:
      secretKeyRef:
        name: feature-flags
        key: sdk-key

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| No rollback strategy | Implement automated rollback |
| No health checks | Add health checks for validation |
| Shared database without migration | Plan for backward-compatible migrations |
| No monitoring | Monitor canary metrics |
| Instant full deployment | Use gradual rollout |
| No feature flags | Use flags for risky features |

## Best Practices

```yaml
# GOOD: Canary deployment with monitoring
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
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            periodSeconds: 10

```

1. **Always have a rollback plan** — automate rollback on failure

2. **Use health checks** — validate deployments before traffic switch

3. **Monitor metrics** — track error rates, latency, and business metrics

4. **Use feature flags** — decouple deployment from release

5. **Test database migrations** — ensure backward compatibility

6. **Start with small canary** — 1-5% traffic initially

7. **Automate promotion** — use metrics for automatic promotion

8. **Use service mesh** — for advanced traffic management

9. **Document runbooks** — for manual intervention
10. **Practice deployments** — test in staging first

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Blue-green resource usage | Cost (2x) | Scale down standby |
| Canary duration | Time to full deployment | Balance speed and risk |
| Traffic split accuracy | User experience | Use service mesh |
| Rollback speed | Recovery time | Blue-green: instant |
| Database migrations | Complexity | Backward-compatible changes |

```bash
# Monitor canary
kubectl top pods -l track=canary
kubectl logs -l track=canary -f

# Check metrics
curl http://prometheus:9090/api/v1/query?query=rate(http_requests_total[5m])

# Switch traffic (blue-green)
kubectl patch svc myapp -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback (blue-green)
kubectl patch svc myapp -p '{"spec":{"selector":{"version":"blue"}}}'

```

## Summary

Blue-green provides instant traffic switching and rollback. Canary enables gradual rollout with validation. Feature flags decouple deployment from release. Choose based on risk tolerance, rollback needs, and validation requirements.

## Cheat Sheet
```bash
# Blue-Green switch
kubectl patch svc myapp -p '{"spec":{"selector":{"version":"green"}}}'

# Blue-Green rollback
kubectl patch svc myapp -p '{"spec":{"selector":{"version":"blue"}}}'

# Canary scale up
kubectl scale deployment/myapp-canary --replicas=2

# Canary scale down
kubectl scale deployment/myapp-canary --replicas=0

# Monitor canary
kubectl top pods -l track=canary
kubectl logs -l track=canary -f

# Feature flag
export FEATURE_NEW_CHECKOUT=true

```

---

---

## See Also
- [Docker](../13-Docker/)
- [Git Advanced](../24-Git-Advanced/)
- [Kubernetes](../14-Kubernetes/)

## References & Learn More

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [CI/CD Pipeline Design Patterns](https://martinfowler.com/articles/continuousIntegration.html)
- [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/0991538429)
