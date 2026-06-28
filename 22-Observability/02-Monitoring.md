# Monitoring

## Definition

Monitoring is the process of collecting, analyzing, and acting on metrics (numeric measurements) to understand system health, performance, and behavior over time. While logging tells you *what happened*, monitoring tells you *how your system is performing* right now and whether it has deviated from expected behavior.

A **monitoring system** scrapes or receives metrics at regular intervals, stores them in a time-series database, visualizes them on dashboards, and fires alerts when predefined thresholds are breached.

## Why Do We Need It?

1. **Proactive detection**: Catch issues before users report them

2. **Capacity planning**: Understand resource usage trends to plan scaling

3. **SLA compliance**: Track uptime, latency percentiles, and error rates against targets

4. **Performance optimization**: Identify bottlenecks (slow DB queries, high memory, CPU saturation)

5. **Incident response**: Provides the data to diagnose and resolve production incidents

6. **Business KPIs**: Track requests/second, conversion rates, queue depths

## How It Works

```text
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐ │
│  │  Application  │    │  Prometheus   │    │    Grafana       │ │
│  │  /metrics     │───▶│  (scrape)     │───▶│  (dashboards)    │ │
│  │  endpoint     │    │               │    │                  │ │
│  └──────────────┘    └──────┬───────┘    └──────────────────┘ │
│                              │                                   │
│  ┌──────────────┐           │           ┌──────────────────┐   │
│  │   Node.js    │───────────┤           │  AlertManager    │   │
│  │   /metrics   │           │           │  (PagerDuty,     │   │
│  └──────────────┘           │           │   Slack, Email)  │   │
│                              │           └──────────────────┘   │
│  ┌──────────────┐           │                                   │
│  │   Postgres   │───────────┘                                   │
│  │   exporter   │                                               │
│  └──────────────┘                                               │
│                                                                 │
│  Time Series DB (Prometheus TSDB / Thanos / Mimir)             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ metric_name{label1="val1", label2="val2"} timestamp value│  │
│  │ http_requests_total{method="GET", status="200"} 1500    │   │
│  │ http_request_duration_seconds{method="POST"} p99=0.45   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

```

### Metric Types

```text
┌─────────────────────────────────────────────────────────────────┐
│  METRIC TYPES                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  COUNTER (monotonically increasing)                            │
│  ────────────────────────────────                              │
│  100 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╱                      │
│   80 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╱                          │
│   60 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╱                                │
│   40 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╱                                    │
│   20 ─ ─ ─ ─ ─ ─ ─ ─ ╱                                        │
│    0 ──────────────── t                                        │
│  Examples: total requests, total errors, bytes transferred     │
│                                                                 │
│  GAUGE (can go up and down)                                     │
│  ─────────────────────────                                     │
│  100 ─ ─ ─ ╱╲                                                 │
│   80 ─ ─ ╱    ╲ ─ ─ ╱╲                                       │
│   60 ─ ╱        ╲ ╱    ╲                                     │
│   40 ─             ╲     ╲                                    │
│   20 ─               ╲     ╲╱                                 │
│    0 ──────────────── t                                        │
│  Examples: CPU usage, memory, active connections, queue size   │
│                                                                 │
│  HISTOGRAM (distribution of values)                             │
│  ─────────────────────────────────                             │
│    ████                                                         │
│    ████ ████                                                    │
│    ████ ████ ████                                               │
│    ████ ████ ████ ████                                         │
│  ────────────────────── t                                      │
│  bucket: [0-100ms] [100-200ms] [200-500ms] [500ms-1s]        │
│  Examples: request latency, response size, query duration       │
│                                                                 │
│  SUMMARY (like histogram, computed client-side)                 │
│  ─────────────────────────────────────────                     │
│  Similar to histogram but calculates quantiles on the client.  │
│  Use histogram for aggregation across instances.                │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Prometheus Metrics with prom-client

```typescript
import express from "express";
import { register, Counter, Histogram, Gauge, collectDefaultMetrics } from "prom-client";

