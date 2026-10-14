# Shipping & Evolution

> **Study time:** ≈ 31 min of reading (5 files, ~6 min average).
> **5 files.** Change without breakage and grow without waste: deploying new versions with zero downtime, paying down technical debt deliberately, treating cloud spend as an engineering metric (FinOps), and managing data lifecycle from hot storage to legal-hold-compliant deletion.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Shipping-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Shipping is not `git push` to prod. Users are mid-request while you deploy; schemas change under running code; yesterday's shortcut becomes next quarter's outage — and yesterday's architecture quietly becomes this quarter's cloud bill. Zero-downtime deployment patterns (blue-green, canary, expand/contract migrations) decouple deploys from risk; a working technical-debt strategy keeps the codebase shippable years in; cost engineering makes dollars a monitored unit alongside latency; and data retention/archival keeps growth legal, deletable, and affordable.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Zero-Downtime Deployments](30.3.5.01-zero-downtime-deployments.md) | Deployment vs release; rolling, blue-green, canary and flags; expand/migrate/contract; drain and rollback boundaries | Important | Specialized | 7 min |
| 02 | [Technical Debt](30.3.5.02-technical-debt.md) | Evidence-based debt items, cost and risk prioritization, strangler and abstraction migrations, tests and exit conditions | Important | Specialized | 6 min |
| 03 | [Cost Engineering & FinOps](30.3.5.03-cost-engineering-finops.md) | Cost allocation, capacity and storage trade-offs, interruptible work, autoscaling signals, unit economics and estimate limits | Important | Specialized | 7 min |
| 04 | [Data Retention & Archival](30.3.5.04-data-retention-archival.md) | Per-class policies and clocks; telemetry tiers; archive retrieval and cost; database expiry lag; serialized holds; deletion across recipients, backups and restores | Important | Specialized | 9 min |

---

## Reading Path and Completion Check

Separate deployment from behavior release. Trace compatibility through rollout and migration; use representative evidence to promote a canary, and know when rollback must become forward repair.

For technical debt, turn a recurring cost or risk into an owned item, compare it with affected future work, then migrate in stages with verification. For FinOps, trace billed quantities to an owner and useful output. Evaluate capacity, storage and interruptible-work choices against service and recovery needs, then validate estimates against actual spend.

For retention, define a policy and clock for each data class and map every copy. Verify archive readability, serialize holds with deletion, and follow expiry through backup and restore paths.

Describe a reversible release, an evidence-backed debt decision and an expiry path constrained by retention and holds. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [CI/CD Stack](../../../40-platform/40.3-ci-cd/INDEX.md) — pipelines that execute these deploy patterns
- [Blue-Green & Canary](../../../40-platform/40.3-ci-cd/03-releases-and-metrics/INDEX.md) — the platform-level implementation
- [Liveness & Lifecycle](../01-liveness-lifecycle/INDEX.md) — graceful shutdown makes zero-downtime possible
- [Feature Flags & Kill Switches](../02-failure-and-recovery/30.3.2.04-feature-flags-kill-switches.md) — decouple deploy from release
- [Backup Strategy & Restore Drills](../02-failure-and-recovery/30.3.2.05-backup-strategy-restore-drills.md) — retention applied to backup artifacts

---

## Navigation

[← Data at Scale](../04-data-at-scale/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md)

---

## Docita Anchor

Candidate implementation locations in [Docita](https://github.com/CVamsi27/docita). Source configuration and gate names guide inspection; inspect the checked-out revision and execution evidence before claiming deployed recovery, capacity, hold or deletion guarantees.

| Topic | Docita evidence |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Feature flags & kill switches | `shared/modules/feature-flags/*` (controller + service + repository) and `apps/api/src/shared/modules/services/feature-flag.service.ts` |
| Zero-downtime releases | Inspect Fly API health/grace configuration; worker startup is not a business-operation probe. Release evidence must establish compatibility and recovery, not merely successful startup |
| Safe schema evolution | Migration CI workflow + gates: `check-migration-safety.mjs`, `check-migration-reversibility.mjs` |
| Cost / FinOps | Inspect API VM sizing, suspend/auto-start and minimum-machine configuration. A workflow file does not prove scheduled capacity changes are currently enabled |
| Data retention | `apps/api/src/shared/modules/compliance/data-retention.scheduler.ts` (see also [Data at Scale](../04-data-at-scale/INDEX.md)) |
