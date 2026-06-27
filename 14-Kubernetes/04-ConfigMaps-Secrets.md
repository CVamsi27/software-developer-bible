# Kubernetes ConfigMaps & Secrets

## Definition

**ConfigMaps** store non-sensitive configuration data as key-value pairs. **Secrets** store sensitive data (passwords, tokens, certificates). Both can be consumed as environment variables or mounted as files in Pods.

Key concepts:
- **ConfigMap**: Non-sensitive configuration data
- **Secret**: Sensitive data (base64 encoded, not encrypted by default)
- **Environment variable**: Inject ConfigMap/Secret as env var
- **Volume mount**: Mount as files in the container
- **Immutable**: Prevent changes after creation

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Hardcoded config in images | ConfigMaps separate config from code |
| Secrets in Dockerfiles | Secrets stored securely in etcd |
| Config changes require rebuild | ConfigMaps can be updated |
| No version control for config | ConfigMaps are Kubernetes resources |
| Sensitive data exposure | Secrets with RBAC and encryption |

## How It Works

### Architecture

```
+----------------------------------------------------------+
|                    Kubernetes Cluster                      |
|                                                           |
|  +------------------+    +------------------+            |
|  |    ConfigMap      |    |      Secret      |            |
|  |  key1: value1     |    |  key1: base64   |            |
|  |  key2: value2     |    |  key2: base64   |            |
|  +--------+---------+    +--------+---------+            |
|           |                      |                        |
|           +----------+-----------+                        |
|                      |                                    |
|                      v                                    |
|  +--------------------------------------------------+   |
|  |                      Pod                           |   |
|  |  +-------------------+  +-------------------+    |   |
|  |  |   Container       |  |   Container       |    |   |
|  |  |                   |  |                   |    |   |
|  |  | ENV:              |  | VOLUME:           |    |   |
|  |  |  DB_HOST=prod-db  |  |  /etc/config/     |    |   |
|  |  |  DB_PASS=***      |  |    config.json    |    |   |
|  |  +-------------------+  +-------------------+    |   |
|  +--------------------------------------------------+   |
+----------------------------------------------------------+
```

## Code Examples

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  DATABASE_HOST: "postgres.production.svc.cluster.local"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"
  config.json: |
    {
      "apiUrl": "https://api.example.com",
      "features": {
        "darkMode": true,
        "notifications": true
      }
    }
  nginx.conf: |
    server {
      listen 80;
      server_name example.com;
      location / {
        proxy_pass http://localhost:8080;
      }
    }
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQxMjM=  # base64 encoded
  API_KEY: c2tfbGl2ZV9hYmMxMjM=
  JWT_SECRET: c2VjcmV0X2p3dF9rZXk=
```

### Create from literals

```bash
# ConfigMap
kubectl create configmap app-config \
  --from-literal=DATABASE_HOST=postgres \
  --from-literal=LOG_LEVEL=info

# Secret
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_PASSWORD=password123 \
  --from-literal=API_KEY=sk_live_abc123

# From file
kubectl create configmap nginx-config \
  --from-file=nginx.conf

# From env file
kubectl create secret generic db-creds \
  --from-env-file=.env
```

### Environment Variable Injection

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: myapp
      image: myapp:1.0.0
      env:
        # From ConfigMap key
        - name: DATABASE_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DATABASE_HOST

        # From Secret key
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_PASSWORD

      # All keys from ConfigMap
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
```

### Volume Mount

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: myapp
      image: myapp:1.0.0
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
          readOnly: true
        - name: secret-volume
          mountPath: /etc/secrets
          readOnly: true

  volumes:
    - name: config-volume
      configMap:
        name: app-config
    - name: secret-volume
      secret:
        secretName: app-secrets
        defaultMode: 0400
```

### Deployment with ConfigMap and Secret

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

          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets

          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/nginx.conf
              subPath: nginx.conf

      volumes:
        - name: nginx-config
          configMap:
            name: nginx-config
```

### Immutable ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
immutable: true
data:
  DATABASE_HOST: "postgres"
  LOG_LEVEL: "info"
```

## Real-World Use Cases

### 1. Application Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: "production"
  PORT: "3000"
  LOG_FORMAT: "json"
  app.json: |
    {
      "name": "myapp",
      "version": "1.0.0",
      "features": {
        "analytics": true,
        "betaFeatures": false
      }
    }
```