// Collect default Node.js metrics (GC, event loop, memory, CPU)
collectDefaultMetrics({ prefix: "myapp_" });

// Define custom metrics
const httpRequestTotal = new Counter({
  name: "http_requests_total",
  help: "Total number of HTTP requests",
  labelNames: ["method", "route", "status"],
});

const httpRequestDuration = new Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request duration in seconds",
  labelNames: ["method", "route", "status"],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

const activeConnections = new Gauge({
  name: "active_connections",
  help: "Number of active connections",
});

const ordersProcessed = new Counter({
  name: "orders_processed_total",
  help: "Total orders processed",
  labelNames: ["status", "paymentMethod"],
});

const queueSize = new Gauge({
  name: "job_queue_size",
  help: "Current size of the job queue",
  labelNames: ["queueName"],
});

// Middleware to instrument Express
function metricsMiddleware(req: express.Request, res: express.Response, next: express.NextFunction) {
  const startTime = Date.now();
  activeConnections.inc();

  res.on("finish", () => {
    const duration = (Date.now() - startTime) / 1000;
    const route = req.route?.path || req.path;

    httpRequestTotal.inc({
      method: req.method,
      route,
      status: res.statusCode.toString(),
    });

    httpRequestDuration.observe(
      { method: req.method, route, status: res.statusCode.toString() },
      duration
    );

    activeConnections.dec();
  });

  next();
}

// Expose metrics endpoint for Prometheus to scrape
const app = express();
app.use(metricsMiddleware);

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

// Example business routes
app.post("/api/orders", async (req, res) => {
  try {
    const order = await processOrder(req.body);
    ordersProcessed.inc({ status: "success", paymentMethod: order.paymentMethod });
    res.json(order);
  } catch (err) {
    ordersProcessed.inc({ status: "error", paymentMethod: "unknown" });
    res.status(500).json({ error: "Order failed" });
  }
});

app.get("/api/orders/:id", async (req, res) => {
  const order = await getOrder(req.params.id);
  res.json(order);
});

export { app, httpRequestDuration, httpRequestTotal };

```

### Custom Business Metrics Collector

```typescript
import { Gauge, Counter } from "prom-client";

class BusinessMetrics {
  private activeUsers = new Gauge({
    name: "business_active_users",
    help: "Number of currently active users",
    labelNames: ["plan"],
  });

  private revenue = new Counter({
    name: "business_revenue_cents_total",
    help: "Total revenue in cents",
    labelNames: ["currency", "product"],
  });

  private searchQueries = new Counter({
    name: "business_search_queries_total",
    help: "Total search queries",
    labelNames: ["hasResults"],
  });

  updateActiveUsers(count: number, plan: string) {
    this.activeUsers.set({ plan }, count);
  }

  recordRevenue(amountCents: number, currency: string, product: string) {
    this.revenue.inc({ currency, product }, amountCents);
  }

  recordSearch(hasResults: boolean) {
    this.searchQueries.inc({ hasResults: hasResults.toString() });
  }
}

export const businessMetrics = new BusinessMetrics();

```

### Grafana Dashboard JSON (Key Panels)

```json
{
  "title": "API Gateway Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(http_requests_total[5m])",
          "legendFormat": "{{method}} {{route}} {{status}}"
        }
      ]
    },
    {
      "title": "Error Rate (%)",
      "type": "stat",
      "targets": [
        {
          "expr": "100 * rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m])",
          "legendFormat": "Error %"
        }
      ],
      "thresholds": {
        "steps": [
          { "color": "green", "value": 0 },
          { "color": "yellow", "value": 1 },
          { "color": "red", "value": 5 }
        ]
      }
    },
    {
      "title": "P99 Latency",
      "type": "graph",
      "targets": [
        {
          "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
          "legendFormat": "p99 {{route}}"
        }
      ]
    },
    {
      "title": "Active Connections",
      "type": "gauge",
      "targets": [
        {
          "expr": "active_connections",
          "legendFormat": "Connections"
        }
      ]
    }
  ]
}

