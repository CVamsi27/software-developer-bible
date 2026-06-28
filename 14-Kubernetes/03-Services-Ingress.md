# Kubernetes Services & Ingress

## Definition

**Services** provide stable networking for a set of Pods. They load-balance traffic across Pods and provide DNS-based service discovery. **Ingress** manages external HTTP/HTTPS access to Services, providing routing, TLS termination, and virtual hosting.

Key concepts:

- **Service**: Stable IP and DNS name for a set of Pods
- **ClusterIP**: Internal-only service access
- **NodePort**: Expose service on each node's IP
- **LoadBalancer**: Cloud provider load balancer
- **Ingress**: HTTP/HTTPS routing rules
- **Ingress Controller**: Implements Ingress rules (nginx, traefik, etc.)

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Pod IPs are ephemeral | Service provides stable IP |
| No load balancing | Service distributes traffic |
| No external access | NodePort/LoadBalancer |
| No HTTP routing | Ingress rules |
| No TLS termination | Ingress with TLS |
| No virtual hosting | Ingress host-based routing |

## How It Works

### Service Architecture

```text
                        Internet

                            |

                            v
                    +---------------+

                    | LoadBalancer  |
                    | (Cloud LB)   |

                    +-------+-------+

                            |

                            v
                    +---------------+

                    |    Ingress    |
                    |   Controller  |

                    +-------+-------+

                            |

              +-------------+-------------+

              |             |             |

              v             v             v
      +-----------+  +-----------+  +-----------+

      |  Service  |  |  Service  |  |  Service  |
      |  (web)    |  |  (api)    |  |  (admin)  |

      +-----------+  +-----------+  +-----------+

         |    |        |    |        |    |

         v    v        v    v        v    v
      +----+ +----+ +----+ +----+ +----+ +----+

      |Pod | |Pod | |Pod | |Pod | |Pod | |Pod |

      +----+ +----+ +----+ +----+ +----+ +----+

```

### Service Types

```text
ClusterIP (default):
+------------------+

| Service          |

| 10.96.0.10:80    |  <-- Cluster-internal IP
+------------------+
  Accessible from: Pods in cluster only

NodePort:
+------------------+

| Service          |

| NodePort: 30080  |  <-- Exposed on every node
+------------------+
  Accessible from: External via <NodeIP>:30080

LoadBalancer:
+------------------+

| Service          |

| Type: LoadBalancer|  <-- Cloud provider LB
+------------------+
  Accessible from: External via LB IP

```

### Ingress Architecture

```text
                      External Traffic

                            |

                            v
                    +---------------+

                    |   Ingress    |
                    |   Controller |
                    |   (nginx)    |

                    +-------+-------+

                            |

                            v
                    +---------------+

                    |   Ingress    |
                    |    Rules     |

                    +-------+-------+

                            |

              +-------------+-------------+

              |             |             |

              v             v             v
        api.example.com  web.example.com  admin.example.com

              |             |             |

              v             v             v
        +---------+   +---------+   +---------+

        | api-svc |   | web-svc |   |admin-svc|
        | :8080   |   | :80     |   | :3000   |

        +---------+   +---------+   +---------+

```

## Code Examples

### ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:

    - protocol: TCP
      port: 80
      targetPort: 8080

```

### NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  type: NodePort
  selector:
    app: myapp
  ports:

    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30080

```

### LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
  annotations:
    # AWS-specific annotations
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-internal: "false"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:

    - protocol: TCP
      port: 80
      targetPort: 8080
  loadBalancerSourceRanges:

    - 10.0.0.0/8

```

### Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
spec:
  clusterIP: None  # Headless
  selector:
    app: myapp
  ports:

    - protocol: TCP
      port: 80
      targetPort: 8080

```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:

    - hosts:
        - api.example.com
        - web.example.com
      secretName: tls-secret
  rules:

    - host: api.example.com
      http:
        paths:

          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080

    - host: web.example.com
      http:
        paths:

          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80

    - host: admin.example.com
      http:
        paths:

          - path: /api
            pathType: Prefix
            backend:
              service:
                name: admin-api
                port:
                  number: 8080

          - path: /
            pathType: Prefix
            backend:
              service:
                name: admin-frontend
                port:
                  number: 80

