---
section: Observability
category: DevOps
tags: [concept, reference, guide]
---

# Alerting

## Definition

**Alerting** is the practice of notifying humans (or automated systems) when a system has deviated from expected behavior. A well-designed alerting system minimizes alert fatigue by alerting on **user-visible symptoms** rather than internal causes, uses **multi-window burn rates** to filter noise, and routes the right severity to the right responder.

A bad alerting setup pages engineers for every blip and they learn to ignore pages. A good one fires 1-3 times per week, always with a runbook, and the on-call knows what to do before opening Slack.

## Why Do We Need It?

1. **Detect incidents before users complain**: most outages are user-reported first because alerts are too noisy to act on
2. **Reduce MTTR (Mean Time To Resolve)**: faster detection = faster resolution
3. **Avoid alert fatigue**: every false positive erodes trust and causes people to ignore real alerts
4. **Meet SLA commitments**: missing SLOs triggers contractual penalties — alerting is the early warning
5. **Distinguish symptoms from causes**: page on "checkout failing", not "database CPU high" (which might not be the cause)

## How It Works

### The Alerting Pyramid

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   P0  ─►  Page immediately (PagerDuty phone call)           │
│         User-facing outage, revenue impact, SLO breach      │
│         Examples: 5xx rate > 5%, checkout down              │
│                                                             │
│   P1  ─►  Slack alert + ticket                              │
│         Degraded experience, SLO at risk                    │
│         Examples: p99 latency > 2s, queue depth growing     │
│                                                             │
│   P2  ─►  Dashboard annotation + email                      │
│         Sub-threshold issue, monitor over time              │
│         Examples: error rate trending up, capacity 80%      │
│                                                             │
│   P3  ─►  Weekly review / dashboard                         │
│         Background signal, no immediate action              │
│         Examples: dependency deprecation warning            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Alert Routing

```text
Source (Prometheus, Datadog, etc.)
  │
  ▼
Alertmanager (deduplication, grouping, silencing)
  │
  ├──► PagerDuty (for P0) ──► Phone call → on-call engineer
  ├──► Slack #alerts-critical (P1)
  ├──► Slack #alerts-warnings (P2)
  └──► Email (P3)
```

## Alert Design Principles

### 1. Alert on Symptoms, Not Causes

```text
❌ Bad: "Postgres CPU > 90%" — many alerts on this, rarely the right action
✅ Good: "Checkout 5xx rate > 1% for 5 min" — clear user impact
```

The cause might be database, network, or a deploy. The alert points to the user impact; the runbook walks through diagnosis.

### 2. Multi-Window Burn Rate

From Google SRE Workbook — alert on **both**:
- Fast burn: 1h window over 14.4x budget consumption (catches acute incidents)
- Slow burn: 6h window over 6x budget consumption (catches creeping issues)

```text
Fast burn (1h):
  if error_rate_1h > 14.4 × (1 - SLO) → PAGE
  Example: 99.9% SLO → 1h error rate > 1.44%

Slow burn (6h):
  if error_rate_6h > 6 × (1 - SLO) → PAGE
  Example: 99.9% SLO → 6h error rate > 0.6%
```

Both conditions must be true. Single-window alerts fire on every blip; multi-window requires sustained burn.

### 3. Alert Grouping & Deduplication

Hundreds of pod restarts → 1 page, not 100 pages. Alertmanager groups by:
- `cluster`, `service`, `severity`
- `summary` template (regex match)
- Time window: 30s default

### 4. Silence for Maintenance

```yaml
# Alertmanager silence matchers
matchers:
  - alertname = "DiskSpaceLow"
  - severity = "warning"
  - cluster = "staging"

# Active for the deploy window
startsAt: 2024-01-15T10:00:00Z
endsAt: 2024-01-15T12:00:00Z
comment: "Schema migration on staging, expected disk usage"
```

## Code Examples

### Prometheus Alerting Rules

