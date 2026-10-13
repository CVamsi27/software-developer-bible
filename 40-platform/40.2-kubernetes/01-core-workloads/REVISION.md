<!-- section: Kubernetes | category: Reference | tags: revision, practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Kubernetes-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Kubernetes — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Kubernetes Pods & ReplicaSets

Source: [Kubernetes Pods & ReplicaSets](40.2.1.01-pods-replicasets.md)

**Q:** A Pod disappears: what recreates it, and what does not?

**A:** A controller such as a ReplicaSet reconciles the requested replica count. A bare Pod has no such workload controller, and replacement does not preserve its process memory.

**Q:** A container crashes while its Pod remains assigned to a healthy node. What changes compared with deleting the Pod?

**A:** The kubelet can restart the container in that same Pod under its restart policy. Deleting a managed Pod instead prompts a workload controller to create a replacement with a new object identity; its process memory is not restored.

**Q:** How does a native sidecar differ from an ordinary init container?

**A:** An ordinary init container must finish before application containers start. A native sidecar is declared as an init container with `restartPolicy: Always`, starts before the application, and continues alongside it; the feature is stable since Kubernetes 1.33.

## Kubernetes Deployments

Source: [Kubernetes Deployments](40.2.1.02-deployments.md)

**Q:** Why can maxUnavailable zero still produce a bad release?

**A:** It constrains rollout availability according to Pod readiness. Incorrect probes, dependency overload, insufficient surge capacity, or application incompatibility can still affect users.

**Q:** A Deployment reports `ProgressDeadlineExceeded`. Has Kubernetes already restored the previous version?

**A:** No. The condition exposes stalled progress; the Deployment controller continues reconciliation. A release controller, pipeline, or operator must choose rollback or repair, and must verify schema and interface compatibility before restoring an older template.

**Q:** Why can a zero-unavailability rollout stall when the old version is healthy?

**A:** The next surge Pod needs quota admission, schedulable capacity, startup, and availability. If any step fails, keeping old capacity is consistent with the policy but prevents progress. Inspect each state rather than treating desired replicas as ready capacity.

**Q:** Nine stable Pods and one canary Pod share a Service. Is exactly 10% of requests guaranteed to hit canary?

**A:** No. Connections, readiness, affinity, and data-plane behavior affect distribution. The two Deployments do not route traffic by themselves; precise traffic fractions need an appropriate routing mechanism.

## StatefulSets & DaemonSets

Source: [StatefulSets & DaemonSets](40.2.1.03-statefulsets-daemonsets.md)

**Q:** What identity does a StatefulSet preserve across replacement?

**A:** A stable ordinal/name and associated storage identity. It does not make application replication, backup, or consistency automatic.

**Q:** What changes when a StatefulSet has Parallel management or an explicit PVC retention policy?

**A:** Parallel changes scale-operation sequencing, not RollingUpdate's update rules. Default PVC retention can be changed by the supported explicit retention policy; inspect it before assuming scale-down keeps or deletes data.

**Q:** Does one desired DaemonSet Pod per node guarantee one healthy agent at every instant?

**A:** No. Placement/startup failures can leave a node uncovered, and surge updates can briefly run two versions. Observe actual per-node readiness and update behavior.

## Jobs & CronJobs

Source: [Jobs & CronJobs](40.2.1.04-jobs-cronjobs.md)

**Q:** Why should a Job handler tolerate duplicate execution?

**A:** Controller retries and infrastructure failures can repeat work. Persist an idempotency decision with the business operation rather than assuming one Pod equals exactly one effect.

**Q:** Does Forbid on a CronJob provide exactly-once scheduling?

**A:** No. It prevents overlapping Jobs from that CronJob according to its policy; delayed/missed schedules and repeated work still require application-level handling.

**Q:** A Job writes its output then crashes before successful exit. What must a replacement attempt assume?

**A:** The prior business effect may already exist although Kubernetes recorded a failed attempt. Reuse a durable idempotency/index decision or otherwise make the effect safe to repeat; completion accounting is not a transaction over external data.

**Q:** One shard in an Indexed Job repeatedly fails while other indexes are useful. How can the controller stop retrying that shard without immediately canceling its siblings?

**A:** Use an Indexed Job with `backoffLimitPerIndex` and a `podFailurePolicy` rule with `FailIndex` for the relevant failure; `podFailurePolicy` requires `restartPolicy: Never`. Kubernetes marks that index failed and stops retrying it while other indexes continue. The Job fails after indexed completion if any index failed, or sooner if failed indexes exceed `maxFailedIndexes`; external effects must still be safe to retry.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
