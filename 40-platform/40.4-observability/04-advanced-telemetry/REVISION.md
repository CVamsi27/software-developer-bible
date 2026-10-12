<!-- section: Observability | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Observability-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Observability — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## OpenTelemetry (OTel)

Source: [OpenTelemetry (OTel)](40.4.4.01-opentelemetry.md)

**Q:** What is OpenTelemetry separate from?

**A:** It standardizes instrumentation, context, and telemetry collection/export. It is not itself the storage/query backend that decides retention, dashboards, or alert policy.

**Q:** What maturity boundary should you check before adopting OpenTelemetry Profiles?

**A:** The Profiles specification is in public Alpha and its protocol remains in development; SDK, Collector and backend support varies. Verify the exact components you plan to deploy; do not infer production support from the general OpenTelemetry name. See the [component status](https://opentelemetry.io/docs/specs/status/) and [Profiles specification](https://opentelemetry.io/docs/specs/otel/profiles/).

**Q:** Why batch and bound telemetry queues?

**A:** Exporters must not create unlimited memory growth or block critical application work when the backend slows down. Queue limits, drops, and retry policy need observability too.

## Continuous Profiling

Source: [Continuous Profiling](40.4.4.02-continuous-profiling.md)

**Q:** How do continuous profiles complement traces?

**A:** Profiles show sampled CPU/allocation/lock costs across time and workloads; traces show a selected request's path. Linking both to versions narrows a regression's cause.

**Q:** Why can a sample-heavy function still be the wrong first optimization?

**A:** Frequency identifies aggregate cost, not necessarily user-critical latency or an avoidable bottleneck. Compare the profile with request paths and workload goals.

## eBPF Observability

Source: [eBPF Observability](40.4.4.03-ebpf-observability.md)

**Q:** Why does eBPF still need a permissions and overhead review?

**A:** Kernel verification constrains program behavior but does not remove access, data-exposure, kernel-version, or resource-cost considerations. Attach only the probes required.

## Coverage and Sampling Decisions

Sources: [OpenTelemetry](40.4.4.01-opentelemetry.md), [Profiling](40.4.4.02-continuous-profiling.md), [eBPF](40.4.4.03-ebpf-observability.md).

**Q:** Can tail sampling recover errors discarded by a 1% head sampler?

**A:** No. It decides among received traces. Keeping all qualifying errors requires an input, buffering and routing policy that supplies those errors and survives its relevant failure cases.

**Q:** Why can two randomly balanced tail-sampling collectors lose trace context?

**A:** Spans from one trace can reach different decision makers. Trace-aware routing, late-span behavior and bounded decision buffers need explicit design.

**Q:** Does high allocation volume prove that objects are retained?

**A:** No. Allocation profiles show churn; live-heap evidence and retention paths are needed to investigate a leak. Compare equivalent workloads and runtime versions.

**Q:** Why does an eBPF HTTP graph need more qualification than a connection graph?

**A:** HTTP interpretation needs compatible parsing, configuration and access to readable protocol data. Encryption, unavailable hooks and lost events can limit coverage; selected flow records are not complete application traces.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