```

### Prometheus Alert Rules

```yaml
# prometheus/alerts.yml
groups:

  - name: application_alerts
    rules:

      - alert: HighErrorRate
        expr: |
          100 * rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}% for {{ $labels.route }}"
          runbook_url: "https://wiki/runbooks/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency exceeds 2s"
          description: "Route {{ $labels.route }} p99 is {{ $value }}s"

      - alert: InstanceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Instance {{ $labels.instance }} is down"

      - alert: HighMemoryUsage
        expr: |
          (process_resident_memory_bytes / 1024 / 1024) > 500
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}MB"

```

### Uptime Monitoring Setup

```typescript
import { register, Gauge } from "prom-client";

interface UptimeCheck {
  name: string;
  url: string;
  expectedStatus: number;
  timeout: number;
}

const uptimeGauge = new Gauge({
  name: "uptime_check_success",
  help: "Whether the uptime check succeeded (1) or failed (0)",
  labelNames: ["target"],
});

const latencyGauge = new Gauge({
  name: "uptime_check_latency_seconds",
  help: "Uptime check latency in seconds",
  labelNames: ["target"],
});

async function checkUptime(check: UptimeCheck): Promise<void> {
  const start = Date.now();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), check.timeout);

    const response = await fetch(check.url, { signal: controller.signal });
    clearTimeout(timeoutId);

    const latency = (Date.now() - start) / 1000;
    const success = response.status === check.expectedStatus ? 1 : 0;

    uptimeGauge.set({ target: check.name }, success);
    latencyGauge.set({ target: check.name }, latency);

    if (!success) {
      console.error(`Uptime check failed: ${check.name} returned ${response.status}`);
    }
  } catch (err) {
    uptimeGauge.set({ target: check.name }, 0);
    latencyGauge.set({ target: check.name }, (Date.now() - start) / 1000);
    console.error(`Uptime check failed: ${check.name}`, err);
  }
}

// Run checks every 30 seconds
const checks: UptimeCheck[] = [
  { name: "api-gateway", url: "https://api.example.com/health", expectedStatus: 200, timeout: 5000 },
  { name: "auth-service", url: "https://auth.example.com/health", expectedStatus: 200, timeout: 5000 },
  { name: "payment-service", url: "https://payments.example.com/health", expectedStatus: 200, timeout: 5000 },
];

setInterval(() => {
  checks.forEach(checkUptime);
}, 30_000);

