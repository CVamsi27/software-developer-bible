<!-- section: Observability | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Observability-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Observability — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## SLI, SLO & SLA

Source: [SLI, SLO & SLA](40.4.3.01-sli-slo-sla.md)

**Q:** How do an SLI and an SLO differ for a latency objective?

**A:** The SLI measures the fraction of eligible requests below a threshold; the SLO sets the target fraction and time window.

**Q:** Why is an error budget not always a number of downtime minutes?

**A:** Request-based budgets count failed eligible requests. Time-based availability can translate to minutes, but the denominator and user traffic model determine the budget.

**Q:** What should happen when the budget is exhausted?

**A:** Follow the pre-agreed policy for risky changes, reliability work, and exceptions. The budget informs a product decision rather than triggering an undocumented universal freeze.

## Alerting

Source: [Alerting](40.4.3.02-alerting.md)

**Q:** What makes a page actionable?

**A:** A symptom requires timely human action, has a clear owner, and links to a usable response. Informational trends can become tickets or dashboards instead.

**Q:** Why combine a short and a long burn-rate window?

**A:** The short window checks that excessive burn is still happening; the longer window confirms sustained impact and reduces isolated-spike noise.

## Budget and Alert Boundaries

Sources: [SLI/SLO/SLA](40.4.3.01-sli-slo-sla.md), [Alerting](40.4.3.02-alerting.md).

**Q:** A million eligible requests allow 0.1% failure and 600 failed. What remains?

**A:** The allowed budget is 1,000 bad requests and 400 remain. This is a request count, not 400 minutes. Eligibility, observed window and rounding policy must stay consistent.

**Q:** Does a six-hour slow-burn alert have to wait for the fast-burn alert?

**A:** No. Each policy combines its own long and short windows; either policy can act independently. A persistent 1% error ratio exceeds the 0.6% slow threshold without exceeding the 1.44% fast threshold.

**Q:** What does no eligible traffic prove about reliability?

**A:** Nothing about successful user service. The observed fraction is undefined. Low traffic, absent error series and a stopped scraper need explicit monitoring policies rather than a default healthy reading.

**Q:** Does a silence repair the service or remove contractual downtime?

**A:** It temporarily suppresses matching notifications. It needs an owner, reason and expiry; the incident and contractual measurement continue under their own rules.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
