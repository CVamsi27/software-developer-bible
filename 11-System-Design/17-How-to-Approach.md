---
section: System Design
category: Architecture
tags: [guide]
---

# How to Approach Any System Design Problem

## TL;DR

System-design interviews are scored on **structure, trade-off reasoning, and follow-up depth** — not on producing the one "right" design. Use a 4-phase loop: (1) clarify scope, (2) estimate scale, (3) sketch high-level architecture, (4) deep-dive the bottleneck, then iterate on follow-ups.

**Why it matters:** Every senior interview (FAANG, high-growth startup, staff-level) gates on this skill. The candidate who structures the conversation, names trade-offs out loud, and drives the design forward is the one who gets the offer — even if a "better" architecture exists that they never reached.

## Requirements

### Functional Requirements (clarify first)

Always start by listing the 3–7 user-visible features the system must support, plus 2–3 explicitly-out-of-scope items.

### Non-Functional Requirements (clarify second)

Pin down the SLOs that will drive every later decision:

- Scale: requests/sec, storage, bandwidth
- Latency: p50, p95, p99
- Availability: 99.9% (3 nines, ~9 hr/yr downtime) vs 99.99% (4 nines, ~53 min/yr) vs 99.999% (5 nines, ~5 min/yr)
- Consistency: strong, causal, eventual?
- Durability: how many 9s of data durability?
- Multi-region? Read replicas in other continents?
- Compliance: GDPR, HIPAA, PCI-DSS, SOC 2?

## How It Works

### The 4-Phase Framework

