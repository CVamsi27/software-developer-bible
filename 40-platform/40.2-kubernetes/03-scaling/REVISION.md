<!-- section: Kubernetes | category: Reference | tags: revision, practice| general-importance: specialized| general-importance: specialized | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Kubernetes-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Kubernetes — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Kubernetes HPA & Scaling

Source: [Kubernetes HPA & Scaling](40.2.3.01-hpa-scaling.md)

**Q:** Why does a CPU utilization target depend on resource requests?

**A:** Utilization compares observed CPU to the requested CPU. Missing or unsuitable requests distort or prevent that metric's scaling decision.

**Q:** Why can an HPA amplify a database incident?

**A:** Additional application replicas can open more connections and issue more requests against an already saturated dependency. Bound downstream concurrency and choose scaling signals carefully.

## Node Autoscaling & Cluster Capacity (Cluster Autoscaler, Karpenter)

Source: [Node Autoscaling & Cluster Capacity (Cluster Autoscaler, Karpenter)](40.2.3.02-node-autoscaling-cluster-capacity.md)

**Q:** Why can adding Pods make no progress even with an HPA?

**A:** If no nodes can satisfy their resource/placement requests, Pods remain pending. Node provisioning, quotas, capacity, and startup delays are separate constraints.

**Q:** What do requests tell a node provisioner that usage does not?

**A:** Requests describe schedulable commitments. Low observed usage cannot justify placing workloads whose declared requests do not fit the node.

**Q:** Why must consolidation respect placement and disruption constraints?

**A:** Evicting workloads only helps if replacement capacity can schedule them and disruption remains acceptable; PDBs, topology, storage, and warm-up can prevent safe movement.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
