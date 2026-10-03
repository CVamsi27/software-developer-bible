<!-- section: CI/CD | category: Reference | tags: revision, practice| general-importance: important| general-importance: important | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-CI/CD-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# CI/CD — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Blue-Green & Canary Deployments

Source: [Blue-Green & Canary Deployments](40.3.3.01-blue-green-canary.md)

**Q:** What decides whether a canary should receive more traffic?

**A:** Measured user-facing success/latency and release-specific signals against a baseline, with an observation window and explicit abort policy; readiness alone is insufficient.

**Q:** Why can a blue-green traffic switch require database compatibility?

**A:** Both application versions may overlap and rollback may restore the old version. Schema/data changes must support that coexistence or use an explicit migration boundary.

**Q:** What should rollback verification observe after a switch?

**A:** The active artifact/configuration, successful requests, latency, error rates, and data compatibility. A completed deployment command does not establish user recovery.

## DORA Metrics & Delivery Performance

Source: [DORA Metrics & Delivery Performance](40.3.3.02-dora-metrics-delivery-performance.md)

**Q:** Why should delivery metrics be interpreted for a service rather than ranked across people?

**A:** Services have different risk, traffic, deployment boundaries, and observation windows. The metrics guide system improvement; individual rankings encourage gaming and hide context.

**Q:** Why can deployment frequency rise while reliability falls?

**A:** Shipping rate is only one dimension. Change failures, recovery, user-facing reliability, and workload context must accompany it.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
