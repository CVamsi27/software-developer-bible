# Advanced Telemetry

> **3 files.** Beyond the basics: OpenTelemetry as the vendor-neutral instrumentation layer, continuous profiling as the fourth signal, and eBPF for zero-instrumentation kernel-level visibility.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Telemetry-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Instrumenting once per vendor does not survive the second vendor swap. OpenTelemetry standardizes SDKs, the OTLP wire protocol, and context propagation (W3C Trace Context), with a collector pipeline that batches, filters, and samples before export. Continuous profiling adds the "which code consumed it" answer that metrics and traces cannot give; eBPF observes every workload from the kernel boundary with no app changes at all. Together they are the senior-differentiator telemetry stack.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [OpenTelemetry](40.4.4.01-opentelemetry.md) | Vendor-neutral traces + metrics + logs, OTLP, W3C Trace Context, head/tail sampling, baggage, collector pipeline | 30 min |
| 02 | [Continuous Profiling](40.4.4.02-continuous-profiling.md) | Always-on CPU/heap/allocation sampling, Pyroscope/Parca, flamegraph diffing across releases, overhead budgets, span-profile trace integration | 30 min |
| 03 | [eBPF Observability](40.4.4.03-ebpf-observability.md) | Kernel programs + verifier + maps, Hubble/Cilium service graph, Pixie auto-telemetry, Falco/Tetragon security overlap, overhead and risks | 30 min |

---

## Cross-References

- [The 3 Pillars](../01-pillars/INDEX.md) — the signals OTel unifies
- [Tracing](../01-pillars/INDEX.md) — trace semantics in depth

---

## Navigation

[← SRE Targets](../03-sre-targets/INDEX.md) · [↑ Observability Home](../INDEX.md) · [Next: Interview Prep →](../05-interview-prep/INDEX.md)
