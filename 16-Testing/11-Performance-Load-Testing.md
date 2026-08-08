---
section: Testing
category: Quality
tags: [concept, reference]
---

# Performance & Load Testing

## Definition

**Performance testing** measures how a system behaves under load — speed, stability, scalability, and resource consumption. It has four common variants:

- **Load testing** — expected traffic (e.g., 1,000 concurrent users during business hours) to validate SLAs.
- **Stress testing** — beyond expected load to find the **breaking point** and observe graceful degradation.
- **Spike testing** — sudden bursts (e.g., 10x traffic in 10s) to validate autoscaling and queue capacity.
- **Soak / endurance testing** — sustained moderate load over hours/days to surface **memory leaks, connection pool exhaustion, and log rotation bugs**.

The 2024+ toolchain has consolidated around **k6** (Go-based, JS scripting, CI-friendly) and **Artillery** (YAML/Node, cloud offering). **Gatling** remains strong in JVM shops, **Locust** in Python shops, and **JMeter** in legacy enterprise.

## TL;DR

Performance tests answer **"will this break under our real-world load?"** — a question unit/integration tests can't. The methodology: define **SLAs** (p95 latency, error rate, throughput), script realistic user flows with **ramp-up + steady-state + ramp-down**, observe **percentiles** (p50, p95, p99 — never averages), and watch **saturation signals** (CPU, memory, DB connection pool, queue depth). Senior engineers run these in **staging pre-prod** on every release and after any architectural change.

## Why it matters

Senior interviews for backend or full-stack roles increasingly include **"how would you validate that a service can handle 10K req/s?"** or **"walk me through debugging a production slowdown."** Strong candidates discuss the **SLO/SLA triangle** (latency vs. throughput vs. error rate), why **averages lie** (p99 is the user experience at the tail), **Little's Law** (concurrency = throughput × latency), and **the four golden signals** (latency, traffic, errors, saturation). Tool choice matters less than methodology: define the question, design the scenario, measure, then act.

## Why Do We Need It?

- **Validate SLAs**: Confirm the system meets p95/p99 latency and error-rate commitments
- **Find breaking points**: Discover where the system actually fails (not where you assume)
- **Tune capacity**: Right-size instances, DB connections, and queues before launch
- **Catch regressions**: Detect perf degradation introduced by code or config changes
- **Validate autoscaling**: Confirm HPA/VPA triggers fire at the right thresholds
- **Surface memory leaks**: Soak tests catch leaks that short unit tests never see
- **De-risk launches**: Avoid the "we celebrated launch, then got paged at 2am" cycle
- **Cost optimization**: Smaller instances at the right size = lower cloud bill

## How It Works

```text
┌──────────────────────────────────────────────────────────────────┐
│                  PERFORMANCE TEST PIPELINE                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │  Script  │──▶│  Runner  │──▶│  System  │──▶│ Metrics  │      │
│  │  (k6)    │   │ (k6 OSS) │   │ Under    │   │ (Influx/ │      │
│  │          │   │          │   │  Test    │   │  Prom)   │      │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘      │
│        │              │              │              │            │
│        │              │              │              ▼            │
│        │              │              │      ┌──────────────┐    │
│        │              │              │      │ Thresholds   │    │
│        │              │              │      │ pass/fail    │    │
│        │              │              │      └──────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### Test Stages

```text
Load (RPS)
   │
   │            ┌───────────────────────┐
   │           /│     Steady-State      │\
   │          / │  (validate SLAs)      │ \
   │         /  └───────────────────────┘  \
   │        /                                \
   │       / Ramp-Up  ────▶  Hold  ────▶  Ramp-Down  \
   │      /                                          \
   │_____/                                            \_____
   0     2m                5m                    2m      Time