```yaml
# alerts.yaml
groups:
  - name: api-availability
    interval: 30s
    rules:
      # Fast burn: 2% of 30-day budget in 1 hour
      - alert: ApiHighErrorBudgetBurn_1h
        expr: |
          (
            sum(rate(http_requests_total{job="api",status=~"5xx"}[1h]))
            /
            sum(rate(http_requests_total{job="api"}[1h]))
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
          slo: api-availability
        annotations:
          summary: "API burning error budget at 14x rate (1h)"
          description: "Error rate {{ $value | humanizePercentage }} exceeds 14x SLO"
          runbook: "https://runbooks.example.com/api-availability"

      # Slow burn: 5% of 30-day budget in 6 hours
      - alert: ApiHighErrorBudgetBurn_6h
        expr: |
          (
            sum(rate(http_requests_total{job="api",status=~"5xx"}[6h]))
            /
            sum(rate(http_requests_total{job="api"}[6h]))
          ) > (6 * 0.001)
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API slowly burning error budget (6h)"
          runbook: "https://runbooks.example.com/api-availability"
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers:
        - severity = "critical"
      receiver: 'pagerduty'
      group_wait: 10s
      repeat_interval: 1h
    - matchers:
        - severity = "warning"
      receiver: 'slack-warnings'

receivers:
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
        description: '{{ .CommonAnnotations.summary }}'
        details:
          runbook: '{{ .CommonAnnotations.runbook }}'
          severity: '{{ .CommonLabels.severity }}'
    # Auto-include the runbook link

  - name: 'slack-warnings'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#alerts-warnings'
        title: '{{ .CommonAnnotations.summary }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

### PagerDuty Integration with Auto-Escalation

```yaml
receivers:
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<key>'
        # Escalation: L1 -> L2 -> L1 manager after 15 min
        # Configured in PagerDuty service settings
```

In PagerDuty:
- L1 schedule: on-call engineer (15 min)
- L2 schedule: secondary on-call (after L1 timeout)
- L3: engineering manager (after 30 min)

## Real-World Use Cases

### 1. Blackbox Exporter for Synthetic Monitoring

```yaml
# prometheus blackbox config
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      valid_status_codes: [200, 204]

# Scrape config
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://example.com
          - https://example.com/api/health
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115

# Alert: site down
- alert: WebsiteDown
  expr: probe_success{job="blackbox"} == 0
  for: 2m
  labels:
    severity: critical
```

### 2. SLO-Aware Alerting with Sloth

```bash
# Generate Prometheus rules + alerts from SLO spec
sloth generate -i ./slo/api-availability.yaml \
  --output ./prometheus-rules/api-availability.yaml

# Includes burn rate alerts at multiple windows automatically
```

### 3. Health Check Probe Alerts (Kubernetes)

```yaml
# Pod stuck in CrashLoopBackOff
- alert: PodCrashLooping
  expr: |
    rate(kube_pod_container_status_restarts_total[10m]) * 60 * 5 > 0
  for: 5m
  labels:
    severity: warning

# Probe failures
- alert: KubernetesNodeNotReady
  expr: kube_node_status_condition{condition="Ready",status="true"} == 0
  for: 5m
  labels:
    severity: critical
```

## Common Mistakes

### 1. Alerting on Everything

```text
❌ Bad: 200+ alerts across the org, 50 firing at any time
✅ Good: < 10 alerts per service, all actionable, all with runbooks
```

If a page doesn't have a clear action ("restart pod", "rollback deploy", "scale out"), it's not ready to be a page.

### 2. No Runbook

Every alert should link to a runbook. Without one, the on-call engineer wastes 30 minutes reading docs instead of fixing.

```yaml
annotations:
  runbook: "https://runbooks.example.com/checkout-failures"
  dashboard: "https://grafana.example.com/d/checkout"
  slack: "https://slack.com/archives/C12345"
```

### 3. Using Percentile Alerts Without Context

```text
❌ Bad: p99 latency > 200ms
✅ Good: p99 latency > 200ms for 5 min AND (not during deploy)
```

A single spike of 200ms is noise. Sustained 200ms+ is a problem. Use `for: 5m` to require duration.

### 4. Pager Spam During Incidents

When a major incident is already being handled, secondary alerts pile on. Use **inhibitions** to suppress:

```yaml
# alertmanager.yml
inhibit_rules:
  - source_matchers: [severity="critical", alertname="ServiceDown"]
    target_matchers: [severity="warning"]
    equal: [cluster, service]
    # When "ServiceDown" fires, suppress all "warning" alerts for same service
