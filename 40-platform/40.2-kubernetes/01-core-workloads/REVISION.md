<!-- section: Kubernetes | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Kubernetes-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Kubernetes — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Kubernetes Pods & ReplicaSets

Source: [Kubernetes Pods & ReplicaSets](40.2.1.01-pods-replicasets.md)

**Q:** A Pod disappears: what recreates it, and what does not?

**A:** A controller such as a ReplicaSet reconciles the requested replica count. A bare Pod has no such workload controller, and replacement does not preserve its process memory.

## Kubernetes Deployments

Source: [Kubernetes Deployments](40.2.1.02-deployments.md)

**Q:** Why can maxUnavailable zero still produce a bad release?

**A:** It constrains rollout availability according to Pod readiness. Incorrect probes, dependency overload, insufficient surge capacity, or application incompatibility can still affect users.

## StatefulSets & DaemonSets

Source: [StatefulSets & DaemonSets](40.2.1.03-statefulsets-daemonsets.md)

**Q:** What identity does a StatefulSet preserve across replacement?

**A:** A stable ordinal/name and associated storage identity. It does not make application replication, backup, or consistency automatic.

## Jobs & CronJobs

Source: [Jobs & CronJobs](40.2.1.04-jobs-cronjobs.md)

**Q:** Why should a Job handler tolerate duplicate execution?

**A:** Controller retries and infrastructure failures can repeat work. Persist an idempotency decision with the business operation rather than assuming one Pod equals exactly one effect.

**Q:** Does Forbid on a CronJob provide exactly-once scheduling?

**A:** No. It prevents overlapping Jobs from that CronJob according to its policy; delayed/missed schedules and repeated work still require application-level handling.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