```

## Tools Comparison

| Tool | Language | Strengths | When to Use |
|------|----------|-----------|-------------|
| **k6** | Go (runs) + JS (scripts) | Fast, CI-friendly, modern API, cloud offering | Default choice for most teams in 2025+ |
| **Artillery** | Node.js (YAML/JS) | Declarative, easy WebSocket/SSE tests | Quick HTTP/WebSocket smoke tests |
| **Gatling** | Scala (scripts) | High throughput, detailed reports | JVM shops, enterprise Java/Scala stacks |
| **Locust** | Python | Distributed by design, code-based | Python shops, complex user behavior |
| **JMeter** | Java (GUI) | Legacy enterprise, mature plugins | Brownfield, regulated environments |
| **Vegeta** | Go (CLI) | Constant-rate attack mode | Quick API saturation probing |
| **wrk** | C | Ultra-light, scripted in Lua | Micro-benchmarks, low-level validation |

## Code Examples

### k6 — Realistic User Flow with Thresholds

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const loginErrorRate = new Rate('login_errors');
const checkoutLatency = new Trend('checkout_latency', true);

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // ramp-up to 100 VUs
    { duration: '5m', target: 100 },   // hold at 100 VUs
    { duration: '3m', target: 500 },   // ramp to 500 VUs (stress)
    { duration: '5m', target: 500 },   // hold at 500 VUs
    { duration: '2m', target: 0 },     // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1500'],   // p95 < 500ms, p99 < 1.5s
    http_req_failed:   ['rate<0.01'],                  // < 1% errors
    login_errors:      ['rate<0.005'],                 // < 0.5% login errors
    checkout_latency:  ['p(95)<2000'],                 // checkout p95 < 2s
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.example.com';

export default function () {
  group('1. Login', () => {
    const loginRes = http.post(`${BASE_URL}/api/login`, JSON.stringify({
      email: `user${__VU}@example.com`,
      password: 'test-password',
    }), { headers: { 'Content-Type': 'application/json' } });

    const ok = check(loginRes, {
      'login status is 200': (r) => r.status === 200,
      'has auth token': (r) => r.json('token') !== undefined,
    });
    if (!ok) loginErrorRate.add(1);
  });

  sleep(1);

  group('2. Browse products', () => {
    const res = http.get(`${BASE_URL}/api/products?page=1`);
    check(res, {
      'products status 200': (r) => r.status === 200,
      'has products array': (r) => Array.isArray(r.json('items')),
    });
  });

  sleep(2);

  group('3. Checkout', () => {
    const start = Date.now();
    const res = http.post(`${BASE_URL}/api/checkout`, JSON.stringify({
      cartId: `cart-${__VU}-${__ITER}`,
      paymentMethod: 'card',
    }), { headers: { 'Content-Type': 'application/json' } });

    checkoutLatency.add(Date.now() - start);
    check(res, { 'checkout status 200': (r) => r.status === 200 });
  });

  sleep(3);
}
```

### k6 — Spike Test (Sudden Traffic Burst)

```javascript
// spike-test.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },    // baseline
    { duration: '10s', target: 2000 },  // 40x spike in 10s
    { duration: '3m',  target: 2000 },  // hold the spike
    { duration: '30s', target: 50 },    // back to baseline
    { duration: '1m',  target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<3000'],
    http_req_failed:   ['rate<0.05'],  // 5% errors acceptable during spike
  },
};

export default function () {
  const res = http.get('https://staging.example.com/api/feed');
  check(res, { 'status 200 or 503': (r) => r.status === 200 || r.status === 503 });
}
```

### k6 — Constant Request Rate (vs. VU-based)

```javascript
// constant-rate.js
import http from 'k6/http';

export const options = {
  scenarios: {
    constant_rps: {
      executor: 'constant-arrival-rate',
      rate: 1000,           // 1000 iterations per `timeUnit`
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,  // initial pool
      maxVUs: 500,          // scale if needed
    },
  },
};

export default function () {
  http.get('https://staging.example.com/api/health');
}
```

**Why this matters**: VU-based tests conflate user thinking time with server load. `constant-arrival-rate` guarantees a fixed request rate regardless of latency — the only way to measure true capacity.

### Artillery — YAML Config for HTTP + WebSocket

```yaml
# artillery-config.yml
config:
  target: "https://staging.example.com"
  phases:
    - duration: 60
      arrivalRate: 50      # 50 new users/sec
      name: "Ramp up"
    - duration: 300
      arrivalRate: 200
      name: "Steady state"
  defaults:
    headers:
      Content-Type: "application/json"

scenarios:
  - name: "Browse and add to cart"
    flow:
      - get:
          url: "/api/products"
      - think: 2
      - post:
          url: "/api/cart"
          json:
            productId: "123"
            quantity: 1
      - think: 1
  - name: "WebSocket live chat"
    engine: "ws"
    flow:
      - ws:
          url: "/ws/chat"
          send: '{"type":"join","room":"general"}'
      - think: 5
      - ws:
          send: '{"type":"message","text":"hello"}'
```

```bash
# Run with HTML report
artillery run artillery-config.yml --output report.json
artillery report report.json --output report.html
```

### Locust — Python Code-Based

