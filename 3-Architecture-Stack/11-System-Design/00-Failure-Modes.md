---
section: System Design
category: Architecture
tags: [concept, distributed-systems, reliability, theory]
---

# Failure Modes

> **Everything fails. Plan for it.** The "failure modes" question is the #1 thing senior engineers care about in a system design. If you can't answer "what if X fails" for every component, you can't design a reliable system.

## TL;DR

- **Hardware fails:** disk, RAM, network, power, datacenter.
- **Software fails:** bugs, memory leaks, slow GC, deadlocks, race conditions.
- **Network fails:** partitions, slow links, packet loss, BGP issues.
- **Humans fail:** misconfigurations, deploys, mistakes.
- **Plan for each:** redundancy, retries, circuit breakers, fallbacks, observability.
- **In interviews: for every component, ask "what if it fails?" and explain the mitigation.**

---

## Why it matters

Every "reliable" or "highly available" or "production" system is built on understanding failure modes. If you don't know what fails and how, you can't design a system that survives.

This is the difference between:
- Junior: "It works"
- Senior: "It works, and when X fails, it falls back to Y"

---

## The Failure Modes

### Hardware

| Failure | Mitigation |
|---------|------------|
| **Disk failure** | RAID, replication, backups |
| **RAM failure** | ECC memory, redundant servers |
| **CPU failure** | Redundant servers, hot spare |
| **Network card failure** | Bonded NICs, dual switches |
| **Power supply failure** | Dual PSUs, UPS, generator |
| **Datacenter failure** | Multi-region deployment, backup datacenter |
| **Server failure** | Replication, auto-scaling, health checks |

### Software

| Failure | Mitigation |
|---------|------------|
| **Bug in new release** | Canary deploys, blue-green, feature flags, rollback |
| **Memory leak** | Restart on OOM, monitor memory, fix the bug |
| **Slow GC** | Tune GC, monitor pause times, use off-heap |
| **Deadlock** | Timeouts, detect and restart, fix the bug |
| **Race condition** | Locks, transactions, idempotency, fix the bug |
| **CPU spike** | Auto-scale, rate limiting, load shedding |
| **Thread pool exhaustion** | Bounded queues, monitoring, async I/O |
| **Database connection pool exhausted** | Connection pool sizing, timeouts, monitor |
| **Cache miss storm** | Refresh-ahead, stale-while-revalidate |

### Network

| Failure | Mitigation |
|---------|------------|
| **Network partition** | Quorum, multi-region, eventual consistency |
| **Packet loss** | TCP retries, application-level retries |
| **Slow link** | Timeouts, circuit breakers, fallbacks |
| **DNS failure** | Cached DNS, multiple DNS providers, IP fallback |
| **BGP hijack** | BGP monitoring, RPKI, multi-provider |
| **CDN failure** | Direct origin, multiple CDNs |
| **DDoS** | CDN/WAF, rate limiting, scrubbing services |

### External services

| Failure | Mitigation |
|---------|------------|
| **Payment provider down** | Queue payments, retry, fall back to secondary provider |
| **Email service down** | Queue emails, retry, fall back to secondary |
| **OAuth provider down** | Cached tokens, fall back to local auth |
| **Cloud provider outage** | Multi-cloud or multi-region (expensive, rare) |

### Humans

| Failure | Mitigation |
|---------|------------|
| **Bad deploy** | CI/CD with tests, canary, rollback, change advisory |
| **Misconfiguration** | Config management, code review, change windows |
| **Accidental data deletion** | Backups, soft delete, audit log, recovery process |
| **Runbook gap** | Incident postmortems, runbook updates, on-call training |
| **Alert fatigue** | Tuning alerts, deduplication, escalation policies |

---

## The "What if X fails?" Framework

For every component in your system, ask:

1. **What if it fails entirely?**
2. **What if it fails partially (degraded mode)?**
3. **What if it's slow (not failed, but bad)?**
4. **What if it's wrong (returns bad data)?**
5. **What if it's a security incident?**

Then design mitigations for each.

**Example: Database**

| Failure | Mitigation |
|---------|------------|
| DB fails entirely | Failover to replica. If no replica, queue writes. |
| DB fails partially (slow) | Read from replica. Return stale data. |
| DB is slow | Add timeout. Circuit breaker. Return cached. |
| DB returns wrong data | Validation. Consistency checks. |
| DB is hacked | Encryption at rest. Audit log. Restore from backup. |

**Example: API Server**