```

### Multi-Path Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-paths
spec:
  ingressClassName: nginx
  rules:

    - host: myapp.example.com
      http:
        paths:

          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080

          - path: /static
            pathType: Prefix
            backend:
              service:
                name: static-service
                port:
                  number: 80

          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80

```

### Managing Services

```bash
# Create service
kubectl apply -f service.yaml

# Get services
kubectl get svc
kubectl get svc -n production

# Describe service
kubectl describe svc myapp

# Check endpoints
kubectl get endpoints myapp

# Test service from within cluster
kubectl run curl --image=curlimages/curl --rm -it -- \
  curl http://myapp:80

# Expose deployment as service
kubectl expose deployment myapp --port=80 --target-port=8080

```

## Real-World Use Cases

### 1. Microservices Application

```yaml
# API Service
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  type: ClusterIP
  selector:
    app: api-gateway
  ports:

    - port: 80
      targetPort: 3000
---
# Auth Service
apiVersion: v1
kind: Service
metadata:
  name: auth-service
spec:
  type: ClusterIP
  selector:
    app: auth
  ports:

    - port: 80
      targetPort: 8080
---
# User Service
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  type: ClusterIP
  selector:
    app: user
  ports:

    - port: 80
      targetPort: 8080

```

### 2. Ingress with Rate Limiting

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
spec:
  ingressClassName: nginx
  tls:

    - hosts:
        - api.example.com
      secretName: api-tls
  rules:

    - host: api.example.com
      http:
        paths:

          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80

```

### 3. gRPC Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: grpc-service
  annotations:
    # gRPC specific annotations
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: grpc-server
  ports:

    - name: grpc
      port: 50051
      targetPort: 50051
      protocol: TCP

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| No health checks on Service | Use readiness probes for endpoints |
| Using NodePort in production | Use LoadBalancer or Ingress |
| No TLS on Ingress | Always use TLS in production |
| Hardcoded Pod IPs | Use Service DNS names |
| No resource limits | Set limits on all Pods |
| Missing annotations | Use correct annotations for cloud provider |
| No network policies | Restrict traffic between services |

## Best Practices

```yaml
# GOOD: Production Service + Ingress
apiVersion: v1
kind: Service
metadata:
  name: api-service
  labels:
    app: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:

    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:

    - hosts:
        - api.example.com
      secretName: api-tls
  rules:

    - host: api.example.com
      http:
        paths:

          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80

```

1. **Use ClusterIP by default** — only expose externally when needed

2. **Always use TLS** — encrypt external traffic

3. **Add readiness probes** — ensure traffic only goes to ready Pods

4. **Use annotations** — configure Ingress controller features

5. **Set resource limits** — prevent resource exhaustion

6. **Use network policies** — restrict inter-service traffic

7. **Monitor service health** — track endpoint availability

8. **Use headless services** — for stateful applications

9. **Configure health checks** — enable load balancer health checks
10. **Use external-dns** — automate DNS record management

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Service type | Latency | ClusterIP < NodePort < LoadBalancer |
| Session affinity | Load distribution | Disable unless required |
| External traffic policy | Hop count | Use Local for same-node routing |
| Connection draining | Graceful shutdown | Configure preStop hooks |
| Rate limiting | Protection | Set appropriate limits |

```bash
# Check service endpoints
kubectl get endpoints myapp

# Test service connectivity
kubectl run test --image=busybox --rm -it -- wget -qO- http://myapp:80

# Check Ingress status
kubectl get ingress
kubectl describe ingress myapp-ingress

# View Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

