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

**Q:** Did the ingress-nginx retirement remove Kubernetes Ingress or every NGINX-based controller?

**A:** No. The community ingress-nginx controller retired in March 2026 and no longer receives fixes or security updates. The Ingress API remains stable but frozen, with no planned removal; Kubernetes recommends Gateway API for new routing features. Other controllers have separate lifecycles. Select a maintained implementation and test policy translation during migration.

**Q:** Which port does an Ingress backend name when a Service maps port 80 to targetPort 8080?

**A:** The Service port, 80. Its endpoints eventually receive traffic on 8080; the implementation may route directly to endpoint addresses. A matching route still needs a running controller and ready reachable backends.

## Kubernetes ConfigMaps & Secrets

Source: [Kubernetes ConfigMaps & Secrets](40.2.2.02-configmaps-secrets.md)

**Q:** Why is a Secret's base64 value not a security boundary?

**A:** Base64 is reversible encoding, and Secret objects are unencrypted in etcd by default. Configure encryption at rest and protect its keys and backups. Restrict direct Secret reads and Pod creation because a workload can expose a mounted value; control mounts and logging, and avoid committing plaintext or encoded secret material.

**Q:** Will editing a ConfigMap always reconfigure the application?

**A:** No. Mounted updates and environment-variable injection have different behavior, and the application may need a reload or Pod restart to observe the new value.

**Q:** A mutable ConfigMap changes while one Pod uses env injection and another uses a normal volume. Trace what each process sees.

**A:** The first process keeps its startup environment until replacement/restart. The ordinary mounted file can refresh eventually, but the second process changes its effective setting only if it rereads/reloads it. A subPath mount would not receive the file update.

**Q:** Why can `defaultMode: 0400` break a non-root application even though the Secret exists?

**A:** Mode, owner/group, and Pod security settings determine access. The actual process user needs read permission; verify the mounted file as that user rather than treating a restrictive mode number as sufficient.

## PodPresets

Source: [PodPresets](40.2.2.03-podpresets.md)

**Q:** What should replace reliance on a removed PodPreset API?

**A:** Use supported workload templates, Helm/Kustomize composition, or a deliberately configured admission mechanism; verify the cluster version and avoid removed API manifests.

**Q:** A fail-closed mutating webhook becomes unavailable. What can happen before the new application Pod reaches scheduling?

**A:** Matching admission requests can fail, so the desired workload exists without its requested new Pods. Inspect admission configuration/events and recover the owned policy service; a new node cannot fix rejected creation.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