| Failure | Mitigation |
|---------|------------|
| Server dies | Load balancer routes to healthy server |
| Server is slow | Health check fails, traffic shifted |
| Server has bug | Canary deploy catches it, rolled back |
| Server is hacked | Rate limiting, WAF, auth, audit |

---

## Specific Patterns for Failure

### 1. Retries with exponential backoff

Don't retry immediately. Wait 1s, 2s, 4s, 8s, 16s. With jitter to prevent thundering herd.

```
attempt 1: try
attempt 2: wait 1s + random(0-100ms), try
attempt 3: wait 2s + random(0-200ms), try
...
give up after 5 attempts
```

### 2. Circuit breaker

If a service is failing, stop calling it. Try again later.

```
CLOSED: normal operation, count failures
  if failures > threshold:
    → OPEN: reject all calls for 30s
OPEN: reject all calls
  after 30s:
    → HALF_OPEN: allow one test call
HALF_OPEN: allow one test call
  if success:
    → CLOSED
  if failure:
    → OPEN
```

**Used by:** Hystrix (Netflix, deprecated), Resilience4j, Polly (.NET), Istio (service mesh)

### 3. Bulkhead

Isolate resources so one failure doesn't take down everything.

```
User-facing service:
  - Thread pool for critical API: 100 threads
  - Thread pool for /search: 50 threads
  - Thread pool for /recommendations: 20 threads

If /search hangs, it only exhausts its 50 threads, not the 100 critical ones.
```

### 4. Timeout everywhere

Every external call needs a timeout. Otherwise a slow service can pin your threads.

```
DB query: 5s timeout
HTTP call: 10s timeout
Cache read: 100ms timeout
```

### 5. Graceful degradation

When a component fails, serve something rather than nothing.

```
Recommendation service down → show "Popular" instead of "Recommended for you"
Map service down → show list of locations instead of map
Search service down → show cached results
```

### 6. Chaos engineering

Deliberately break things in production to test failure handling.

- Netflix Chaos Monkey: randomly kill EC2 instances
- AWS Fault Injection Service: simulate AZ failures
- Gremlin: chaos engineering platform

### 7. Backups and disaster recovery

- Regular backups (daily)
- Tested restoration (every quarter)
- Multi-region for true DR
- Recovery Time Objective (RTO): how long can you be down?
- Recovery Point Objective (RPO): how much data can you lose?

---

## Failure Mode Catalog

Here are common failure modes you should be able to discuss:

### 1. Network partition

**What:** Two parts of the system can't talk to each other.

**Effect:** Some nodes can't reach others. Can lead to split brain, lost writes, inconsistency.

**Mitigation:** Quorum (only majority can serve), CAP trade-off, multi-region, partition-tolerant algorithms.

### 2. Split brain

**What:** Two nodes both think they're the leader.

**Effect:** Both accept writes. When partition heals, conflict.

**Mitigation:** Quorum, fencing tokens, leader lease with timeout, witness/arbiter.

### 3. Cascading failure

**What:** Service A fails, which causes B to overload, which fails, which causes C to fail...

**Effect:** Whole system goes down even though only one component failed.

**Mitigation:** Circuit breakers, bulkheads, timeouts, rate limiting, load shedding, capacity planning.

### 4. Thundering herd

**What:** Many requests all hit at once (after a pause, after a cache miss, after a deploy).

**Effect:** Service overload.

**Mitigation:** Jitter on retries, cache stampede protection, rolling deploys, pre-warming.

### 5. Slowloris / Slow client

**What:** A client sends data very slowly, holding a connection open.

**Effect:** Connection pool exhausted.

**Mitigation:** Read timeouts, connection timeouts, max connections per client, request size limits.

### 6. Data corruption

**What:** Bad data ends up in the database (bug, hardware, manual mistake).

**Effect:** Wrong results, downstream errors.

**Mitigation:** Validation, audit log, backups, restore process, schema constraints.

### 7. Runaway process

**What:** A bug causes a process to consume 100% CPU/memory.

**Effect:** Service slow or down.

**Mitigation:** Resource limits (cgroups, Kubernetes limits), monitoring, restart on OOM, kill on stuck.

### 8. Deadlock

**What:** Two processes hold locks the other needs.

**Effect:** Both hang forever.

**Mitigation:** Timeouts, lock ordering, deadlock detection, retry on conflict.

### 9. Cache poisoning

**What:** Bad data in the cache, served to all users.

**Effect:** Wrong results across the system.