```text
┌─────────────────────────────────────────────────────────────┐
│              SYSTEM DESIGN INTERVIEW FRAMEWORK              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: CLARIFY       (5 min)                              │
│  ├── List functional requirements (3-7)                      │
│  ├── Pin down NFRs (scale, latency, availability)            │
│  └── State explicit out-of-scope items                       │
│                                                              │
│  Phase 2: ESTIMATE      (5 min)                              │
│  ├── DAU → QPS (peak = ~2x average)                          │
│  ├── Storage = rows × size × retention                       │
│  ├── Bandwidth = QPS × payload                               │
│  └── Pick the right shape (cache? queue? sharding?)          │
│                                                              │
│  Phase 3: HIGH-LEVEL    (5-10 min)                           │
│  ├── Draw boxes: client, LB, app, cache, DB, queue, workers  │
│  ├── Mark data flow with arrows                              │
│  ├── Identify read/write paths                               │
│  └── Mark trust boundaries (auth, rate limit)                │
│                                                              │
│  Phase 4: DEEP-DIVE     (20-25 min)                          │
│  ├── Drill the bottleneck the interviewer cares about        │
│  ├── Discuss trade-offs, not "best practices"                │
│  └── End with monitoring/operational concerns                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: Clarify (5 minutes)

The biggest signal you can send: **you don't jump to a database choice**. Senior candidates use the first 5 minutes to scope the problem and the SLOs. Ask:

- "What's the most important feature here — the one we must not get wrong?"
- "Is this for global users or one region?"
- "How fresh does data need to be? Read-your-writes? Eventual?"
- "What's the budget? Is this a 3-person team or 30?"
- "Should I optimize for latency or for cost?"

Then state the scope back to the interviewer. This single act converts 50% of mid-level candidates to senior-level signal.

### Phase 2: Capacity Estimation (5 minutes)

Use the **back-of-the-envelope numbers** (see table below) to size the system. You don't need exact numbers — you need orders of magnitude and a sense of which dimension is dominant.

| Constant | Value |
|---|---|
| 1 day | 10^5 seconds |
| 1 month | 2.5 × 10^6 seconds |
| 1 KB | 10^3 bytes; 1 MB = 10^6; 1 GB = 10^9; 1 TB = 10^12 |
| Read : Write ratio | 100:1 typical for social/web, 1:1 for messaging |
| Peak QPS | ~2–5× average |
| Reasonable single-DB throughput | 5K–20K QPS (sharded: 100K+) |
| Reasonable single-Redis throughput | 100K+ QPS |
| Reasonable single-cache miss latency | 1–5 ms |
| Cross-AZ RTT | 1–2 ms |
| Cross-region RTT | 50–150 ms |

Worked example (URL shortener):

- 100M URLs/day created → 100M / 10^5 = 1,000 writes/sec average → 2K/sec peak
- 1B redirects/day → 10K reads/sec average → 30K/sec peak
- 5-year retention × 500 bytes/URL × 100M/day × 365 = ~90 TB

### Phase 3: High-Level Architecture (5–10 minutes)

Draw the boxes. Use the **Client → LB → App → Cache → DB** spine as the default, then add what the problem demands:

| Problem needs | Add |
|---|---|
| Async work (email, video encoding) | Queue (Kafka / SQS) + Workers |
| Search / ranking | Search index (Elasticsearch / OpenSearch) |
| Full-text + facets | Same as above, but discuss indexing pipeline |
| Object storage | S3 / GCS / MinIO for blobs |
| Time-series data | TSDB (Prometheus, InfluxDB, TimescaleDB) |
| Caching | Redis / Memcached, multi-tier |
| Geo distribution | Multi-region, edge CDN, geo-DNS |
| Long-running jobs | Job queue (Sidekiq, Temporal, Airflow) |
| ML inference | Feature store + model server (Triton, BentoML) |

Always label the **read path** and the **write path** separately on the diagram — it makes the design legible in one glance.

### Phase 4: Deep-Dive (20–25 minutes)

The interviewer will guide you here. The two most common deep-dives:

1. **Data model + consistency** — How do you shard? What are the indexes? How do you handle concurrent updates?
2. **Hot path / scale-out** — How does the system handle a celebrity, a flash sale, a 10× traffic spike?

For each, name **2–3 trade-offs** and pick one with a clear reason. The senior-level tell is *naming the option you didn't pick and why*.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Jumping to "let's use Cassandra" | First derive the access pattern, then justify the store |
| Drawing every microservice in 5 minutes | Start with 3–5 boxes; split only when the interview asks |
| Using every tech buzzword | Pick a stack and explain it; don't name 12 databases |
| Skipping the numbers | Always show estimation work — it grounds the design |
| Ignoring the write path | Most designs only optimize reads; flag this proactively |
| No monitoring/alerting section | End every design with: metrics, logs, traces, on-call |
| "It depends" without follow-up | Always resolve: state the dependency, then pick |
| Forgetting cost | Flag bandwidth, storage, and compute as a constraint |

## Best Practices

1. **Drive the conversation** — Senior candidates use phrases like "Let me start with the requirements" and "The riskiest part of this design is X, so I'll deep-dive there next."
2. **State trade-offs out loud** — "We could use Postgres here, but with 100K writes/sec we'd need sharding. DynamoDB gives us that for free at the cost of weaker transactions."
3. **Start simple, then iterate** — A 3-box design that the interviewer can challenge is better than a 15-box design that no one can read.
4. **Anchor in numbers** — Always connect a decision to "we expect 30K reads/sec, so we need a read replica per AZ" or similar.
5. **Name the failure modes** — "If Redis is down, we degrade to DB-only with a circuit breaker — this is the 99.9% case; the cache hit path is the 99.99%."
6. **Close with operations** — "How do we know this is healthy?" — metrics, alerts, SLO dashboards, on-call playbook.
7. **Listen for hints** — When the interviewer says "what about X?" they are giving you the next deep-dive topic. Take it.

## Real-World Use Cases

- **FAANG on-site loop**: 45 minutes, one of the canonical problems (URL shortener, news feed, chat, video, etc.). Score = structure + depth + trade-off reasoning.
- **Staff / principal loop**: 60 minutes, often an open-ended domain ("design a hospital system for a new country") where the *clarification* phase is 15 minutes and the deep-dive is 40.
- **Take-home design doc**: 2–4 hours, written format. Same structure applies but you can be more thorough.

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Hot keys in cache | Single instance saturates | Consistent hashing + replica factor |
| Celebrity skew | One user generates 30% of writes | Split hot/cold paths; per-key rate limits |
| Network RTT | 100ms RTT = 100ms p50 floor | Edge cache, prefetch, request coalescing |
| DB connection storms | Cascade failure after deploy | Pool sizing + jitter + circuit breakers |
| GC pauses in app tier | Tail latency spike | Use Go/Rust for hot paths, jvm tuning, off-heap |

## Summary

- **Frame**: 4-phase loop — Clarify → Estimate → High-Level → Deep-Dive.
- **Time-box**: 5 + 5 + 10 + 25 minutes.
- **Style**: State trade-offs out loud, name what you didn't pick and why.
- **Anchor**: Always show numbers; always end with operations.
- **Senior signal**: You drive the conversation; you don't wait for the interviewer to ask.

## Cheat Sheet

```text
SYSTEM DESIGN CHEAT SHEET
═══════════════════════════════════════
PHASES (45-min loop):
  1. Clarify (5m)   — list 3-7 features, pin NFRs
  2. Estimate (5m)  — QPS, storage, bandwidth
  3. High-Level (10m) — boxes + arrows
  4. Deep-Dive (25m) — bottleneck, trade-offs

KEY NUMBERS:
  - 1 day = 10^5 sec, 1 month = 2.5×10^6 sec
  - peak QPS = 2-5x average
  - single DB = 5K-20K QPS, single Redis = 100K+
  - cross-AZ RTT 1-2ms, cross-region 50-150ms

SENIOR SIGNALS:
  - State trade-offs out loud
  - End with monitoring/operations
  - Don't jump to a database
  - Name failure modes
  - Drive the conversation

```

---

## See Also
- [API Gateway](../12-Microservices/02-API-Gateway.md)
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [System Design Interview Questions](16-Interview-Questions.md)
- [URL Shortener](01-URL-Shortener.md)

## References & Learn More

- [System Design Primer (donnemartin)](https://github.com/donnemartin/system-design-primer)
- [Alex Xu — System Design Interview Vol 1 & 2](https://bytebytego.com/)
- [Designing Data-Intensive Applications — Martin Kleppmann](https://dataintensive.net/)
- [System Design Interview Questions — Hello Interview](https://www.hellointerview.com/)
- [Pragmatic System Design — Alex Xu YouTube](https://www.youtube.com/c/ByteByteGo)
