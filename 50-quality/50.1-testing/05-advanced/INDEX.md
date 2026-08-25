# Advanced Testing

> **2 files.** Testing beyond correctness: performance/load testing (k6, Artillery, Locust) and chaos engineering — proving the system survives load and failure, not just happy paths.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

The pyramid answers "does it work for one user?" Staff/SRE interviews ask "does it work for ten thousand users while a dependency is on fire?" These two disciplines answer that.

---

## The 2 files

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 01 | [Performance & Load Testing](50.1.5.01-performance-load-testing.md) | k6, Artillery, Locust, p95/p99, ramp-up, stress/soak | Production-scale services | 30 min |
| 02 | [Chaos Engineering & Game Days](50.1.5.02-chaos-engineering.md) | Steady-state hypothesis, blast radius, Toxiproxy, Chaos Monkey, Gremlin, Litmus | Resilient distributed systems | 30 min |

---

## Quick orientation

```text
Question                              Discipline
Does it survive expected peak?   →    Load testing
Where does it break?             →    Stress testing
How does it behave over hours?   →    Soak testing
What if a dependency dies?       →    Chaos engineering
Who fixes it when it does?       →    Game days
```

Both chapters share one principle: measure a **steady-state metric** first (p95 latency, success rate), then perturb the system and compare.

---

## Cross-References

- [Production Engineering](../../50.4-production-engineering/INDEX.md) — SLOs give load/chaos tests their pass/fail line.
- [Observability](../../../40-platform/40.4-observability/INDEX.md) — you cannot chaos-test what you cannot see.
- [Chaos Engineering (production angle)](../../50.4-production-engineering/50.4.03-chaos-engineering.md) — the same discipline from the ops side.

---

## Navigation

[← Mocking & Patterns](../04-mocking-and-patterns/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Interview Prep →](../06-interview-prep/INDEX.md)
