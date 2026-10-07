<!-- section: Kubernetes | category: Reference | tags: revision, practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Kubernetes-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Kubernetes — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Kubernetes Services & Ingress

Source: [Kubernetes Services & Ingress](40.2.2.01-services-ingress.md)

**Q:** How is an Ingress object different from a running ingress controller?

**A:** The object declares routing rules; a controller watches those rules and configures an actual data plane. Without a matching controller the declaration cannot route traffic.

**Q:** Does a Service route directly to a durable Pod identity?

**A:** It selects eligible endpoints; Pods are replaceable. Stable service discovery is separate from application session persistence and storage.

## Kubernetes ConfigMaps & Secrets

Source: [Kubernetes ConfigMaps & Secrets](40.2.2.02-configmaps-secrets.md)

**Q:** Why is a Secret's base64 value not a security boundary?

**A:** Base64 is encoding. Protect access with RBAC, encrypt stored data where required, control mounts/logging, and avoid committing plaintext or encoded secret material.

**Q:** Will editing a ConfigMap always reconfigure the application?

**A:** No. Mounted updates and environment-variable injection have different behavior, and the application may need a reload or Pod restart to observe the new value.

## PodPresets

Source: [PodPresets](40.2.2.03-podpresets.md)

**Q:** What should replace reliance on a removed PodPreset API?

**A:** Use supported workload templates, Helm/Kustomize composition, or a deliberately configured admission mechanism; verify the cluster version and avoid removed API manifests.

**Q:** Did the ingress-nginx retirement remove Kubernetes Ingress or every NGINX-based controller?

**A:** No. The community ingress-nginx controller retired in March 2026 and no longer receives fixes or security updates. Ingress remains an API, and other products have separate lifecycles. Select a maintained implementation and test policy translation during migration.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
