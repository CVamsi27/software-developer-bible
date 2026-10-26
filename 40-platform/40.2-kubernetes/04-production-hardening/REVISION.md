<!-- section: Kubernetes | category: Reference | tags: revision, practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Kubernetes-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Kubernetes — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Kubernetes Health Checks

Source: [Kubernetes Health Checks](40.2.4.01-health-checks.md)

**Q:** Which probe should keep a slow-starting process from premature restarts?

**A:** A startup probe. Once it succeeds, readiness controls traffic eligibility and liveness can detect a stuck process; dependency failure should not automatically restart every replica.

**Q:** After startup succeeds, does readiness wait for a successful liveness probe?

**A:** No. They run independently. Failed readiness withdraws ordinary Service eligibility without restarting; failed liveness past its threshold stops the container. Existing traffic and direct Pod access need separate handling.

**Q:** What changes when a shared database fails but every API event loop remains responsive?

**A:** If every API request requires that database, readiness can withdraw an affected replica while local liveness stays successful. If the application can serve a useful degraded response, keep it ready and handle the dependency failure in the request path. Making a shared database failure a liveness condition would restart replicas without repairing the cause.

**Q:** Does an HTTPS probe or Kubernetes v1.37's alpha gRPC TLS probe verify the server's certificate?

**A:** No. HTTPS and the gRPC TLS probe encrypt traffic but skip server-certificate verification. The gRPC TLS mode is alpha in v1.37 and disabled by default; neither mode proves server identity.

## Pod Disruption Budgets

Source: [Pod Disruption Budgets](40.2.4.02-pod-disruption-budgets.md)

**Q:** Does a PodDisruptionBudget control a Deployment's rolling update?

**A:** No. It constrains voluntary evictions through the eviction API. Deployment rollout availability is controlled by the workload's rollout strategy.

**Q:** With three healthy replicas and `maxUnavailable: 1`, why is the second healthy eviction rejected after the first?

**A:** The desired healthy threshold is two, and the first accepted disruption consumes the available allowance. Replacement intent is not replacement readiness. Wait for healthy capacity to return.

**Q:** What does `selector: {}` select in a `policy/v1` PodDisruptionBudget, and when can you use `maxUnavailable`?

**A:** An empty selector matches every Pod in the namespace, so use explicit labels and check the PDB status. `maxUnavailable` needs one supported managing controller for the selected Pods; for arbitrary or bare Pods, use an integer `minAvailable`.

## RBAC & Network Policies

Source: [RBAC & Network Policies](40.2.4.03-rbac-network-policies.md)

**Q:** Why can a NetworkPolicy manifest have no effect?

**A:** The cluster's network implementation must enforce NetworkPolicy. The object's existence alone does not prove data-plane isolation.

**Q:** If no RBAC rule matches a request, does that alone prove the API server rejects it?

**A:** No. The RBAC authorizer returns no opinion when no rule matches, so another configured authorizer may decide the request. A conclusive allow or deny decides it; if every authorizer returns no opinion, the API server denies it.

**Q:** What is the difference between RBAC and NetworkPolicy?

**A:** RBAC authorizes Kubernetes API operations; NetworkPolicy constrains supported network traffic paths. Permission to read a Secret and permission to connect to a service are different boundaries.

**Q:** Why does a Role alone grant no user access, and how does a RoleBinding to a ClusterRole stay namespaced?

**A:** The Role describes permissions; a binding connects them to subjects. A RoleBinding grants the referenced Role or ClusterRole within its own namespace. A ClusterRoleBinding instead grants its ClusterRole cluster-wide.

**Q:** API-to-database egress allows TCP 5432, but a DNS lookup fails. What changed in the connection trace?

**A:** The database connection first needs name resolution. The API's isolated egress also needs the actual DNS path on UDP/TCP 53, and the destination's ingress must permit the database connection. A rule for database traffic does not imply DNS access.

**Q:** Does a default-deny Pod NetworkPolicy quarantine the Pod from its own node?

**A:** No. Standard NetworkPolicy permits traffic to/from the Pod's node and cannot deny self-access; hostNetwork handling is also implementation dependent. A host boundary needs separate controls.

## Resource Quotas

Source: [Resource Quotas](40.2.4.04-resource-quotas.md)

**Q:** Why does an admitted resource quota not reserve useful service capacity?

**A:** Quotas cap namespace requests/counts. Scheduling capacity, per-container limits, placement, and the workload's performance still require separate policies.

**Q:** Trace a container with default CPU request `200m` and limit `500m` through namespace admission and node placement.

**A:** LimitRange supplies defaults, then quota checks the resulting request and limit totals. If admitted, the scheduler still needs a feasible node for the request. Admission does not reserve node capacity or prove readiness.

**Q:** In the per-container resource model, what happens if a CPU-request quota exists but required requests and compatible defaults are absent?

**A:** Admission can reject Pod creation. The workload controller may exist with fewer Pods than desired; inspect its events. This differs from an existing Pending Pod that the scheduler cannot place.

**Q:** Does CPU/memory quota always require explicit fields on every container?

**A:** No. The older per-container check applies to that model, but Kubernetes 1.37 skips it when PodLevelResources is enabled and Pod-level resources are set. Account from the effective Pod declarations and verify the feature support.

**Q:** Why can the node autoscaler do nothing when a quota rejects the fourth requested replica?

**A:** Admission rejected the Pod before it existed, so there is no unschedulable Pod to trigger node provisioning. Fix the namespace budget or workload request first; a Pending Pod indicates a later scheduling-stage problem.

**Q:** A namespace stays below its CPU-request quota. Can its running containers collectively use more CPU than that request total?

**A:** Yes, when node capacity and their runtime limits permit it. Request accounting is not live usage accounting. Quotas restrict declared admission demand; runtime limits and node contention govern actual use.

**Q:** Does a LimitRange minimum of one CPU reserve one CPU for each accepted container?

**A:** No. It constrains the declared allocation. Scheduling still needs a suitable node, and latency depends on the workload and runtime conditions. Adding or changing defaults also does not retroactively resize existing Pods.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
