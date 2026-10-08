<!-- section: Performance Monitoring | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Performance%20Monitoring-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Performance Monitoring — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Performance APIs

Source: [Performance APIs](50.3.2.01-performance-apis.md)

**Q:** Why use marks and measures around a specific operation?

**A:** They define the operation's own timing boundary rather than inferring it from whole-page load events. Name and clear entries deliberately to avoid unbounded accumulation.

**Q:** Trace what happens when a measured operation rejects and its reporting callback also throws.

**A:** The helper measures in finally, catches the reporting failure and clears its owned entries. The caller still receives the operation's original rejection. The interval ends at settlement, not at a later paint.

**Q:** What changes when two calls use the same operation label concurrently?

**A:** The sequence suffix gives each its own start/measure names. Each clears only its own entries; shared names could otherwise measure or clear the other call's timing.

## Profiling Tools

Source: [Profiling Tools](50.3.2.02-profiling-tools.md)

**Q:** How do profiles and network waterfalls identify different costs?

**A:** Profiles reveal CPU/render work and task scheduling; waterfalls show requests, dependencies, and transfer timing. Slow experience may involve both, so connect observations.

**Q:** A handler has 120 ms total time and a child has 80 ms total time. Why is their combined cost not 200 ms?

**A:** The parent's total includes its child. Inspect self time and the call tree to attribute the remaining 40 ms; do not sum nested totals or overlapping work.

**Q:** What does the layout experiment change, and what remains outside its stopwatch?

**A:** Both paths change row widths and read geometry. Interleaving can require repeated layout; batching writes allows subsequent reads to share current geometry. The synchronous interval ends before a future paint and does not establish full interaction latency or a fixed speedup.

**Q:** A heap grows after several mount/unmount cycles. What evidence distinguishes a leak from normal allocation?

**A:** Compare the same idle state and inspect retained objects and their reference paths. Remove the suspected owner, repeat the cycle and check accumulation. Garbage collection, console references and valid caches can explain growth without a leak.

## Lighthouse CI

Source: [Lighthouse CI](50.3.2.03-lighthouse-ci.md)

**Q:** Why keep lab conditions stable in a performance gate?

**A:** Device emulation, throttling, cache, build, and test route change the result. Comparable repetitions and tolerance distinguish regressions from noise.

**Q:** Why does the static Lighthouse fixture retain reports locally instead of requiring an upload server?

**A:** Collection, assertions and retention are separate. Filesystem export supplies local reports; the CI artifact system must retain them. An error-level assertion's nonzero status needs a required pipeline check to block merging.

**Q:** What changes if a category score passes but an LCP error threshold fails?

**A:** The assertion command fails. A category score is not proof that each raw timing passed; warning-level assertions alone do not cause a nonzero status.

**Q:** Why does a zero LCP budget test a different claim from a normal budget?

**A:** It deliberately makes a positive collected LCP violate the assertion. That proves the failure path is enforced, not that the product has a production regression.

## Real User Monitoring (RUM)

Source: [Real User Monitoring (RUM)](50.3.2.04-real-user-monitoring.md)

**Q:** What should a RUM report segment before comparing releases?

**A:** Device/network, route, region, navigation type, and relevant user populations under a privacy policy. A traffic-mix change can move the global percentile without a code regression.

**Q:** Trace two reports with the same metric ID, values 1,800 and 2,200 ms, and sequences 1 then 2.

**A:** The receiver creates one identity, then replaces its snapshot with sequence 2. A retry or later arrival of sequence 1 does not become another visit or overwrite the newer value. The fixture is process-local and not durable.

**Q:** Why does always retaining slow visits but sampling fast visits bias an ordinary p75?

**A:** Slow visits have a higher inclusion probability. For 90 fast and 10 slow visits, retaining all slow and about 10 percent fast yields about 9 fast plus 10 slow observations. Use separate diagnostics or a valid weighted analysis rather than treating that sample as uniform.

**Q:** What changes when sendBeacon returns true but the receiver never stores the report?

**A:** The browser accepted queueing, not a durable receipt. Collection coverage can still be lost. The chosen transport, retry and receiver acknowledgment contract must remain explicit.

**Q:** Why can your RUM disagree with CrUX without either source having an arithmetic error?

**A:** They can observe different users, eligibility, time windows and lifecycle boundaries. Your endpoint does not supply CrUX. Compare scope before interpreting their percentiles as identical populations.

## HTTP/2 & HTTP/3 Performance Effects

Source: [HTTP/2 & HTTP/3 Performance Effects](50.3.2.05-http2-http3-performance-effects.md)

**Q:** What head-of-line problem does QUIC reduce without eliminating every shared constraint?

**A:** A lost stream's bytes need not block delivery of unrelated stream bytes. Connection-wide congestion control, bandwidth, flow control, and compression dependencies can still affect multiple streams.

**Q:** Why can stream B still progress when stream A has missing bytes in QUIC?

**A:** Delivery ordering is per stream. If B has its required bytes and no compression/application dependency blocks it, A's gap need not block B. Shared congestion can still reduce both streams' sending rate, and one lost packet may create gaps in several streams.

**Q:** Does a connection ID guarantee an uninterrupted Wi-Fi-to-cellular transition?

**A:** No. It helps identify the connection after an address change, but migration depends on peer behavior, routing and successful path validation. Application retry and duplicate-effect handling still need contracts.

**Q:** What changes when a server rejects 0-RTT early data?

**A:** The client must follow the negotiated recovery behavior; early sending did not establish acceptance. Replay-safe application semantics are required where early data is accepted. Zero refers to setup wait before sending, not zero response latency.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — choose the measurement boundary before comparing tool outputs

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