```

## Real-World Use Cases

1. **SLO monitoring**: Track 99.9% uptime SLA with error budget burn rate alerts

2. **Capacity planning**: Monitor CPU/memory trends to predict when to scale

3. **Database monitoring**: Track query latency, connection pool usage, replication lag

4. **Queue depth monitoring**: Alert when message queue (SQS, RabbitMQ) grows beyond threshold

5. **Deployment verification**: Compare error rates before/after a deploy (canary analysis)

6. **Cost monitoring**: Track API calls to expensive third-party services

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Alert fatigue (too many alerts) | Team ignores all alerts | Only alert on actionable conditions with clear runbooks |
| Missing label cardinality control | High-cardinality labels explode TSDB storage | Limit label values (no userId, no requestId as labels) |
| No dashboards for SLOs | Can't track business commitments | Build SLO dashboards from day one |
| Using gauges for rates | Misleading spikes | Use counters + `rate()` in PromQL |
| Alerting on symptoms only | No root cause context | Include both symptom and cause in alert design |
| Not recording error budgets | Don't know when reliability is at risk | Track error budget burn rate |

## Best Practices

1. **RED method** — monitor Rate, Errors, Duration for every service

2. **USE method** — monitor Utilization, Saturation, Errors for infrastructure

3. **Four Golden Signals** — latency, traffic, errors, saturation (Google SRE)

4. **SLI/SLO framework** — define Service Level Indicators and Objectives before building dashboards

5. **Alert on burn rate** — not raw thresholds — to reduce false positives

6. **Label carefully** — high cardinality labels (userId, requestId) cause storage explosion

7. **Use recording rules** — precompute expensive PromQL queries for dashboards

8. **Version your dashboards** — store Grafana JSON in git

9. **Runbook links in alerts** — every alert should link to a diagnosis guide
10. **Regular review** — prune unused metrics and stale alerts quarterly

## Performance Considerations

- **Metrics exposition overhead** — registering many metrics increases `/metrics` scrape time; keep metric count under ~500 per service
- **Histogram bucket choice** — too many buckets increase storage; choose buckets based on your latency SLO
- **Label cardinality** — each unique label combination creates a new time series; a `userId` label with 1M users = 1M series
- **Scrape interval** — 15s is standard; shorter intervals increase storage without proportional value
- **Retention** — Prometheus stores ~15 days by default; use Thanos/Mimir for long-term storage

## Interview Questions

### Beginner

1. **What are the four golden signals of monitoring?**

   - Latency (time to serve requests), Traffic (requests per second), Errors (error rate), Saturation (how full resources are).

2. **What is the difference between a counter and a gauge?**

   - A counter only increases (total requests). A gauge can go up or down (current memory, active connections).

3. **What is Prometheus and how does it collect metrics?**

   - Prometheus is a time-series database that scrapes `/metrics` endpoints on a configurable interval (pull model). It stores metrics locally and supports PromQL for querying.

4. **Why shouldn't you use high-cardinality labels?**

   - Each unique label value creates a new time series. Labels like `userId` with millions of values cause storage explosion and slow queries.

5. **What is the RED method?**

   - Rate (requests/second), Errors (error rate), Duration (latency). Applied to every service for uniform observability.

### Intermediate

6. **Explain the difference between a histogram and a summary.**

   - Both measure distributions. Histograms aggregate on the server side (Prometheus), allowing cross-instance quantile calculations. Summaries compute quantiles client-side, which is less flexible but doesn't require server-side aggregation.

7. **How would you set up alerting for an SLO of 99.9% availability?**

   - Define SLI (success rate = non-5xx responses / total requests). Calculate error budget (0.1%). Alert when burn rate exceeds threshold (e.g., burning error budget 14.4x in 1h means exhausting in 1 week).

8. **What is a PromQL recording rule and when would you use it?**

   - Recording rules precompute PromQL expressions and save results as new metrics. Use for expensive queries needed on dashboards (e.g., complex aggregations over large time ranges).

9. **How do you monitor a message queue system?**

   - Track queue depth (gauge), consumer lag (gauge), processing rate (counter), and error rate (counter). Alert when queue depth exceeds threshold or consumer lag grows.

10. **What is the USE method?**

    - Utilization (percentage of resource in use), Saturation (queue depth / wait time), Errors (error count). Applied to infrastructure resources (CPU, memory, disk, network).

### Senior

11. **Design a monitoring strategy for a microservices system.**

    - Standardize on RED metrics per service. Deploy Prometheus with federation or Thanos for scale. Build dashboards per service and cross-service. Implement SLO-based alerting with burn rate. Use recording rules for dashboard performance. Store long-term metrics in Thanos/Mimir.

12. **Your P99 latency alert fires at 3am. Walk through your investigation.**

    - Check Grafana dashboard for which service/route is slow. Compare before/after deploy timeline. Check CPU/memory saturation. Review recent config changes. Check dependency latency (DB, cache, external APIs). Check for traffic spikes. Use distributed trace to find the slow span.

13. **How do you handle metric explosion in a large system?**

    - Control label cardinality at instrumentation time. Use metric aggregation at the edge (OpenTelemetry Collector). Set retention policies per metric. Use Prometheus remote write with downsampling. Audit metrics quarterly to remove unused ones.

14. **Explain error budget burn rate and why it's better than simple threshold alerts.**

    - Burn rate = how fast you're consuming your error budget. A 99.9% SLO with 1h window burn rate of 14.4x means you'll exhaust budget in 1 week. This accounts for traffic volume — a 1% error rate on low traffic is less urgent than on high traffic. Reduces false positives compared to static thresholds.

15. **Design a canary deployment monitoring system.**

    - Deploy new version to small percentage of traffic. Compare error rate, latency, and business metrics between canary and baseline. Use statistical significance testing. Auto-promote if metrics are within thresholds, auto-rollback if degraded. Use Flagger or Argo Rollouts.

### FAANG-style

16. **If you could only monitor 3 metrics for a web service, what would they be?**

    - Request rate (traffic), error rate (reliability), P99 latency (user experience). These cover the RED method and give immediate visibility into service health.

17. **How would you detect a slow database query that's degrading performance?**

    - Instrument database query duration as a histogram. Create an alert on p99 query latency. Use query-level labels to identify slow queries. Enable slow query logging for threshold-based capture. Use pg_stat_statements or equivalent.

18. **Your system shows 0% error rate but users report issues. What's happening?**

    - Errors might be happening outside instrumentation (client-side, network). Check client-side monitoring. Check for partial failures (200 responses with error bodies). Check timeout behavior (requests succeeding but slowly). Check for data correctness issues (200 OK but wrong data).

19. **Design a cost-effective monitoring stack for a startup.**

    - Start with Prometheus + Grafana (free). Use Loki for logs (cheaper than ELK). Use Tempo for traces. Instrument with OpenTelemetry. Keep metric retention short (15 days). Use cloud-managed alternatives (CloudWatch, Datadog) only if team can't maintain infra.

20. **How do you monitor the monitoring system itself?**

    - Monitor Prometheus/Grafana scrape success, storage usage, query latency. Use blackbox exporters for external checks. Run a separate monitoring stack (meta-monitoring). Alert on monitoring gaps (no metrics for a service for >5 minutes).

### Follow-ups

21. **What's the difference between Prometheus pull model vs push model (StatsD)?**

    - Pull: Prometheus scrapes targets — simple, service doesn't need to know Prometheus address, but requires network accessibility. Push: services push metrics (StatsD, Pushgateway) — simpler firewall config, but services need to know collector address and can lose data during outages.

22. **How do you handle metric collection in Kubernetes?**

    - Use Prometheus operator with ServiceMonitor CRDs. Deploy node-exporter as DaemonSet. Use kube-state-metrics for cluster objects. Auto-discover pods with label selectors. Use admission webhooks for annotation-based scraping.

23. **When would you use Grafana over Kibana for monitoring?**

    - Grafana for time-series metrics (Prometheus, InfluxDB). Kibana for log analytics (Elasticsearch). Grafana can also query Loki for logs. For a unified view, use Grafana as the single pane with Prometheus, Loki, and Tempo as backends.

24. **How do you test alerting rules before deploying them?**

    - Use Promtool to validate rules: `promtool check rules alerts.yml`. Use promtool test to simulate scenarios. Dry-run against historical data. Use Grafana alert provisioning for testing. Deploy to staging first with synthetic traffic.

25. **What metrics would you track for a database?**

    - Connection pool (active, idle, waiting), query latency (p50, p95, p99), replication lag, cache hit ratio, disk I/O, locks, transactions per second, deadlocks, table bloat.

## Summary

Monitoring transforms raw metrics into actionable visibility. Use the RED/USE/Four Golden Signals frameworks to ensure comprehensive coverage. Instrument with Prometheus, visualize with Grafana, and alert with SLO-based burn rates. Control label cardinality, version dashboards, and maintain alert hygiene to keep the system useful.

## References & Learn More

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Google SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [The USE Method](https://www.brendangregg.com/usemethod.html)
- [The RED Method](https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/)
- [PromQL for Humans](https://timber.io/blog/promql-for-humans/)
- [Alerting Best Practices](https://sre.google/workbook/alerting-on-slos/)
