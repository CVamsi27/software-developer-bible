<!-- section: Infra Patterns | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-Infra%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Liveness Lifecycle — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Health Checks & Graceful Shutdown — Liveness, Readiness, SIGTERM

Source: [Health Checks & Graceful Shutdown — Liveness, Readiness, SIGTERM](30.3.1.01-health-checks-graceful-shutdown.md)

**Q:** Why should a dependency outage normally fail readiness before liveness?

**A:** Readiness withdraws traffic when the instance cannot serve. Restarting every instance for a shared dependency failure can create a restart storm without repairing that dependency.

**Q:** What is the shutdown order for a serving process?

**A:** Withdraw readiness, stop admitting work, drain accepted requests within a deadline, close resources and exit before forced termination.

**Q:** Why should liveness not depend on every downstream service?

**A:** A shared outage can restart every instance without repairing the dependency and can make recovery harder.

**Q:** What must a shutdown deadline reserve time for?

**A:** The slowest permitted in-flight work plus cleanup, with a forced-exit boundary shorter than the platform termination grace period.

**Q:** Why does a green probe not prove the business path works?

**A:** A probe checks a selected signal. Synthetic transactions or other end-to-end evidence are needed for important dependencies and workflows.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
