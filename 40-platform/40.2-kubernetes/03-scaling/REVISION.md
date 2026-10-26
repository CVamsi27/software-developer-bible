<!-- section: Kubernetes | category: Reference | tags: revision, practice | role-priority: optional | general-importance: specialized -->
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

**Q:** Four replicas average 80% CPU against a 50% target. What does the basic HPA ratio recommend before controller adjustments?

**A:** `ceil(4 × 80 / 50) = 7` replicas. Current consumption belongs in the numerator: demand above target increases capacity. Missing metrics, readiness, tolerance, stabilization, and configured policies can modify the actual decision.

**Q:** Three Pods each request `500m` and use `400m`. With a 50% CPU target, trace the recommendation and the steps before new replicas serve traffic.

**A:** Utilization is 80%, so the basic recommendation is `ceil(3 × 80 / 50) = 5`. HPA writes the scale target; Deployment/ReplicaSet reconciliation creates Pods, scheduling finds nodes, kubelets start containers, and readiness admits them to ordinary Service traffic. Five desired replicas can still mean only three ready replicas.

**Q:** What changes if each CPU request doubles while measured use stays the same?

**A:** Utilization falls from 80% to 40%; the basic recommendation becomes `ceil(3 × 40 / 50) = 3`. No physical demand disappeared. The changed denominator affects HPA while the larger request also makes placement harder.

**Q:** One HPA metric fails while another recommends fewer replicas. Can the healthy metric alone trigger downscale?

**A:** The controller skips that downscale rather than assuming the missing signal is safe. A usable metric recommending scale-up can still cause an increase. Missing data changes the decision, not just the displayed metric.

**Q:** Which HPA metrics can scale a workload from zero in Kubernetes v1.37, and what makes that state different from manually pausing a workload?

**A:** At least one object or external metric is required; CPU and memory resource metrics cannot wake a workload without Pods. The HPA marks its own scale-to-zero state with `ScaledToZero=True`. A durable queue can retain work while workers start, but a Service does not buffer HTTP requests for a zero-replica target.

**Q:** Does a 10% HPA downscale policy remove no Pods when only three replicas remain?

**A:** No. The removal allowance rounds up to a whole Pod, so one can be removed if the recommendation, minimum count and other rules allow it. A percentage policy is not fractional-Pod precision.

**Q:** Will an HPA with minReplicas zero wake a Deployment that was initialized with zero replicas?

**A:** Not without its HPA-owned `ScaledToZero=True` state. Start with at least one replica so the controller can own a later transition to zero; manual zero remains a pause.

## Node Autoscaling & Cluster Capacity (Cluster Autoscaler, Karpenter)

Source: [Node Autoscaling & Cluster Capacity (Cluster Autoscaler, Karpenter)](40.2.3.02-node-autoscaling-cluster-capacity.md)

**Q:** Why can adding Pods make no progress even with an HPA?

**A:** If no nodes can satisfy their resource/placement requests, Pods remain pending. Node provisioning, quotas, capacity, and startup delays are separate constraints.

**Q:** What do requests tell a node provisioner that usage does not?

**A:** Requests describe schedulable commitments. Low observed usage cannot justify placing workloads whose declared requests do not fit the node.

**Q:** Why must consolidation respect placement and disruption constraints?

**A:** Evicting workloads only helps if replacement capacity can schedule them and disruption remains acceptable; PDBs, topology, storage, and warm-up can prevent safe movement.

**Q:** Why can a `1500m` Pod remain unschedulable when two allowed nodes each have one CPU left?

**A:** Requests must fit on one feasible node; aggregate free CPU across machines is not one schedulable slot. A provisioner needs a permitted node shape with enough capacity and matching placement constraints.

**Q:** Does tolerating the GPU pool's taint allocate a GPU or guarantee placement in that pool?

**A:** It only permits the taint. A selector or affinity chooses the pool, and a device resource request allocates an exposed GPU. The provider's device plugin must first make that resource available.

**Q:** Why does a device-plugin GPU request need a matching limit?

**A:** Kubernetes does not allow a GPU request without its limit. Limits alone default the request; when both are written they must be equal. Pool tolerations and labels do not satisfy that resource contract.

**Q:** Does an expiration event guarantee Karpenter immediately finishes deleting a node with protected Pods?

**A:** No. Selection for disruption and completing drain are separate. A do-not-disrupt Pod can block expiration/manual termination without a NodeClaim grace deadline; when a configured deadline expires, forced deletion can interrupt the application.

**Q:** Why might a low-priority headroom buffer fail to refill after application Pods preempt it?

**A:** The autoscaler's configured expendable-priority cutoff can exclude the replacement placeholders from scale-up demand. Verify the priority configuration and actual Pending events; preemption alone does not prove refill works.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