**Mitigation:** Validation on read, schema for cache entries, short TTL for risky data.

### 10. DNS failure

**What:** DNS resolution fails (DNS provider down, cache poisoned).

**Effect:** All services can't find each other.

**Mitigation:** Cached DNS, IP fallback, multiple DNS providers, monitoring.

### 11. TLS/SSL expiration

**What:** Cert expires.

**Effect:** All HTTPS requests fail.

**Mitigation:** Auto-renewal (Let's Encrypt, cert-manager), monitoring, alerts 30 days before expiry.

### 12. Time skew

**What:** Servers' clocks drift.

**Effect:** Auth fails (JWT expired prematurely), distributed systems confused.

**Mitigation:** NTP, monotonic clocks, clock skew tolerance in protocols.

---

## Observability for Failure

You can't fix what you can't see. The 3 pillars:

### 1. Metrics (numbers over time)

- Request rate, error rate, latency (RED)
- Utilization: CPU, memory, disk, network
- Saturation: queue depth, connection pool usage
- Business metrics: orders/sec, signups/sec

**Tools:** Prometheus, Datadog, CloudWatch, Grafana

### 2. Logs (events)

- Structured logs (JSON)
- Request ID for tracing
- Error logs with stack traces
- Log levels: DEBUG, INFO, WARN, ERROR

**Tools:** ELK (Elasticsearch, Logstash, Kibana), Splunk, Loki, CloudWatch Logs

### 3. Traces (request flow)

- Distributed tracing across services
- Span per operation
- Parent-child relationships
- See where time is spent

**Tools:** Jaeger, Zipkin, Datadog APM, Honeycomb, OpenTelemetry

### 4. (Bonus) Real User Monitoring (RUM)

- See what real users experience
- Page load times, JS errors
- Conversion funnels

**Tools:** Sentry, Datadog RUM, New Relic

---

## When to discuss in interviews

For every component, ask "what if it fails?" and explain the mitigation.

**Example: "What if the database fails?"**
- "We have a primary + 2 replicas. If the primary fails, the replicas use Raft to elect a new primary. Failover takes about 10 seconds. During that time, writes are rejected with a clear error. We also have a 1-minute read replica lag, so reads can continue from a replica with eventual consistency."

**Example: "What if the cache fails?"**
- "Cache miss means we read from the DB. The DB can handle 10x current load. If the cache is down for an extended period, we add a circuit breaker: after N cache errors, skip the cache entirely and go direct to DB. The system degrades but doesn't fail."

---

## Anti-patterns

- **Single point of failure.** Every component has a backup, except this one. The one that takes you down.
- **Synchronous calls without timeouts.** A slow service can hang your threads.
- **No retries.** Transient failures become permanent.
- **No circuit breaker.** When a service is down, you keep hammering it.
- **No graceful degradation.** When X fails, the whole system fails. Show *something* instead.
- **No observability.** When something breaks, you have no idea why.
- **No chaos engineering.** You think your failure handling works, but you've never tested it.
- **Manual failover.** If a human has to be paged to recover, you'll have downtime.
- **Untested backups.** You have backups. Have you ever restored from one?

---

## Related concepts

- [00-CAP-Theorem.md](00-CAP-Theorem.md) — partitions are inevitable
- [00-Consensus-and-Leader-Election.md](00-Consensus-and-Leader-Election.md) — how to elect a leader
- [00-Distributed-Transactions.md](00-Distributed-Transactions.md) — saga for multi-service
- [../../40-Platform-Stack/22-Observability/](../../40-Platform-Stack/22-Observability/) — observability
- [../../40-Platform-Stack/14-Kubernetes/](../../40-Platform-Stack/14-Kubernetes/) — K8s failure handling

---

## TL;DR

- **Hardware, software, network, humans all fail. Plan for each.**
- **For every component, ask "what if it fails?" and name the mitigation.**
- **Patterns:** retries, circuit breakers, bulkheads, timeouts, graceful degradation, chaos engineering.
- **Observability is mandatory:** metrics + logs + traces.
- **Test your failure handling:** chaos engineering, game days, fire drills.
- **In interviews: name specific failure modes, name specific mitigations.**

For case studies, see [02-WhatsApp.md](02-WhatsApp.md) (message delivery failure handling), [06-Payment-Gateway.md](06-Payment-Gateway.md) (payment provider failure), [15-Chat-System.md](15-Chat-System.md) (WebSocket failure handling), [22-Distributed-Counter.md](22-Distributed-Counter.md) (consensus for hot keys).
