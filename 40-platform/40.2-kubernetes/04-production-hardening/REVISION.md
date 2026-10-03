<!-- section: Kubernetes | category: Reference | tags: revision, practi | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Kubernetes-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Kubernetes — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Kubernetes Health Checks

Source: [Kubernetes Health Checks](40.2.4.01-health-checks.md)

**Q:** Which probe should keep a slow-starting process from premature restarts?

**A:** A startup probe. Once it succeeds, readiness controls traffic eligibility and liveness can detect a stuck process; dependency failure should not automatically restart every replica.

## Pod Disruption Budgets

Source: [Pod Disruption Budgets](40.2.4.02-pod-disruption-budgets.md)

**Q:** Does a PodDisruptionBudget control a Deployment's rolling update?

**A:** No. It constrains voluntary evictions through the eviction API. Deployment rollout availability is controlled by the workload's rollout strategy.

## RBAC & Network Policies

Source: [RBAC & Network Policies](40.2.4.03-rbac-network-policies.md)

**Q:** Why can a NetworkPolicy manifest have no effect?

**A:** The cluster's network implementation must enforce NetworkPolicy. The object's existence alone does not prove data-plane isolation.

**Q:** What is the difference between RBAC and NetworkPolicy?

**A:** RBAC authorizes Kubernetes API operations; NetworkPolicy constrains supported network traffic paths. Permission to read a Secret and permission to connect to a service are different boundaries.

## Resource Quotas

Source: [Resource Quotas](40.2.4.04-resource-quotas.md)

**Q:** Why does an admitted resource quota not reserve useful service capacity?

**A:** Quotas cap namespace requests/counts. Scheduling capacity, per-container limits, placement, and the workload's performance still require separate policies.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
