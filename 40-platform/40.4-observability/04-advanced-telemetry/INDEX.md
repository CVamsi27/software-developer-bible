# Advanced Telemetry

> **1 file.** OpenTelemetry — the vendor-neutral standard that unifies traces, metrics, and logs into one instrumentation layer you own instead of your vendors'.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Telemetry-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-in--progress-yellow)](#)

---

## Why this category exists

Instrumenting once per vendor does not survive the second vendor swap. OpenTelemetry standardizes SDKs, the OTLP wire protocol, and context propagation (W3C Trace Context), with a collector pipeline that batches, filters, and samples before export. It is the modern default answer to "how do you instrument services?" and a senior-differentiator topic in interviews.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [OpenTelemetry](40.4.4.01-opentelemetry.md) | Vendor-neutral traces + metrics + logs, OTLP, W3C Trace Context, head/tail sampling, baggage, collector pipeline | 30 min |

*Slots reserved: `40.4.4.02` continuous profiling, `40.4.4.03` eBPF observability (upcoming chapters — no links yet).*

---

## Cross-References

- [The 3 Pillars](../01-pillars/INDEX.md) — the signals OTel unifies
- [Tracing](../01-pillars/INDEX.md) — trace semantics in depth

---

## Navigation

[← SRE Targets](../03-sre-targets/INDEX.md) · [↑ Observability Home](../INDEX.md) · [Next: Interview Prep →](../05-interview-prep/INDEX.md)
