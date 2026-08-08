---
section: Kubernetes
category: DevOps
tags: [concept]
---

# PodPresets

## TL;DR

A (now-deprecated) alpha API for admission-time injection of env, secrets, and volumes into Pods. Largely superseded by Kyverno/OPA Gatekeeper.

**Why it matters:** Tests the older injection pattern and the modern policy engines that replaced it. Often asked as a "what was this and what replaced it?" question.

## Definition

**PodPreset** is a Kubernetes API resource that injects runtime configuration (environment variables, secrets, volumes, volume mounts) into pods at admission time — without modifying the pod template or deployment spec. PodPresets match pods by label selector and automatically add specified configuration before the pod is created. This decouples configuration from pod/Deployment definitions, enabling platform teams to enforce standards (sidecars, proxy settings, monitoring agents) without application team involvement.

> **Note:** PodPresets were introduced as an alpha feature in Kubernetes 1.6 and are **not enabled by default** in most clusters. They remain in alpha as of recent Kubernetes versions. For production use, consider alternatives like **Admission Webhooks** (MutatingAdmissionWebhook), **OPA/Gatekeeper**, or **Kyverno**.

## Why Do We Need It?

1. **Platform standardization** — Inject logging, monitoring, and proxy sidecars without app changes
2. **Secret injection** — Automatically mount service mesh certificates or registry credentials
3. **Proxy configuration** — Add HTTP_PROXY, HTTPS_PROXY, NO_PROXY env vars to all pods
4. **Volume mounts** — Mount shared CA certificates, timezone data, or config files
5. **Cross-cutting concerns** — Separate infrastructure configuration from application configuration

## How It Works

### Admission-Time Injection

```text
PodPreset Injection Flow:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                  POD CREATION FLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User creates Pod (or Deployment creates Pod)             │
│                                                              │
│  2. API Server receives Pod create request                   │
│                                                              │
│  3. Admission Controller runs:                               │
│     ├── Fetch all PodPresets in the namespace                │
│     ├── Check if Pod matches ANY PodPreset label selector    │
│     │   └── PodPreset.matchLabels vs Pod.metadata.labels     │
│     └── If match found:                                      │
│         ├── Merge: Env vars                                  │
│         ├── Merge: Volume mounts                             │
│         ├── Merge: Volumes                                  │
│         ├── Add: VolumeMount annotations                     │
│         └── Annotate: "podpreset.admission.kubernetes.io"    │
│                                                              │
│  4. Pod is created with injected configuration               │
│                                                              │
│  5. Changes are NOT persisted in Pod template                │
│     (Only the running pod is affected)                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### PodPreset Lifecycle

```text
PodPreset Merge Behavior:
═══════════════════════════════════════════════════════════════

PodPreset Spec:
├── selector: Pod label selector (REQUIRED)
├── env: Environment variables to inject
├── envFrom: ConfigMap/Secret references
├── volumes: Volumes to add
├── volumeMounts: Volume mounts to add
└── labels: Additional labels to add to Pod

Merge Rules:
├── Environment variables:
│   ├── PodPreset env vars are ADDED to existing
│   └── If key already exists in Pod spec → PodPreset OVERWRITES
├── Volumes:
│   ├── PodPreset volumes are APPENDED
│   └── Conflicts handled by last-applied
├── VolumeMounts:
│   ├── PodPreset mounts are APPENDED
│   └── Must reference a Volume from PodPreset OR Pod spec
└── Multiple PodPresets:
    ├── All matching PodPresets are applied
    └── Apply order: alphabetical by name

```

## Code Examples

### 1. Basic PodPreset — Env Injection

```yaml
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: proxy-config
  namespace: default
spec:
  selector:
    matchLabels:
      app: web
  # Inject proxy settings into all pods with label app=web
  env:
  - name: HTTP_PROXY
    value: "http://proxy.example.com:8080"
  - name: HTTPS_PROXY
    value: "http://proxy.example.com:8080"
  - name: NO_PROXY
    value: "localhost,127.0.0.1,.cluster.local"
```

### 2. PodPreset — Secret Injection

```yaml
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: db-credentials
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  envFrom:
  - secretRef:
      name: database-credentials  # Must exist in namespace
  env:
  - name: DB_CONNECTION_STRING
    valueFrom:
      secretKeyRef:
        name: database-credentials
        key: connection-string
```

### 3. PodPreset — Volume Mount Injection

```yaml
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: shared-certs
  namespace: default
spec:
  selector:
    matchLabels:
      app: api
  volumes:
  - name: ca-certs
    configMap:
      name: ca-certificates
      defaultMode: 0444
  volumeMounts:
  - name: ca-certs
    mountPath: /etc/ssl/certs/ca-certs.crt
    subPath: ca-certs.crt
    readOnly: true
  - name: ca-certs
    mountPath: /usr/local/share/ca-certificates/
    readOnly: true
```

### 4. PodPreset — Multiple Injections

```yaml
# PodPreset 1: Logging sidecar config
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: logging-config
  namespace: default
