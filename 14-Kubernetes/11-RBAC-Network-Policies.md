---
section: Kubernetes
category: DevOps
tags: [concept]
---

# RBAC & Network Policies

## Definition

**RBAC (Role-Based Access Control)** controls who can access the Kubernetes API and what actions they can perform. **Network Policies** control how pods communicate with each other and external services. Both are fundamental to Kubernetes security.

## Why Do We Need It?

1. **RBAC**: Principle of least privilege, multi-team clusters, audit compliance (SOC2, PCI-DSS)
2. **Network Policies**: Micro-segmentation, zero-trust networking, prevent lateral movement

## Code Examples

### RBAC: Role & RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: default
  name: read-pods
subjects:
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

---

### See Also

- [ConfigMaps & Secrets](../04-ConfigMaps-Secrets.md)
- [Security Contexts](../01-Pods-ReplicaSets.md)

### References

- [K8s RBAC Docs](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [K8s Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