```

## Best Practices

1. **Alert on user-impacting symptoms**, not internal metrics
2. **Every alert has a runbook** linked in the annotation
3. **Multi-window burn rate** for SLO-based alerts (1h + 6h)
4. **Group related alerts** (don't page 50 times for one incident)
5. **Use silences** during planned maintenance and incidents
6. **Page only what wakes someone up** at night
7. **Review alerts quarterly** — silence rates > 50% means it's noise
8. **Track "useless pages"** — every page that doesn't lead to action
9. **Test alerts** — fire them in staging to verify they actually work
10. **Document escalation** — who, when, how long before next level

## Alerting Anti-Patterns

| Anti-Pattern | Why It's Bad | Better |
|--------------|--------------|--------|
| Alert on raw CPU > 80% | Doesn't mean user impact | Alert on request success rate |
| Page on single failure | Catches blips | Use `for:` duration |
| 100+ alerts per service | Alert fatigue | < 10, all actionable |
| No runbook | Slow resolution | Always link runbook |
| Alert in dev/staging | Wakes up on-call | Environment label, separate routing |
| "Container restarted" | Restart can be normal | Alert on CrashLoopBackOff pattern |

## Performance Considerations

- **Alertmanager group_wait** (30s default): delays grouping; lower for P0
- **repeat_interval** (4h default): don't re-page too often
- **Evaluate interval** (30s): too frequent = load on Prometheus
- **Cardinality**: keep labels low (alertname, severity, service) to avoid explosion

## Summary

- Alert on **user-visible symptoms**, not internal causes
- Use **multi-window burn rate** (1h fast, 6h slow) for SLO-based alerting
- Every alert has a **runbook**, **dashboard link**, and **clear action**
- Group and deduplicate to avoid alert storms
- Silence during planned maintenance, inhibit during known incidents
- Review alerts quarterly — silence rate > 50% is noise
- < 10 actionable alerts per service is the goal

---

## Cheat Sheet
```text
ALERTING CHEAT SHEET
============================================================

PRINCIPLES:
  • Alert on symptoms (user impact), not causes (CPU)
  • Multi-window burn rate (1h fast + 6h slow)
  • Every alert has a runbook
  • < 10 actionable alerts per service

SEVERITY LEVELS:
  P0 critical - page immediately (PagerDuty)
  P1 warning  - Slack + ticket
  P2 info     - email + dashboard
  P3 low      - weekly review

BURN RATE THRESHOLDS (SLO 99.9%):
  1h window:  > 1.44% errors = page (14.4x burn)
  6h window:  > 0.6%  errors = page (6x burn)
  Both conditions must hold (multi-window)

PROMETHEUS EXAMPLE:
  - alert: ApiHighErrorBudgetBurn
    expr: |
      (sum(rate(http_5xx[1h])) / sum(rate(http_all[1h])))
      > (14.4 * 0.001)
    for: 2m
    annotations:
      runbook: "https://runbooks.example.com/api"

INTERVIEW TIPS:
  • Explain why symptom > cause for alerts
  • Walk through multi-window burn rate math
  • Discuss alert fatigue and how to fight it
  • Mention the "every alert has a runbook" rule
```
---

## See Also
- [Error Tracking](04-Error-Tracking.md)
- [Health Checks](05-Health-Checks.md)
- [Kubernetes](../14-Kubernetes/)
- [Logging](01-Logging.md)
- [Monitoring](02-Monitoring.md)
- [SLI / SLO / SLA](07-SLI-SLO-SLA.md)
- [System Design](../11-System-Design/)

## References & Learn More

- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Google SRE Workbook - Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Prometheus Alerting Best Practices](https://prometheus.io/docs/practices/alerting/)
- [Alertmanager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
- [Sloth - SLO generator](https://github.com/slok/sloth)
- [Robust Perception - Alerts Best Practices](https://www.robustperception.io/)
