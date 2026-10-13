# Advanced Telemetry

> **Study time:** ≈ 28 min of reading (4 files, ~7 min average).
> **4 files.** OpenTelemetry standardizes instrumentation and export; continuous profiles add code-level evidence, with OpenTelemetry Profiles still in public Alpha; eBPF adds selected kernel-level visibility.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Telemetry-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Instrumenting once per vendor does not survive the second vendor swap. OpenTelemetry standardizes SDKs, the OTLP wire protocol, and context propagation (W3C Trace Context), with a collector pipeline that batches, filters, and samples before export. Continuous profiling adds the "which code consumed it" answer that metrics and traces cannot give; eBPF observes supported hooks and workloads; encryption, symbols, permissions and lost events bound its coverage. Together they are the senior-differentiator telemetry stack.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [OpenTelemetry](40.4.4.01-opentelemetry.md) | Vendor-neutral traces + metrics + logs, OTLP, W3C Trace Context, head/tail sampling, baggage, collector pipeline | Important | Important | 9 min |
| 02 | [Continuous Profiling](40.4.4.02-continuous-profiling.md) | Always-on CPU/heap/allocation sampling, Pyroscope/Parca, flamegraph diffing across releases, overhead budgets, span-profile trace integration | Important | Important | 8 min |
| 03 | [eBPF Observability](40.4.4.03-ebpf-observability.md) | Kernel programs + verifier + maps, Hubble/Cilium service graph, Pixie auto-telemetry, Falco/Tetragon security overlap, overhead and risks | Important | Specialized | 9 min |

---

## Cross-References

- [The 3 Pillars](../01-pillars/INDEX.md) — the signals OTel unifies
- [Distributed Tracing](../01-pillars/40.4.1.03-tracing.md) — trace semantics in depth

---

## Navigation

[← SRE Targets](../03-sre-targets/INDEX.md) · [↑ Observability Home](../INDEX.md) · [Next: Interview Prep →](../05-interview-prep/INDEX.md)

---

## Docita Anchor

Read-only source pointers in [Docita](https://github.com/CVamsi27/docita); these do not establish production collection coverage or privacy guarantees.

_No direct docita implementation yet_ for OpenTelemetry/eBPF — tracing is Sentry-based. What docita does have is the surrounding discipline:

| Topic | Docita evidence |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Correlation IDs | `request-id.interceptor.ts` + `request-logging.interceptor.ts` provide request correlation in the implemented paths; verify error and async boundaries |
| Log scrubbing gates | `phi-redactor.ts`; CI checks `check-sensitive-logging.mjs`, `check-sentry-scrubbing.mjs`, `check-sentry-scrubber-parity.mjs` |
| Metrics aggregation & cardinality care | `metrics-aggregation.service.ts`, business metrics separated from API-request metrics |
| RUM telemetry | `web-vitals-metrics.service.ts` + RUM controller |
| Continuous profiling | Sentry profiling integration exists (`SENTRY_PROFILING`), kept off by default on Alpine |

## Learning Passes

1. Place API, SDK, Collector and backend in one pipeline; follow identity and sampling decisions.
2. Read a profile as statistical resource evidence and compare equivalent release workloads.
3. Trace a kernel event through hook, buffer and agent; state what it cannot reveal.
4. Complete revision before the observability interview bank.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
