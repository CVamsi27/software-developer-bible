<!-- section: Performance Monitoring | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Performance%20Monitoring-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Performance Monitoring — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Performance APIs

Source: [Performance APIs](50.3.2.01-performance-apis.md)

**Q:** Why use marks and measures around a specific operation?

**A:** They define the operation's own timing boundary rather than inferring it from whole-page load events. Name and clear entries deliberately to avoid unbounded accumulation.

## Profiling Tools

Source: [Profiling Tools](50.3.2.02-profiling-tools.md)

**Q:** How do profiles and network waterfalls identify different costs?

**A:** Profiles reveal CPU/render work and task scheduling; waterfalls show requests, dependencies, and transfer timing. Slow experience may involve both, so connect observations.

## Lighthouse CI

Source: [Lighthouse CI](50.3.2.03-lighthouse-ci.md)

**Q:** Why keep lab conditions stable in a performance gate?

**A:** Device emulation, throttling, cache, build, and test route change the result. Comparable repetitions and tolerance distinguish regressions from noise.

## Real User Monitoring (RUM)

Source: [Real User Monitoring (RUM)](50.3.2.04-real-user-monitoring.md)

**Q:** What should a RUM report segment before comparing releases?

**A:** Device/network, route, region, navigation type, and relevant user populations under a privacy policy. A traffic-mix change can move the global percentile without a code regression.

## HTTP/2 & HTTP/3 Performance Effects

Source: [HTTP/2 & HTTP/3 Performance Effects](50.3.2.05-http2-http3-performance-effects.md)

**Q:** What head-of-line problem does QUIC reduce without eliminating every shared constraint?

**A:** A lost stream's bytes need not block delivery of unrelated stream bytes. Connection-wide congestion control, bandwidth, flow control, and compression dependencies can still affect multiple streams.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
