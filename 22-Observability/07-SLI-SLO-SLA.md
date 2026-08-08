---
section: Observability
category: DevOps
tags: [concept, reference, guide]
---

# SLI, SLO & SLA

## Definition

**SLI** (Service Level Indicator), **SLO** (Service Level Objective), and **SLA** (Service Level Agreement) form the hierarchy of reliability commitments in SRE practice. They answer progressively harder questions: *what we measure*, *what we promise*, and *what we are contractually liable for*.

- **SLI**: a quantitative measure of service behavior (e.g., p99 request latency)
- **SLO**: the target value for an SLI over a window (e.g., p99 < 200ms for 99.9% of requests over 30 days)
- **SLA**: a contractual agreement with consequences (refund, credit) when the SLO is missed

The **error budget** is the inverse of the SLO target — the allowed failure rate. A 99.9% SLO gives a 0.1% error budget, which can be "spent" on releases, incidents, or experiments.

## Why Do We Need It?

1. **Align engineering with users**: measure what users experience, not what ops monitors
2. **Avoid over-engineering**: 100% reliability is impossible and unaffordable; SLOs define "good enough"
3. **Data-driven reliability decisions**: when to invest in reliability vs. features
4. **Customer trust**: SLAs formalize commitments in vendor contracts
5. **Burn rate alerting**: alert when error budget is consumed too fast, not on individual failures

## How It Works

### The Reliability Hierarchy

```text
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   SLA (contract) ───────►  SLO (target)  ───────►  SLI (metric)  │
│   "99.9% uptime           "p99 < 200ms for        request       │
│    or 10% credit"          99.9% of requests"     latency       │
│                                                                 │
│   ▼                                                              │
│                                                                 │
│   Error Budget = 100% − SLO target                              │
│   e.g., SLO 99.9% → 0.1% budget → ~43.8 min downtime/month     │
│                                                                 │
│   Burn Rate = how fast you're consuming the budget              │
│   1.0 = on pace, 2.0 = burning 2x as fast (alert!)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Common SLI Categories

| Category | SLI Example | Good For |
|----------|-------------|----------|
| **Availability** | ratio of successful requests (2xx) | User-facing APIs |
| **Latency** | p99 of request duration < threshold | Performance-critical paths |
| **Throughput** | requests/sec processed | Batch jobs, queues |
| **Correctness** | ratio of correct responses | ML models, search relevance |
| **Freshness** | age of last successful data update | Dashboards, cache invalidation |
| **Durability** | ratio of data retained over time | Storage systems |

### SLO Target Tiers

| SLO | Downtime/Month | Use Case |
|-----|----------------|----------|
| 90% | 72 hours | Internal tools, dev environments |
| 99% | 7.2 hours | Many B2B apps |
| 99.9% | 43.8 minutes | Most production APIs |
| 99.95% | 21.9 minutes | Critical user-facing |
| 99.99% | 4.4 minutes | Infrastructure (e.g., DNS) |
| 99.999% | 26.3 seconds | Telecom, payment processing |

The cost grows ~10x for each additional "9" — be honest about what users need.

## Code Examples

### Defining an SLI in OpenSLO

```yaml
# slo-availability.yaml
apiVersion: openslo/v1
kind: SLO
metadata:
  name: api-availability
spec:
  description: HTTP API availability
  service: checkout-service
  budgetingMethod: Occurrences
  objectives:
    - displayName: 99.9% availability
      target: 0.999
      timeWindow:
        - duration: 30d
          isRolling: true
  indicators:
    - name: http-availability
      spec:
        ratioMetric:
          counter: true
          good:
            source: prometheus
            query: |
              sum(rate(http_requests_total{job="checkout",status=~"2xx"}[5m]))
          total:
            source: prometheus
            query: |
              sum(rate(http_requests_total{job="checkout"}[5m]))
```

### Prometheus Recording Rule for Error Rate

```yaml
# prometheus-rules.yaml
groups:
  - name: slo-recording
    interval: 30s
    rules:
      - record: slo:slo_error_burnrate:ratio_rate_5m
        expr: |
          (
            sum(rate(http_requests_total{job="api",status=~"5xx"}[5m]))
            /
            sum(rate(http_requests_total{job="api"}[5m]))
          )
```

### Multi-Window Burn Rate Alert

```yaml
# Alert: 2% of budget in 1h AND 5% of budget in 6h
- alert: SLO_HighBurnRate
  expr: |
    (
      slo:slo_error_burnrate:ratio_rate_1h{sloth_id="api-availability"} > (14.4 * 0.001)
      and
      slo:slo_error_burnrate:ratio_rate_6h{sloth_id="api-availability"} > (6 * 0.001)
    )
  for: 2m
  labels:
    severity: critical
    slo: api-availability
  annotations:
    summary: "API availability SLO burning 14x faster than sustainable"
    runbook: https://runbooks.example.com/api-availability
```

This is the **Google SRE workbook** pattern: 1h short window catches fast burns; 6h long window filters out blips.

### Measuring p99 Latency in Prometheus

```yaml
# histogram for latency SLI
- record: slo:slo_latency_p99:histogram_quantile_5m
  expr: |
    histogram_quantile(0.99,
      sum by (le) (rate(http_request_duration_seconds_bucket{job="api"}[5m]))
    )