```python
# locustfile.py
from locust import HttpUser, task, between
import random

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)  # 1-3s think time between tasks

    @task(3)  # weight 3 — more frequent
    def browse_products(self):
        self.client.get(f"/api/products?page={random.randint(1, 20)}")

    @task(1)  # weight 1
    def view_cart(self):
        self.client.get("/api/cart")

    @task(1)
    def checkout(self):
        with self.client.post("/api/checkout", json={
            "cartId": f"cart-{self.user_id}",
            "paymentMethod": "card",
        }, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2.0:
                response.failure("Checkout took > 2s")
```

```bash
locust -f locustfile.py --headless --users 500 --spawn-rate 50 \
  --host https://staging.example.com --run-time 10m
```

## Key Metrics

| Metric | What It Measures | Target (typical) | Why It Matters |
|--------|------------------|------------------|----------------|
| **p50 (median)** | Typical user experience | < 200ms | What "most" users see |
| **p95** | 95th percentile latency | < 500ms | SLA target — what 1 in 20 users experience |
| **p99** | Tail latency | < 1.5s | The "feels broken" threshold |
| **RPS / RPS-per-instance** | Throughput | Varies | Capacity planning input |
| **Error rate** | % failed requests | < 0.1% for 5xx | Reliability signal |
| **Concurrent users** | Active sessions | Capacity-defined | Little's Law: `L = λ × W` |
| **CPU utilization** | Server saturation | < 75% sustained | Headroom for spikes |
| **Memory** | Heap/GC pressure | Stable over time | Leak detection in soak tests |
| **DB connection pool** | Saturation | < 80% | Queueing indicator |
| **GC pause time** | Stop-the-world | < 100ms p99 | Node/Java tail-latency cause |

> **Anti-pattern: using averages.** A 100ms average can hide a 5s p99 that 1% of users see. Always report percentiles.

## Real-World Use Cases

### 1. Pre-Production Capacity Validation

Before launching a new service, run a **capacity test**: ramp to 1.5x expected production traffic, hold for 30 minutes, and verify SLAs hold with headroom. Use the results to right-size the **autoscaling min/max instance counts** and **DB connection pool size**.

### 2. Continuous Performance Regression Detection

```yaml
# .github/workflows/perf.yml
name: Performance Regression
on:
  pull_request:
    paths: ['src/**', 'package.json']

jobs:
  k6:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Spin up preview env
        run: vercel deploy --target=staging
      - name: Run k6 smoke test
        uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/load/smoke.js
        env:
          BASE_URL: ${{ steps.deploy.outputs.url }}
      - name: Compare against baseline
        run: |
          node scripts/compare-perf-baseline.mjs \
            --current current.json \
            --baseline baseline.json \
            --threshold 10  # fail if p95 regresses > 10%
```

The PR fails if p95 latency regresses > 10% from the main-branch baseline. This catches "innocent" PRs that add a single `await db.query()` to a hot path.

### 3. Soak Test for Memory Leaks

```javascript
// soak-test.js
export const options = {
  executor: 'constant-vus',
  vus: 200,
  duration: '4h',  // 4-hour soak
  thresholds: {
    'vus_memory': ['value<512000000'],  // 512MB VU heap
  },
};
```

Run weekly against staging. Memory growth > 5% per hour indicates a leak. A common culprit: closure-bound references in long-lived caches, un-released DB connections, or unbounded `Map`/`Set` in event handlers.

### 4. Third-Party API Chaos Testing

```javascript
// third-party-chaos.js
import http from 'k6/http';
import { check, sleep } from 'k6';

// Simulate payment provider slowdown
const RESPONSES = [
  () => ({ status: 200, body: '{"status":"ok"}' }),
  () => ({ status: 200, body: '{"status":"ok"}' }),
  () => ({ status: 200, body: '{"status":"ok"}' }),
  () => ({ status: 503, body: '{"error":"timeout"}' }),  // 25% failure
  () => null,  // 5% timeout (no response)
];

export default function () {
  const behavior = RESPONSES[Math.floor(Math.random() * RESPONSES.length)];
  // ...injected into the app under test via a mock server
}
```

Wire a chaos proxy (e.g., **Toxiproxy**, **Pumba**, **WiredTiger**) between your service and downstream dependencies to validate **circuit breaker**, **retry budgets**, and **fallback paths** under realistic failure conditions.

## Common Mistakes

### 1. Running Tests Against Production by Accident

```javascript
// ❌ BAD: hardcoded prod URL
const BASE_URL = 'https://api.example.com';
```

Always use a dedicated **staging environment** that mirrors production topology. Run tests in CI, not from a developer's laptop, where the load generator competes with everything else.

### 2. Using VU-based Tests Without Thinking Time

```javascript
// ❌ BAD: 1000 VUs hammering the server back-to-back
export default function () {
  http.get('/api/feed');
}
```