### 2. Database Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  POSTGRES_DB: bXlhcHA=           # myapp
  POSTGRES_USER: cG9zdGdyZXM=     # postgres
  POSTGRES_PASSWORD: c2VjcmV0     # secret
```

### 3. TLS Certificate

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
spec:
  tls:
    - hosts:
        - example.com
      secretName: tls-secret
```

### 4. Docker Registry Credentials

```bash
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=user@example.com
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Committing secrets to git | Use external secret management |
| Not base64 encoding secrets | `echo -n "password" | base64` |
| Using Secrets for non-sensitive data | Use ConfigMaps for non-sensitive |
| Hardcoding config in images | Use ConfigMaps |
| Not setting defaultMode | Set restrictive file permissions |
| Using same Secret across namespaces | Create separate Secrets per namespace |
| Not rotating secrets | Implement secret rotation |

## Best Practices

```yaml
# GOOD: Production-ready ConfigMap and Secret
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
  labels:
    app: myapp
data:
  NODE_ENV: "production"
  LOG_LEVEL: "warn"
  config.json: |
    {
      "database": {
        "host": "postgres.production.svc.cluster.local",
        "port": 5432,
        "pool": {
          "min": 2,
          "max": 10
        }
      }
    }

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
  labels:
    app: myapp
type: Opaque
data:
  DATABASE_PASSWORD: <base64-encoded>

---
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
      serviceAccountName: myapp-sa
      containers:
        - name: myapp
          image: myapp:1.0.0
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets
          volumeMounts:
            - name: config
              mountPath: /etc/config
              readOnly: true
      volumes:
        - name: config
          configMap:
            name: app-config
```

1. **Never commit secrets to Git** — use external secret management
2. **Use immutable ConfigMaps** — prevent accidental changes
3. **Set restrictive file permissions** — `defaultMode: 0400` for secrets
4. **Rotate secrets regularly** — implement secret rotation
5. **Use namespaces** — isolate ConfigMaps/Secrets per namespace
6. **Use RBAC** — restrict access to Secrets
7. **Enable encryption at rest** — encrypt Secrets in etcd
8. **Use external secret stores** — Vault, AWS SSM, GCP Secret Manager
9. **Version your ConfigMaps** — append version suffixes
10. **Monitor ConfigMap changes** — audit ConfigMap updates

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| ConfigMap size | Etcd performance | Keep under 1MB |
| Secret size | Etcd performance | Keep under 1MB |
| Volume mount updates | File system overhead | Use projected volumes |
| Environment variable updates | Pod restart required | Use volume mounts |
| Immutable ConfigMaps | Better performance | Enable for static configs |

```bash
# Create ConfigMap from file
kubectl create configmap myconfig \
  --from-file=config.json \
  --from-literal=key=value

# View ConfigMap
kubectl get configmap myconfig -o yaml

# View Secret (decoded)
kubectl get secret mysecret -o jsonpath='{.data.DB_PASS}' | base64 -d

# Edit ConfigMap
kubectl edit configmap myconfig

