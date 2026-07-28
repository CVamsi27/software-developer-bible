[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

# Kubernetes Helm

## Definition

**Helm** is the package manager for Kubernetes. It packages Kubernetes manifests into reusable units called **charts**, manages releases, and enables templating and configuration management. Helm simplifies deployment, updates, and rollbacks of complex applications.

Key concepts:

- **Chart**: A package of Kubernetes resources (like apt/yum packages)
- **Release**: A running instance of a chart with specific configuration
- **Values**: Configuration parameters for a chart
- **Repository**: Collection of charts (like Docker Hub for charts)
- **Template**: Go templating engine for dynamic manifest generation

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Complex YAML manifests | Charts package multiple resources |
| No configuration management | Values files for customization |
| No release management | Helm tracks release history |
| No rollback capability | Helm manages rollbacks |
| No versioning | Charts have semantic versions |
| Duplication across environments | Reusable charts with different values |

## How It Works

### Helm Architecture

```text
+----------------------------------------------------------+

|                      Helm CLI                             |
|  helm install, upgrade, rollback, list, etc.             |

+----------------------------------------------------------+

                          |

                          v
+----------------------------------------------------------+

|                    Chart Repository                       |
|  +----------+  +----------+  +----------+               |
|  |  nginx   |  |  myapp   |  | postgres |               |
|  |  v1.0.0  |  |  v2.0.0  |  |  v15.0  |               |
|  +----------+  +----------+  +----------+               |

+----------------------------------------------------------+

                          |

                          v
+----------------------------------------------------------+

|                    Kubernetes Cluster                      |
|  +--------------------------------------------------+   |
|  |                    Release: myapp-prod            |   |
|  |  Chart: myapp                                     |   |
|  |  Values: values-prod.yaml                          |   |
|  |  Resources:                                        |   |
|  |    - Deployment                                    |   |
|  |    - Service                                       |   |
|  |    - ConfigMap                                     |   |
|  |    - Secret                                        |   |
|  +--------------------------------------------------+   |

+----------------------------------------------------------+

```

### Chart Structure

```text
mychart/
+-- Chart.yaml          # Chart metadata
+-- Chart.lock          # Dependency lock file
+-- values.yaml         # Default configuration values
+-- values.schema.json  # JSON Schema for values
+-- templates/          # Kubernetes manifest templates

|   +-- deployment.yaml
|   +-- service.yaml
|   +-- configmap.yaml
|   +-- ingress.yaml
|   +-- hpa.yaml
|   +-- _helpers.tpl    # Template helpers
|   +-- NOTES.txt       # Post-install notes
+-- charts/             # Sub-charts (dependencies)
+-- crds/               # Custom Resource Definitions

```

## Code Examples

### Basic Chart

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: My application Helm chart
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:

  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

```

### Values File

```yaml
# values.yaml
replicaCount: 3

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:

    - host: myapp.example.com
      paths:

        - path: /
          pathType: Prefix
  tls:

    - secretName: myapp-tls
      hosts:

        - myapp.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

postgresql:
  enabled: true
  auth:
    postgresPassword: "secret"
    database: "myapp"

```

### Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:

        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:

            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            periodSeconds: 10
          resources:
            {{- toYaml .Values.resources | nindent 12 }}

```

### Service Template

```yaml
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:

    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    {{- include "mychart.selectorLabels" . | nindent 4 }}

```

### Ingress Template

```yaml
# templates/ingress.yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  ingressClassName: {{ .Values.ingress.className }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}

    - hosts:
        {{- range .hosts }}

        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}

    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}

          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "mychart.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}

```

### Helper Templates

```yaml
# templates/_helpers.tpl
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
app.kubernetes.io/version: {{ .Values.image.tag | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

```

### Helm Commands

```bash
# Install chart
helm install myrelease ./mychart -f values-prod.yaml

# Upgrade release
helm upgrade myrelease ./mychart -f values-prod.yaml

# Rollback release
helm rollback myrelease 1

# List releases
helm list -A

# Uninstall release
helm uninstall myrelease

# Search charts
helm search repo nginx

# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update repositories
helm repo update

# Show chart info
helm show chart mychart
helm show values mychart

```

### Environment-Specific Values

```yaml
# values-dev.yaml
replicaCount: 1
resources:
  limits:
    cpu: 250m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
autoscaling:
  enabled: false

# values-prod.yaml
replicaCount: 5
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi
autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 20

```

## Real-World Use Cases

### 1. Complete Application Stack

```bash
# Install with dependencies
helm install myapp ./mychart \
  -f values-prod.yaml \
  --set image.tag=2.0.0 \
  --set postgresql.auth.password=secret \
  --namespace production \
  --create-namespace

```

### 2. CI/CD Integration

```yaml
# .github/workflows/deploy.yml

- name: Deploy to Kubernetes
  run: |
    helm upgrade --install myapp ./chart \
      -f values-${{ env.ENVIRONMENT }}.yaml \
      --set image.tag=${{ github.sha }} \
      --wait --timeout 300s

```

### 3. Chart Testing

```bash
# Lint chart
helm lint ./mychart

# Template rendering
helm template myrelease ./mychart -f values-prod.yaml

# Dry run
helm install myrelease ./mychart --dry-run --debug

# Test release
helm test myrelease

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Hardcoding values | Use values files |
| No chart versioning | Follow semantic versioning |
| Missing templates | Use helm create for boilerplate |
| No dependency management | Use Chart.yaml dependencies |
| No release naming | Use descriptive release names |
| No rollback strategy | Test helm rollback |
| Not using --wait | Use --wait for deployment completion |

## Best Practices

```yaml
# GOOD: Production-ready chart
apiVersion: v2
name: myapp
description: Production application chart
type: application
version: 1.0.0
appVersion: "1.0.0"

dependencies:

  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

```

1. **Use semantic versioning** — follow semver for chart versions

2. **Template everything** — avoid hardcoding in manifests

3. **Use helpers** — create reusable template functions

4. **Validate with lint** — `helm lint` before deployment

5. **Test with dry-run** — `helm install --dry-run --debug`

6. **Use values files** — separate configuration from templates

7. **Manage dependencies** — use Chart.yaml dependencies

8. **Document with NOTES.txt** — provide post-install instructions

9. **Use namespaces** — isolate releases
10. **Monitor releases** — use helm list and helm status

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Chart complexity | Deployment time | Simplify templates |
| Resource requests | Scheduling | Set accurate requests |
| Release history | Storage | Limit --history-max |
| Template rendering | CPU usage | Cache rendered templates |
| Dependency downloads | Network | Use local chart dependencies |

```bash
# Optimize deployment
helm upgrade --install myrelease ./mychart \
  --wait --timeout 300s \
  --atomic

# Limit release history
helm upgrade --install myrelease ./mychart \
  --history-max 5

# Use values file
helm install myrelease ./mychart -f values-prod.yaml

```

## Summary

Helm simplifies Kubernetes application management through charts, templating, and release management. It enables versioned deployments, rollbacks, and configuration management. Essential for managing complex applications in production.

## Cheat Sheet
```bash
# Install
helm install myrelease ./mychart -f values.yaml

# Upgrade
helm upgrade myrelease ./mychart -f values.yaml

# Rollback
helm rollback myrelease 1

# List
helm list -A

# Uninstall
helm uninstall myrelease

# Template
helm template myrelease ./mychart -f values.yaml

# Lint
helm lint ./mychart

# Repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search
helm search repo nginx

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
