<!-- section: Infra Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Infra%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Shipping And Evolution — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Zero-Downtime Deployments — Blue-Green, Canary, Rolling, Feature Flags

Source: [Zero-Downtime Deployments — Blue-Green, Canary, Rolling, Feature Flags](30.3.5.01-zero-downtime-deployments.md)

**Q:** Why must a rollback plan include database compatibility?

**A:** The previous binary may encounter a schema or data format introduced by the new version. Expand/contract changes keep old and new readers/writers compatible during overlap.

**Q:** What should precede a canary percentage increase?

**A:** A defined observation window and checks for errors, latency, saturation and business correctness, with a tested stop/rollback path and compatible data changes.

**Q:** Does maxUnavailable = 0 make every request succeed during a rollout?

**A:** No. It constrains available rollout capacity under readiness rules. Spare scheduling capacity, routing convergence, business correctness and bounded in-flight drain remain separate requirements.

**Q:** What does `ProgressDeadlineExceeded` do when a Kubernetes Deployment stalls?

**A:** It reports stalled progress while the controller keeps reconciling; it does not automatically roll back. A release owner or higher-level controller must decide whether to pause, roll back or repair forward. See the [Kubernetes Deployment documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

**Q:** Why can a one-time old-to-new-column backfill become stale before reader cutover?

**A:** Old writers may keep modifying only the old column. Bridge/upgrade every writer, capture concurrent changes and revalidate meaning before making the new field authoritative.

**Q:** Does switching back to the old fleet undo an accepted payment?

**A:** No. Routing changes future work. Shared schema/data, queued events, client assets and remote effects need compatibility and reconciliation; rollback can be unsafe after new effects commit.

## Technical Debt — Identification, Prioritization, Remediation

Source: [Technical Debt — Identification, Prioritization, Remediation](30.3.5.02-technical-debt.md)

**Q:** What makes a debt item actionable rather than a complaint?

**A:** A concrete ongoing cost or risk, evidence of its impact, an owner and a bounded remediation option. Prioritize it against product work with the same resource constraints.

**Q:** Must technical debt have been deliberately chosen?

**A:** No. Inadvertent debt can be discovered when new information reveals a costly boundary. The useful decision records actual future friction/risk, remediation cost and affected work.

**Q:** When is parallel comparison of old/new implementations unsafe?

**A:** When both execute authoritative writes or remote effects, such as charging a payment. Use pure reads/calculations or isolated/suppressed side effects and a deliberate ownership transition.

**Q:** What must precede consolidating divergent booking checks, and where should concurrency be enforced?

**A:** Derive the intended rule from booking policy before choosing which behavior to keep. Then enforce the no-overlap invariant at the authoritative write boundary: two requests can both pass a preflight check before either writes. Use a storage constraint or transaction/locking mechanism suited to the data model and test competing requests. See [Technical Debt](30.3.5.02-technical-debt.md).

## Cost Engineering & FinOps

Source: [Cost Engineering & FinOps](30.3.5.03-cost-engineering-finops.md)

**Q:** Why should cost optimization use cost per useful business unit as well as total spend?

**A:** Lower spend can reflect lost traffic or degraded service. Unit cost connects resources to useful output, with reliability and performance tracked alongside it.

**Q:** Why can cost per request improve while cost per useful order worsens?

**A:** Retries inflate request counts without creating useful orders. Define output and cost boundaries, then compare total cost, successful business output, demand and reliability together.

**Q:** Should checkpoint recovery depend on receiving an interruption warning?

**A:** No. Notices are provider-specific and may be best-effort. Commit output and checkpoint atomically when they share a datastore; across systems, make replay idempotent or deduplicated and reconcile before acknowledging the job.

**Q:** What does a passing infrastructure cost estimate establish?

**A:** It estimates supported resource changes under its pricing and usage assumptions. It does not predict actual traffic, every runtime charge or the next invoice; a separate policy must decide whether the estimate blocks review or release. See [Cost Engineering & FinOps](30.3.5.03-cost-engineering-finops.md).

## Data Retention & Archival

Source: [Data Retention & Archival](30.3.5.04-data-retention-archival.md)

**Q:** Why must legal holds be checked on every deletion path?

**A:** A separate cleanup job, partition drop or storage lifecycle can otherwise erase held data. Holds must constrain automated expiry and have auditable release rules.

**Q:** Does a keyed pseudonym or name redaction automatically anonymize a record?

**A:** No. Identifiers, relationships and other attributes can remain linkable. Assess the actual data/context; pseudonymization is not automatic erasure or a compliance certificate.

**Q:** Why can a held record still disappear after a deletion worker checks no hold?

**A:** A hold can arrive between the check and action. Serialize hold/deletion decisions at an authority and revalidate action boundaries; remote work already submitted needs its own recovery.

**Q:** Does deleting a current S3 object guarantee all earlier versions are gone?

**A:** No. A delete marker/current expiration can leave noncurrent versions, while holds/retention can protect others. Verify relevant versions and the asynchronous policy outcome.

**Q:** Does the United Kingdom's one-month response period mean every backup must be physically erased within that month?

**A:** No. The [Information Commissioner's Office (ICO) guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/) describes when to respond, not a universal physical-erasure deadline. Determine scope, exceptions and deadlines under the applicable rules; where permitted, keep delayed backup copies inaccessible and beyond use until their established overwrite schedule.

**Q:** What can defeat cryptographic erasure after a key is deleted?

**A:** Other usable/wrapped/cached/backed-up keys or plaintext copies can still expose the data. Scope and verify every decryption path; deleting one key is not evidence that all copies are unreadable.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
