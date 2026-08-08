---
section: CI/CD
category: DevOps
tags: [concept]
---

# ArgoCD (GitOps)

## TL;DR

Pull-based GitOps controller that syncs Kubernetes cluster state to a Git repository with drift detection and self-heal.

**Why it matters:** De-facto GitOps for K8s. Tests Application vs ApplicationSet, sync waves, sync policies, and how it coexists with image-updater bots.

## Definition

**ArgoCD** is a declarative, GitOps continuous delivery tool for Kubernetes. It automates application deployment and lifecycle management by synchronizing a Git repository's desired state with the actual cluster state. Applications, configurations, and environments are all defined in Git, with ArgoCD ensuring the cluster matches the repository.

## Why Do We Need It?

1. **Git as single source of truth**: Cluster state is version-controlled in Git
2. **Automated sync**: Cluster automatically matches Git state
3. **Self-healing**: Manual changes to cluster are reverted to Git state
4. **Multi-cluster**: Manage deployments across many clusters from one ArgoCD
5. **Visual UI**: Application topology, sync status, and rollback history
6. **Pull-based deployment**: Cluster pulls from Git, not CI pushing to cluster

## How It Works

```text
┌─────────────────────────────────────────────────────────────┐
│                    ARGOCD ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Developer pushes to Git                                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────┐       ┌──────────────────┐               │
│  │ Git Repository│◄─────│  ArgoCD Server   │               │
│  │ (desired      │       │  (polls every 3m)│               │
│  │  state)       │       └────────┬─────────┘               │
│  └──────────────┘                │                          │
│                                  │ syncs                    │
│                                  ▼                          │
│                          ┌──────────────────┐              │
│                          │ Kubernetes       │              │
│                          │ Cluster(s)       │              │
│                          │ (actual state)   │              │
│                          └──────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Application Definition

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/my-app.git
    targetRevision: main
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### ApplicationSet (Multi-Environment)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-app-environments
spec:
  generators:
    - list:
        elements:
          - env: dev
            namespace: dev
            cluster: https://kubernetes.default.svc
          - env: staging
            namespace: staging
            cluster: https://kubernetes.default.svc
          - env: prod
            namespace: prod
            cluster: https://prod-cluster.example.com
  template:
    metadata:
      name: 'my-app-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/my-app.git
        targetRevision: main
        path: 'k8s/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          selfHeal: true
```

### Rollback

```bash
# View sync history
argocd app get my-app

# Rollback to previous version
argocd app rollback my-app --prune

# Rollback to specific revision
argocd app rollback my-app 3

# Rollback via UI
# Application → History & Rollback → Select revision → Rollback
```

## Best Practices

1. **One Application per app/environment** combination
2. **Use Kustomize or Helm** for environment-specific overlays
3. **Enable auto-sync** with `selfHeal` and `prune` for production
4. **Set resource limits** via `syncPolicy.retry`
5. **Use ApplicationSets** for multi-environment deployments
6. **Separate ArgoCD config** from application config in Git
7. **Configure notifications** for sync failures (Slack, email)

## Summary

- ArgoCD is a GitOps tool that synchronizes Kubernetes cluster state with Git repositories
- Applications are defined declaratively in Git and ArgoCD automatically reconciles drift
- Sync strategies include automated sync with prun, manual sync, and sync waves for ordered deployments
- SSO integration (OIDC, Dex) provides role-based access for multi-team environments
- Health checks, rollback capabilities, and sync hooks provide deployment safety guarantees

---

## Cheat Sheet
```text
ARGOCD (GITOPS) CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```

---

## See Also
- [Blue-Green & Canary](03-Blue-Green-Canary.md)
- [Docker](../13-Docker/)

## References & Learn More

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [GitOps Principles](https://www.gitops.tech/)
