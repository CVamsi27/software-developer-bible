<!-- section: Infra Patterns | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-Infra%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Shipping And Evolution — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Zero-Downtime Deployments — Blue-Green, Canary, Rolling, Feature Flags

Source: [Zero-Downtime Deployments — Blue-Green, Canary, Rolling, Feature Flags](30.3.5.01-zero-downtime-deployments.md)

**Q:** Why must a rollback plan include database compatibility?

**A:** The previous binary may encounter a schema or data format introduced by the new version. Expand/contract changes keep old and new readers/writers compatible during overlap.

**Q:** What should precede a canary percentage increase?

**A:** A defined observation window and checks for errors, latency, saturation and business correctness, with a tested stop/rollback path and compatible data changes.

## Technical Debt — Identification, Prioritization, Remediation

Source: [Technical Debt — Identification, Prioritization, Remediation](30.3.5.02-technical-debt.md)

**Q:** What makes a debt item actionable rather than a complaint?

**A:** A concrete ongoing cost or risk, evidence of its impact, an owner and a bounded remediation option. Prioritize it against product work with the same resource constraints.

## Cost Engineering & FinOps

Source: [Cost Engineering & FinOps](30.3.5.03-cost-engineering-finops.md)

**Q:** Why should cost optimization use cost per useful business unit as well as total spend?

**A:** Lower spend can reflect lost traffic or degraded service. Unit cost connects resources to useful output, with reliability and performance tracked alongside it.

## Data Retention & Archival

Source: [Data Retention & Archival](30.3.5.04-data-retention-archival.md)

**Q:** Why must legal holds be checked on every deletion path?

**A:** A separate cleanup job, partition drop or storage lifecycle can otherwise erase held data. Holds must constrain automated expiry and have auditable release rules.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