```

## Interview Questions

### Beginner (5-10)

1. **What is a Kubernetes Service?**
   A stable network endpoint for a set of Pods, providing load balancing and DNS.

2. **What are the Service types?**
   ClusterIP, NodePort, LoadBalancer, ExternalName.

3. **What is the difference between ClusterIP and NodePort?**
   ClusterIP is internal only. NodePort exposes on each node's IP.

4. **What is an Ingress?**
   Manages external HTTP/HTTPS access to Services with routing rules.

5. **How does a Service find its Pods?**
   Via label selectors matching Pod labels.

6. **What is a headless Service?**
   A Service with `clusterIP: None`, returning Pod IPs directly.

7. **What is the default Service type?**
   ClusterIP.

8. **How do you expose a Deployment externally?**
   Create a Service of type NodePort or LoadBalancer, or use Ingress.

9. **What is an Ingress Controller?**
   A reverse proxy that implements Ingress rules (nginx, traefik, etc.).

10. **How do you enable TLS on Ingress?**
    Add a `tls` section with host and secret reference.

### Intermediate (5-10)

11. **How does Kubernetes handle service discovery?**
    CoreDNS resolves service names to cluster IPs. Environment variables also work.

12. **What is the difference between Service and Ingress?**
    Service provides L4 load balancing. Ingress provides L7 routing with host/path rules.

13. **How do you configure session affinity?**
    Set `sessionAffinity: ClientIP` in the Service spec.

14. **What is externalTrafficPolicy?**
    Controls how external traffic is routed: `Cluster` (default) or `Local`.

15. **How do you rate-limit traffic in Ingress?**
    Use Ingress controller annotations (e.g., nginx.ingress.kubernetes.io/rate-limit).

16. **What is a ServiceEntry in Istio?**
    Extends service mesh to external services not in Kubernetes.

17. **How do you handle gRPC load balancing?**
    Use headless service or configure gRPC load balancing in the Service.

18. **What is the difference between LoadBalancer and NodePort?**
    NodePort exposes on node IP. LoadBalancer provisions a cloud load balancer.

19. **How do you manage TLS certificates?**
    Use cert-manager for automatic Let's Encrypt certificates.

20. **What is the difference between Ingress and Gateway API?**
    Gateway API is the next-gen standard with richer features and better role separation.

### Senior (10-15)

21. **How would you design a multi-tenant ingress architecture?**
    Use namespace-based isolation, separate Ingress controllers per tenant, and network policies.

22. **Explain Ingress controller traffic flow.**
    External traffic hits LB -> Ingress controller Pod -> routes to Service -> Pod.

23. **How do you handle WebSocket connections in Ingress?**
    Use annotations for WebSocket upgrade support: `nginx.ingress.kubernetes.io/proxy-read-timeout`.

24. **What is the difference between LoadBalancer and MetalLB?**
    LoadBalancer uses cloud provider LB. MetalLB provides bare-metal LoadBalancer implementation.

25. **How do you implement canary deployments with Ingress?**
    Use Ingress annotations for traffic splitting (nginx.ingress.kubernetes.io/canary-weight).

### FAANG-style (5-10)

26. **Design a global load balancing architecture for a multi-region application.**
    Use cloud LB for regional routing, Ingress for local routing, and DNS for geographic distribution.

27. **How would you handle 1M+ requests per second?**
    Use horizontal pod autoscaling, connection pooling, CDN, and efficient Ingress configuration.

28. **Design a zero-downtime service migration strategy.**
    Use Ingress traffic shifting, Service label updates, and DNS TTL management.

29. **How would you implement service mesh without Istio?**
    Use Linkerd for lighter-weight service mesh, or configure mTLS manually.

30. **Describe a disaster recovery strategy for Ingress.**
    Multi-cluster Ingress, failover DNS, cross-region replication, and automated recovery.

### Follow-ups (5-10)

31. **What is the difference between Ingress and Egress?**
    Ingress: external -> cluster. Egress: cluster -> external.

32. **How do you handle UDP traffic in Kubernetes?**
    Use LoadBalancer Service with `protocol: UDP` or NodePort.

33. **What is the maximum number of Services per namespace?**
    No hard limit, but performance degrades with many Services.

34. **How do you monitor Service health?**
    Use Prometheus metrics, endpoint health checks, and Service mesh observability.

35. **What is a ExternalName Service?**
    Maps a service name to a DNS CNAME record for external services.

## Summary

Services provide stable networking for Pods. Ingress manages external HTTP/HTTPS access. Together, they enable service discovery, load balancing, and external traffic management in Kubernetes.

## Cheat Sheet

```bash
# Services
kubectl get svc
kubectl describe svc myapp
kubectl get endpoints myapp
kubectl expose deployment myapp --port=80 --target-port=8080

# Ingress
kubectl get ingress
kubectl describe ingress myapp
kubectl apply -f ingress.yaml

# Testing
kubectl run test --image=curlimages/curl --rm -it -- curl http://myapp:80

# Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

```

---

## References & Learn More

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
