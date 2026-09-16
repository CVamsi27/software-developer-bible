# Shipping & Evolution

> **Study time:** ≈ 53 min of reading (4 files, ~13 min average).
> **4 files.** Change without breakage and grow without waste: deploying new versions with zero downtime, paying down technical debt deliberately, treating cloud spend as an engineering metric (FinOps), and managing data lifecycle from hot storage to legal-hold-compliant deletion.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Shipping-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Shipping is not `git push` to prod. Users are mid-request while you deploy; schemas change under running code; yesterday's shortcut becomes next quarter's outage — and yesterday's architecture quietly becomes this quarter's cloud bill. Zero-downtime deployment patterns (blue-green, canary, expand/contract migrations) decouple deploys from risk; a working technical-debt strategy keeps the codebase shippable years in; cost engineering makes dollars a monitored unit alongside latency; and data retention/archival keeps growth legal, deletable, and affordable.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Zero-Downtime Deployments](30.3.5.01-zero-downtime-deployments.md) | Rolling vs blue-green vs canary, expand/contract migrations, health-gated rollouts, rollback paths | 15 min |
| 02 | [Technical Debt](30.3.5.02-technical-debt.md) | Debt quadrants, intentional vs accidental debt, remediation strategy, communicating debt to stakeholders | 16 min |
| 03 | [Cost Engineering & FinOps](30.3.5.03-cost-engineering-finops.md) | Rightsizing, storage tiering, spot strategy, autoscaling traps, tagging/allocation, unit economics, cost checks in CI | 11 min |
| 04 | [Data Retention & Archival](30.3.5.04-data-retention-archival.md) | Retention drivers, log/metric tiers, hot/warm/cold storage, DB TTLs, legal hold, right-to-erasure pipelines, runbooks | 11 min |

---

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

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — ships and evolves for real.

| Topic | Docita evidence |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Feature flags & kill switches | `shared/modules/feature-flags/*` (controller + service + repository) and `services/feature-flag.service.ts` |
| Zero-downtime releases | Fly health-gated deploys (`grace_period 240s`), `worker-canary-deploy.sh`, release-evidence docs in `docs/operations/releases/*` |
| Safe schema evolution | Migration CI workflow + gates: `check-migration-safety.mjs`, `check-migration-reversibility.mjs` |
| Cost / FinOps | ADR 0011 suspend-to-zero off-hours + scheduled capacity via `scale-api-hours.yml`; single 2GB machine by design |
| Data retention | `compliance/data-retention.scheduler.ts` (see also [Data at Scale](../04-data-at-scale/INDEX.md)) |