Real users have **think time** between requests. k6 VUs with no `sleep()` are unrealistic — they'll find saturation that real users never hit, while missing the cases that matter.

### 3. Trusting Averages

```text
Average: 250ms
"Looks fine!"

Reality: p50=120ms, p95=400ms, p99=8200ms  ← 1% of users wait 8 seconds
```

Always report p50/p95/p99 in dashboards. Latency distributions are **almost never normal** — they're long-tailed.

### 4. Running One Test, Making Big Decisions

```bash
# ❌ BAD: one test run → "we can handle 10K QPS"
k6 run --vus 1000 --duration 5m load-test.js

# ✅ GOOD: 3-5 runs at different days/times, with cold/warm caches
```

A single run can be skewed by warm-up, GC, or background jobs. Take the **median of 3-5 runs** and watch variance.

### 5. Not Watching Server-Side Metrics

Client-side latency p95 = 500ms doesn't mean much if the **DB CPU is at 95%** or the **connection pool is exhausted**. Always correlate client metrics with server metrics (Prometheus + Grafana dashboards for the test run).

## Best Practices

1. **Test in staging, not production** — except for **shadow traffic** / **dark launches**, which can be done safely.
2. **Use percentile-based SLAs** — p95 < 500ms, error rate < 0.1%, throughput > X RPS.
3. **Run from the right location** — if your users are in EU, run from EU. Use **k6 Cloud** for distributed load generation.
4. **Match the test data shape** — a "100K user" test that only queries 100 rows in the DB isn't a real test.
5. **Warm up before measuring** — JIT, caches, and connection pools need a warm-up phase; don't include cold-start in your numbers.
6. **Correlate with server metrics** — Prometheus + Grafana dashboards during the test run.
7. **Set thresholds as pass/fail gates** — `thresholds: { http_req_duration: ['p(99)<1500'] }` makes the test binary.
8. **Run perf tests in CI on a schedule** (nightly) and on PRs for critical paths.
9. **Test failure modes**, not just happy paths — kill a DB connection, slow down a downstream, exhaust a queue.
10. **Document the results** — "staging can handle 5K RPS p95<300ms on 3 c5.xlarge nodes" is a real capacity claim.

## Performance Considerations

- **Load generator saturation**: A single k6 process tops out around **30-50K RPS**. For higher throughput, distribute with k6 Cloud or run multiple processes in parallel.
- **Network bandwidth**: 1Gbps link can be a bottleneck before the server. Use multiple geographically distributed generators.
- **Test environment parity**: Performance results are only as good as the environment. CPU pinning, instance type, DB version, and even kernel version matter.
- **Time-of-day effects**: Cloud network and shared infra perform differently at 3am vs. 3pm. Run multiple times to capture variance.
- **Cold start vs. warm**: First request after deploy hits cold caches, JIT, and connection pools. Always include a warm-up stage.

## Summary

- Performance testing validates **SLAs under realistic load** — p95/p99 latency, error rate, throughput, saturation
- Four main types: **load** (expected), **stress** (beyond expected), **spike** (sudden burst), **soak** (sustained)
- Modern toolchain: **k6** (default for most teams in 2025+), **Artillery**, **Gatling**, **Locust**, **wrk**
- Always report **percentiles** (p50/p95/p99), never averages — distributions are long-tailed
- Use **constant-arrival-rate** scenarios for true capacity testing, not just VU-based tests
- Run tests in **staging** that mirrors production topology — never in prod (except for dark launches)
- **Soak tests** (hours) catch memory leaks and connection pool exhaustion that short tests miss
- Watch **server-side metrics** alongside client latency — DB CPU, connection pool, queue depth tell the real story
- Set **threshold-based pass/fail gates** so perf regressions block CI
- Senior signal: discuss **Little's Law**, the **four golden signals**, and why averages lie

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Core Web Vitals](../26-Performance-Monitoring/01-Core-Web-Vitals.md)
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [Observability](../22-Observability/)
- [System Design](../11-System-Design/)

## References & Learn More

- [k6 Documentation](https://k6.io/docs/)
- [k6 Scenarios Reference](https://k6.io/docs/using-k6/scenarios/)
- [Artillery Documentation](https://www.artillery.io/docs)
- [Gatling Documentation](https://gatling.io/docs/)
- [Brendan Gregg — Latency](https://www.brendangregg.com/latency.html)
- [Google SRE Book — Ch. 6: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Little's Law: Concurrency = Throughput × Latency](https://en.wikipedia.org/wiki/Little%27s_law)
- [The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)