```

## Real-World Use Cases

### 1. Multi-Tier SLOs

```text
User-Facing Tier:
  SLO: page LCP < 2.5s for 99% of page views
  SLI: Real User Monitoring (CrUX + web-vitals)

API Tier:
  SLO: checkout endpoint p99 < 500ms, 99.95% success
  SLI: Prometheus histogram_quantile + success rate

Storage Tier:
  SLO: write durability 99.999999% (eight nines)
  SLI: ratio of bytes written to bytes still readable
```

### 2. Error Budget Policy

```markdown
## Error Budget Policy (api-service)

If we burn 50% of the monthly budget before day 15:
  - Pause non-critical feature releases
  - Engineering lead reviews top 3 contributors
  - SRE team runs a reliability sprint (2 weeks)

If we burn 100% of the monthly budget:
  - Feature freeze until next budget window
  - Root cause analysis on top 5 incidents
  - Reliability OKRs prioritized over feature OKRs
```

### 3. SLA Tiers in B2B

```text
Free tier:    99% uptime, no SLA, no refund
Pro tier:     99.9% uptime, 10% credit if violated
Enterprise:   99.95% uptime, 25% credit + dedicated support
```

## Common Mistakes

### 1. Setting SLO = 100%

100% is impossible and unaffordable. Even Google Search publishes a 99.99% SLO, not 100%.

### 2. Measuring the Wrong Thing

```text
❌ Bad: server CPU < 80% (proxy for health)
✅ Good: 99% of user requests complete in < 500ms (user experience)
```

### 3. Single-Window Burn Rate Alerts

```text
❌ Bad: alert when 5xx > 0.1% over 5 min (alert on every blip)
✅ Good: alert on 1h burn (catches fast) AND 6h burn (sustained)
```

### 4. Forgetting to Communicate SLOs

Engineering, product, and leadership must agree on SLOs. Without this, SLOs become an "SRE team's problem" and are ignored when convenient.

### 5. Tracking Only Availability

Latency SLOs are often more important. A service that always returns 200 but takes 30 seconds is unusable.

## Best Practices

1. **Start with availability + latency SLI** — easiest to measure, most user-visible
2. **Choose realistic targets** — what you can sustain, not what sounds impressive
3. **Use multi-window burn-rate alerts** (1h short, 6h long)
4. **Document the error budget policy** — what happens when budget is exhausted?
5. **Review SLOs quarterly** with product and engineering
6. **Tie SLOs to user journeys**, not internal components
7. **Track SLO compliance over rolling 30/90 days** for trend analysis
8. **Publish SLOs internally** — dashboard, monthly review
9. **Pair SLOs with runbooks** — every alert links to a runbook
10. **Measure from the user's perspective** — synthetic + RUM, not just server metrics

## Performance Considerations

| Factor | Impact on SLO |
|--------|---------------|
| Tail latency (p99) | Most user-visible pain point |
| Cold starts (Lambda) | Can blow latency SLOs |
| Network jitter | Affects p99 disproportionately |
| DB query time | Common root cause of latency SLO breach |
| Retry storms | Can amplify and extend incidents |

## Summary

- SLI is a metric, SLO is a target, SLA is a contract
- Error budget = 1 − SLO target; burn rate measures consumption
- Multi-window burn-rate alerts (1h + 6h) catch real incidents without alert fatigue
- Set realistic targets (99.9% is enough for most B2B)
- Pair SLOs with runbooks, dashboards, and error budget policies
- Review SLOs quarterly with stakeholders

---

## Cheat Sheet
```text
SLI / SLO / SLA CHEAT SHEET
============================================================

HIERARCHY:
  SLI = what you MEASURE     (e.g., p99 latency, error rate)
  SLO = what you TARGET      (e.g., p99 < 200ms for 99.9%)
  SLA = what you CONTRACT    (e.g., 10% credit if breached)

ERROR BUDGET:
  budget = 1 - SLO
  e.g., 99.9% SLO = 0.1% budget = ~43.8 min/month

BURN RATE:
  rate of budget consumption
  1.0 = on pace, 14.4 = 1h fast burn (alert)
  Use 1h + 6h windows AND'd to avoid blips

COMMON SLI METRICS:
  availability = (good_requests / total_requests)
  latency_p99 = histogram_quantile(0.99, ...)
  throughput = rate(requests[5m])
  freshness = time() - max(timestamp)

SLO TARGETS (typical):
  99%   - 7.2 h/month     - B2B internal tools
  99.9% - 43.8 min/month  - production APIs
  99.99% - 4.4 min/month  - critical infrastructure
  99.999% - 26 sec/month  - payment / telecom

INTERVIEW TIPS:
  • Always explain the difference between SLI / SLO / SLA
  • Discuss error budget policy in practice
  • Show how to compute burn rate from Prometheus
  • Mention the cost curve of additional 9s
```
---

## See Also
- [Error Tracking](04-Error-Tracking.md)
- [Kubernetes](../14-Kubernetes/)
- [Logging](01-Logging.md)
- [Monitoring](02-Monitoring.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [System Design](../11-System-Design/)

## References & Learn More

- [Google SRE Book - SLO chapter](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE Workbook - Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [Sloth (SLO generator for Prometheus)](https://github.com/slok/sloth)
- [OpenSLO Specification](https://openslo.com/)
- [Prometheus Best Practices - SLO](https://prometheus.io/docs/practices/alerting/)