spec:
  selector:
    matchLabels:
      tier: backend
  env:
  - name: LOG_FORMAT
    value: "json"
  - name: LOG_LEVEL
    value: "info"
  - name: LOG_OUTPUT
    value: "stdout"
---
# PodPreset 2: Monitoring configuration
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: monitoring-config
  namespace: default
spec:
  selector:
    matchLabels:
      app: api
  env:
  - name: METRICS_ENABLED
    value: "true"
  - name: METRICS_PORT
    value: "9090"
  envFrom:
  - configMapRef:
      name: monitoring-config
---
# Pod: matches BOTH PodPresets (has tier=backend AND app=api)
apiVersion: v1
kind: Pod
metadata:
  name: api-pod
  labels:
    app: api       # Matches monitoring-config
    tier: backend  # Matches logging-config
spec:
  containers:
  - name: api
    image: my-api:latest
# Result: Gets env vars from BOTH PodPresets
```

### 5. PodPreset with ConfigMap

```yaml
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: app-settings
  namespace: default
spec:
  selector:
    matchLabels:
      run: my-app
  envFrom:
  - configMapRef:
      name: app-config
  env:
  - name: NODE_ENV
    value: "production"
  - name: POD_NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace
```

### 6. Enable PodPresets in Cluster

```yaml
# kube-apiserver configuration (--enable-admission-plugins flag)
# File: /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --enable-admission-plugins=PodPreset,NamespaceLifecycle
    # Other flags...
```

```bash
# Verify PodPresets are enabled
kubectl api-resources | grep podpreset

# Expected output:
# podpresets  settings.k8s.io/v1alpha1  true  PodPreset
```

### 7. View Injected Configuration

```bash
# Create PodPreset
kubectl apply -f proxy-config.yaml

# Create a matching pod
kubectl run test-pod --image=nginx --labels="app=web"

# Check the pod spec (note: annotations show injection)
kubectl get pod test-pod -o yaml | grep -A5 podpreset
#   podpreset.admission.kubernetes.io/podpreset-proxy-config: "Resource Version"

# View full injected env vars
kubectl exec test-pod -- env | grep -E "PROXY|HTTP"
# HTTP_PROXY=http://proxy.example.com:8080
# HTTPS_PROXY=http://proxy.example.com:8080
# NO_PROXY=localhost,127.0.0.1,.cluster.local

# Check pod annotations
kubectl get pod test-pod -o jsonpath='{.metadata.annotations}' | jq .
```

### 8. Testing PodPreset Selection

```yaml
# Pod that DOES NOT match — no injection
apiVersion: v1
kind: Pod
metadata:
  name: no-preset-pod
  labels:
    app: worker  # Does NOT match any PodPreset selector
spec:
  containers:
  - name: worker
    image: my-worker:latest
# Result: NO env vars injected
```

### 9. Alternative: MutatingAdmissionWebhook (Production)

```yaml
# For production use, use MutatingAdmissionWebhook instead of PodPreset
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingAdmissionWebhookConfiguration
metadata:
  name: pod-config-injector
webhooks:
- name: injector.example.com
  clientConfig:
    service:
      name: webhook-service
      namespace: default
      path: /mutate
    caBundle: <base64-ca-cert>
  rules:
  - operations: ["CREATE"]
    apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
  admissionReviewVersions: ["v1"]
  sideEffects: None
```

### 10. Kyverno Alternative (Production)

```yaml
# Kyverno policy — production-grade alternative to PodPresets
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-proxy-env
spec:
  rules:
  - name: inject-proxy
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - name: "*"
            env:
            - name: HTTP_PROXY
              value: "http://proxy.example.com:8080"
            - name: HTTPS_PROXY
              value: "http://proxy.example.com:8080"
```

## Real-World Use Cases

| Use Case | Injection | Target |
|----------|-----------|--------|
| **Corp proxy** | HTTP_PROXY, HTTPS_PROXY, NO_PROXY | All pods in namespace |
| **Service mesh** | Sidecar injection annotations, mTLS certs | Pods with mesh label |
| **Monitoring** | METRICS_ENABLED, OTEL_EXPORTER env vars | Backend pods |
| **Logging** | Log format, output destination, log level | All application pods |
| **Tracing** | JAEGER_AGENT_HOST, OTEL_SERVICE_NAME | API/microservice pods |
| **Security** | Scanner agent, sysdig agent config | All pods |
| **Time zone** | TZ env var, /etc/localtime volume mount | All pods |
| **CA certs** | CA certificate volumes | Pods making external TLS calls |

## Common Mistakes

### 1. PodPreset Not Enabled

```bash
# ❌ BAD: Assuming PodPresets work out of the box
kubectl apply -f podpreset.yaml
# podpreset created

# But pods don't get injected!
kubectl get pod test-pod -o yaml | grep podpreset
# (nothing)

# ✅ GOOD: Verify PodPreset admission controller is enabled
kubectl api-resources | grep podpreset
# podpresets  settings.k8s.io/v1alpha1
```

### 2. Label Selector Mismatch

```yaml
# ❌ BAD: PodPreset uses wrong selector
spec:
  selector:
    matchLabels:
      app: api
