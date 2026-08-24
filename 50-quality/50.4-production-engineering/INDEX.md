# Production Engineering — Index

> **3 files** — Incident response, SLI/SLO/error budgets, chaos engineering — operating systems in production. The senior differentiator stack.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why production engineering:** This is what separates a senior engineer from a staff/principal. Knowing how to design for reliability (SLOs), respond to incidents (postmortems), and proactively find weaknesses (chaos engineering) is the difference between "ships features" and "owns the system".

---

## Topic Categories

| Category | File | Why it matters |
|----------|------|----------------|
| [Reliability Targets](#reliability-targets) | [SLI/SLO/Error Budgets](50.4.02-sli-slo-error-budgets.md) | The SRE framework — every staff interview |
| [Incident Response](#incident-response) | [Incident Response](50.4.01-incident-response.md) | When things break — severity, triage, postmortems |
| [Proactive Resilience](#proactive-resilience) | [Chaos Engineering](50.4.03-chaos-engineering.md) | Find weaknesses before they find you |

---

## Reliability Targets

The SRE framework.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [SLI/SLO/Error Budgets](50.4.02-sli-slo-error-budgets.md) | SLIs, SLOs, SLAs, error budgets, burn rates, multi-window alerting, Prometheus/Grafana | 45 min |

**Quick recall:**
- **SLI** = the metric (e.g., request success rate)
- **SLO** = the target (e.g., 99.9% of requests succeed)
- **Error budget** = `1 - SLO` (e.g., 0.1% of requests can fail)

---

## Incident Response

When things break (and they will).

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Incident Response](50.4.01-incident-response.md) | Severity levels (SEV1-4), triage workflow, communication templates, blameless postmortems, runbooks | 45 min |

**Severity (typical):**
- **SEV1** — full outage, customers affected, all-hands
- **SEV2** — major degradation, some customers affected
- **SEV3** — minor issue, workaround exists
- **SEV4** — cosmetic, no customer impact

---

## Proactive Resilience

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Chaos Engineering](50.4.03-chaos-engineering.md) | Chaos experiments (network, resource, service), game days, Chaos Monkey, Gremlin, Litmus, resilience testing | 30 min |

**Principles:**
1. Build a hypothesis around steady-state behavior
2. Vary real-world events (kill instance, inject latency, partition network)
3. Run experiments in production (start small)
4. Automate continuous experiments
5. Minimize blast radius

---

## Suggested Study Order

1. **SLI/SLO/Error Budgets** — the foundation
2. **Incident Response** — what to do when SLOs are violated
3. **Chaos Engineering** — proactively find weaknesses

---

## Common interview topics

- "What's an SLO? How do you set one?"
- "How do you use error budgets to make decisions?"
- "Walk me through a production incident you handled."
- "How do you write a blameless postmortem?"
- "How do you run a chaos experiment?"

---

## Cross-References

- [Observability](../../40-platform/40.4-observability/INDEX.md) — the 3 pillars of observability feed SLOs
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — resilience patterns (circuit breaker, etc.)
- [Testing — Chaos](../../50-quality/50.1-testing/50.1.12-chaos-engineering.md) — chaos testing in depth

---

## Navigation

[← Previous: Performance Monitoring](../50.3-performance-monitoring/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: WebSockets →](../../60-realtime/60.1-websockets/INDEX.md)
