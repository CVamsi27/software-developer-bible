# Production Engineering — Index

> **Study time:** ≈ 1 h 2 m of reading (7 files, ~9 min average).
> **7 files** — Incident response, SLI/SLO/error budgets, chaos engineering, production readiness reviews, and sustainable on-call — operating systems in production. The senior differentiator stack.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why production engineering:** This is what separates a senior engineer from a staff/principal. Knowing how to design for reliability (SLOs), respond to incidents (postmortems), proactively find weaknesses (chaos engineering), gate launches (PRRs), and keep humans sustainable on-call is the difference between "ships features" and "owns the system".

---

## Topic Categories

| Category | File | Why it matters | Role priority | General importance |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------- | ------------------ |
| [Reliability Targets](#reliability-targets) | [SLI/SLO/Error Budgets](50.4.02-sli-slo-error-budgets.md) | The SRE framework — every staff interview | Important | Important |
| [Incident Response](#incident-response) | [Incident Response](50.4.01-incident-response.md) | When things break — severity, triage, postmortems | Important | Important |
| [Proactive Resilience](#proactive-resilience) | [Chaos Engineering in Production](50.4.03-chaos-engineering.md) | Exercise your redundancy before it is tested for real | Important | Important |
| [Launch Gates & Humans](#launch-gates--humans) | [Production Readiness Reviews](50.4.04-production-readiness-reviews.md), [On-Call Without Burnout](50.4.05-on-call-without-burnout.md) | Prevent incidents at launch; keep responders healthy | Important | Important |

---

## Reliability Targets

The SRE framework.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 02 | [SLI/SLO/Error Budgets](50.4.02-sli-slo-error-budgets.md) | SLIs, SLOs, SLAs, error budgets, burn rates, multi-window alerting, Prometheus/Grafana | Important | Important | 8 min |

**Quick recall:**
- **SLI** = the metric (e.g., request success rate)
- **SLO** = the target (e.g., 99.9% of requests succeed)
- **Error budget** = `1 - SLO` (e.g., 0.1% of requests can fail)

---

## Incident Response

When things break (and they will).

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Incident Response](50.4.01-incident-response.md) | Severity levels (SEV1-4), triage workflow, communication templates, blameless postmortems, runbooks | Important | Important | 11 min |

**Severity (typical):**
- **SEV1** — full outage, customers affected, all-hands
- **SEV2** — major degradation, some customers affected
- **SEV3** — minor issue, workaround exists
- **SEV4** — cosmetic, no customer impact

---

## Proactive Resilience

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 03 | [Chaos Engineering in Production](50.4.03-chaos-engineering.md) | Game-day runbook, production injection policy + guardrails, automated chaos in CI/CD, failover drills, resilience metrics (experiment design lives in [50.1.5.02](../50.1-testing/05-advanced/50.1.5.02-chaos-engineering.md)) | Important | Important | 9 min |

**Principles:**
1. Build a hypothesis around steady-state behavior
2. Vary real-world events (kill instance, inject latency, partition network)
3. Run experiments in production (start small)
4. Automate continuous experiments
5. Minimize blast radius

---

## Launch Gates & Humans

Prevention before the incident; sustainability after it.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Production Readiness Reviews](50.4.04-production-readiness-reviews.md) | PRR as go/no-go launch gate, checklist domains (capacity, alerts, runbooks, rollback, load tests, security), evidence-based review, risk tiers, lightweight variant | Important | Important | 10 min |
| 05 | [On-Call Without Burnout](50.4.05-on-call-without-burnout.md) | Primary/secondary rotations, follow-the-sun, paging philosophy (page only actionable), alert-fatigue governance, handoff rituals, comp-time policies, on-call health metrics | Important | Important | 11 min |
| 06 | [Interview Questions](50.4.06-interview-questions.md) | 6 senior Q&A: incident command, postmortem discipline, SLO governance, chaos experiment design, PRR gates, on-call health | Important | Important | 11 min |

**The two rules:**
- **PRR**: evidence over assertion — a gate that never defers anything is decoration.
- **On-call**: page symptoms, ticket causes — pager health is service health.

---

## Suggested Study Order

1. **SLI/SLO/Error Budgets** — the foundation
2. **Incident Response** — what to do when SLOs are violated
3. **Chaos Engineering** — proactively find weaknesses
4. **Production Readiness Reviews** — stop incidents before they start
5. **On-Call Without Burnout** — keep the humans running

---

## Common interview topics

- "What's an SLO? How do you set one?"
- "How do you use error budgets to make decisions?"
- "Walk me through a production incident you handled."
- "How do you write a blameless postmortem?"
- "How do you run a chaos experiment?"
- "How do you make sure a service is production-ready?" (PRR)
- "How do you keep on-call sustainable?" (rotation design, alert governance)

---

## Cross-References

- [Observability](../../40-platform/40.4-observability/INDEX.md) — the 3 pillars of observability feed SLOs
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — resilience patterns (circuit breaker, etc.)
- [Testing — Chaos](../50.1-testing/05-advanced/50.1.5.02-chaos-engineering.md) — chaos testing in depth

---

## Navigation

[← Previous: Performance Monitoring](../50.3-performance-monitoring/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: WebSockets →](../../60-realtime/60.1-websockets/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Runbooks | `docs/runbooks/` (`abdm-onboarding.md`, `abdm-sandbox-setup.md`) |
| Incident playbooks | `docs/operations/playbooks/` (`db-connection-exhaustion.md`, `razorpay-outage.md`, `pdf-queue-backlog.md`, …) |
| Release evidence practice | `docs/operations/releases/2026-08-06-p5-closure.md` + `RELEASE_EVIDENCE_CHECKLIST.md` |
| Audits | `docs/audits/2026-08-19-comprehensive-audit.md` (+ evidence dir) |
| ADR process as review gate | `docs/architecture/decisions/` — 15 numbered records incl. reversals (`0009-vercel-retired.md`) |
| Compliance automation | `apps/api/src/shared/modules/compliance/data-retention.scheduler.ts` + `archival.service.ts`; ops alerting via `ops-alert.listener.ts` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