---
# Pod has different label
metadata:
  labels:
    app: backend  # Won't match!
    tier: api     # Wrong key!

# ✅ GOOD: Match labels exactly
spec:
  selector:
    matchLabels:
      app: api
---
metadata:
  labels:
    app: api      # Match!
```

### 3. Overwriting Existing Env Vars

```yaml
# ❌ BAD: PodPreset overwrites existing env var
# Pod specifies:
env:
- name: LOG_LEVEL
  value: "debug"  # Dev wants debug
---
# PodPreset overwrites to:
env:
- name: LOG_LEVEL
  value: "info"   # Platform team says info

# PodPreset's value wins! Dev's LOG_LEVEL=debug is overwritten.

# ✅ GOOD: Document PodPreset injection behavior
# Or use admission webhooks with merge policies
```

### 4. Not Testing Injection

```bash
# ❌ BAD: Deploying PodPreset without testing
kubectl apply -f podpreset.yaml
kubectl run test --image=nginx --labels="app=web"
kubectl exec test -- env  # Check if vars injected

# ✅ GOOD: Test before relying on it
kubectl describe podpreset proxy-config
kubectl get pod test -o yaml | grep -A10 podpreset
```

## Best Practices

1. **Use descriptive names** — PodPreset names should describe what they inject (`proxy-config`, `logging-settings`)
2. **Document injection behavior** — Team members need to know what gets injected
3. **Test thoroughly** — Verify injection works before relying on it
4. **Consider alternatives** — For production, use Kyverno, OPA/Gatekeeper, or admission webhooks
5. **Limit namespace scope** — Apply PodPresets to specific namespaces
6. **Avoid conflicts** — Don't create multiple PodPresets that set the same env vars
7. **Monitor admission controller** — Track PodPreset injection success/failure
8. **Use label conventions** — Standardize labels that trigger PodPreset injection
9. **Version control PodPresets** — Store in Git with other infrastructure config
10. **Plan for alpha limitations** — PodPresets are alpha; have a migration path

## PodPreset vs Alternatives

| Feature | PodPreset | MutatingWebhook | Kyverno | OPA/Gatekeeper |
|---------|:---------:|:---------------:|:-------:|:--------------:|
| Status | Alpha | GA | GA (external) | GA (external) |
| Setup | Admission flag | Webhook service | DaemonSet | Webhook service |
| Complexity | Low | High | Medium | High |
| Flexibility | Limited | Full | Full | Full |
| Policy as code | ❌ | Custom | ✅ DSL | ✅ Rego |
| Dry run | ❌ | ✅ | ✅ | ✅ |
| Performance | Built-in | External call | External | External |

## Summary

- PodPresets inject configuration (env vars, volumes, mounts) into pods at admission time via label matching
- Alpha feature — not enabled by default; requires `--enable-admission-plugins=PodPreset` on API server
- Multiple PodPresets can match a single pod; they are merged alphabetically by name
- PodPreset values overwrite existing pod spec values (env vars with same key)
- For production, use Kyverno, OPA/Gatekeeper, or MutatingAdmissionWebhook instead

## Cheat Sheet

```yaml
# Basic PodPreset
apiVersion: settings.k8s.io/v1alpha1
kind: PodPreset
metadata:
  name: my-preset
spec:
  selector:
    matchLabels:
      app: my-app
  env:
  - name: MY_VAR
    value: "my-value"
  envFrom:
  - configMapRef:
      name: my-config
  volumes:
  - name: my-volume
    emptyDir: {}
  volumeMounts:
  - name: my-volume
    mountPath: /data
```

```bash
# Enable
--enable-admission-plugins=PodPreset

# Verify
kubectl api-resources | grep podpreset

# Create
kubectl apply -f podpreset.yaml

# Check injection
kubectl get pod <name> -o yaml | grep podpreset
kubectl describe pod <name> | grep -A5 "Annotations"

# Test dry run
kubectl run test --image=nginx --labels="app=my-app" --dry-run=server -o yaml
```

```text
PodPreset Key Points:
├── Injects: Env vars, volumes, volume mounts
├── Selector: matchLabels on pod labels
├── State: Alpha (K8s 1.6+)
├── Not enabled by default
├── Conflicts: PodPreset values OVERWRITE pod spec values
├── Multiple: Applied alphabetically by name
├── Check: kubectl get podpreset
├── Limit: Single namespace only
└── Production alternative: MutatingAdmissionWebhook, Kyverno
```

---

## See Also

- [ConfigMaps & Secrets](04-ConfigMaps-Secrets.md)
- [Deployments](02-Deployments.md)
- [Health Checks](06-Health-Checks.md)
- [Helm](07-Helm.md)
- [Interview Questions](08-Interview-Questions.md)
- [Pods & ReplicaSets](01-Pods-ReplicaSets.md)
- [RBAC & Network Policies](11-RBAC-Network-Policies.md)

## References & Learn More

- [K8s PodPreset Docs](https://kubernetes.io/docs/concepts/workloads/pods/podpreset/)
- [K8s Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
- [Kyverno Docs](https://kyverno.io/docs/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/)
- [Mutating Admission Webhook Example](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/)