# Delete ConfigMap
kubectl delete configmap myconfig
```

## Interview Questions

### Beginner (5-10)

1. **What is a ConfigMap?**
   Stores non-sensitive configuration data as key-value pairs for Pods.

2. **What is a Secret?**
   Stores sensitive data (passwords, tokens) in base64-encoded format.

3. **What is the difference between ConfigMap and Secret?**
   ConfigMaps are for non-sensitive data. Secrets are for sensitive data with base64 encoding.

4. **How do you use a ConfigMap in a Pod?**
   As environment variables (envFrom) or volume mounts.

5. **How do you create a Secret from a file?**
   `kubectl create secret generic mysecret --from-file=key.json`

6. **What is base64 encoding?**
   A binary-to-text encoding scheme. Not encryption—just encoding.

7. **How do you update a ConfigMap?**
   `kubectl edit configmap myconfig` or `kubectl apply -f configmap.yaml`

8. **What happens when a ConfigMap is updated?**
   Volume mounts are updated automatically. Environment variables require Pod restart.

9. **What is an immutable ConfigMap?**
   A ConfigMap that cannot be updated after creation.

10. **How do you view Secret values?**
    `kubectl get secret mysecret -o jsonpath='{.data.key}' | base64 -d`

### Intermediate (5-10)

11. **How do you mount a ConfigMap as a file?**
    Use `volumes` and `volumeMounts` in the Pod spec.

12. **What is envFrom?**
    Injects all keys from a ConfigMap/Secret as environment variables.

13. **How do you set file permissions for mounted Secrets?**
    Use `defaultMode` in the volume spec.

14. **What is projected volume?**
    Combines multiple ConfigMaps/Secrets into a single volume.

15. **How do you encrypt Secrets at rest?**
    Enable encryption provider in kube-apiserver configuration.

16. **What is the maximum size of a ConfigMap/Secret?**
    1MB (limited by etcd).

17. **How do you share ConfigMaps across namespaces?**
    You can't directly. Copy or use external configuration management.

18. **What is the difference between configMapRef and configMapKeyRef?**
    configMapRef injects all keys. configMapKeyRef injects a specific key.

19. **How do you handle ConfigMap updates without Pod restart?**
    Mount as volume. Kubernetes updates the mounted files automatically.

20. **What is the security implication of Secrets?**
    Base64 is not encryption. Enable etcd encryption and RBAC.

### Senior (10-15)

21. **How would you manage secrets across multiple environments?**
    Use external secret stores (Vault), namespace isolation, and secret rotation.

22. **Explain etcd encryption for Secrets.**
    Enable EncryptionConfiguration in kube-apiserver with AES-CBC or AES-GCM.

23. **How do you implement secret rotation?**
    Use external-secrets operator, sealed-secrets, or custom controllers.

24. **What is the difference between Secret types?**
    Opaque (generic), kubernetes.io/tls, kubernetes.io/dockerconfigjson, kubernetes.io/basic-auth.

25. **How do you audit ConfigMap/Secret access?**
    Enable Kubernetes audit logging and monitor access events.

### FAANG-style (5-10)

26. **Design a secrets management architecture for 100+ microservices.**
    Use HashiCorp Vault with Kubernetes auth, external-secrets operator, and automated rotation.

27. **How would you handle secrets in a multi-cluster setup?**
    Use central secret store with replication, or sealed-secrets per cluster.

28. **Design a ConfigMap management strategy for configuration drift.**
    Use GitOps with ConfigMap as Code, automated validation, and drift detection.

29. **How would you implement zero-downtime secret rotation?**
    Use projected volumes with auto-reload, or external-secrets operator.

30. **Describe a compliance strategy for secrets management.**
    Encryption at rest, RBAC, audit logging, rotation policies, and access reviews.

### Follow-ups (5-10)

31. **What is the difference between Secret and ConfigMap?**
    Secret is base64-encoded and supports RBAC. ConfigMap is plain text.

32. **How do you use Secrets with Helm?**
    Use Helm secrets plugin or external-secrets operator.

33. **What is sealed-secrets?**
    A Kubernetes controller that decrypts Secrets encrypted with kubeseal.

34. **How do you handle secrets in CI/CD pipelines?**
    Use CI/CD secrets management, not Kubernetes Secrets.

35. **What is the difference between env and volume mount for Secrets?**
    Env: available as environment variable. Volume: mounted as file.

## Summary

ConfigMaps and Secrets separate configuration from code. ConfigMaps store non-sensitive data; Secrets store sensitive data. Use volume mounts for automatic updates, environment variables for simplicity, and external secret management for production security.

## Cheat Sheet

```bash
# ConfigMap
kubectl create configmap myconfig --from-literal=key=value
kubectl create configmap myconfig --from-file=config.json
kubectl get configmap myconfig -o yaml
kubectl describe configmap myconfig

# Secret
kubectl create secret generic mysecret --from-literal=key=value
kubectl create secret tls tls-secret --cert=cert.pem --key=key.pem
kubectl get secret mysecret -o jsonpath='{.data.key}' | base64 -d

# Apply
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

# Delete
kubectl delete configmap myconfig
kubectl delete secret mysecret
```

---

## References & Learn More
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Learn Kubernetes The Easy Way](https://learnk8s.io/)
- [Kubernetes Patterns by Bilgin Ibryam](https://www.amazon.com/Kubernetes-Patterns-Cloud-Native-Applications/dp/1492050288)
- [CNCF Landscape](https://landscape.cncf.io/)
