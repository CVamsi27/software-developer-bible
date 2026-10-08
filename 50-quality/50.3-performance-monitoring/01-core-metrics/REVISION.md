<!-- section: Performance Monitoring | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Performance%20Monitoring-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Performance Monitoring — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Core Web Vitals

Source: [Core Web Vitals](50.3.1.01-core-web-vitals.md)

**Q:** Why assess the 75th percentile separately for the relevant device population?

**A:** It exposes the experience a substantial user segment receives rather than hiding it in a global mean. Good field thresholds are LCP at most 2.5s, INP at most 200ms, and CLS at most 0.1.

**Q:** Why does a Lighthouse run not directly measure field INP?

**A:** INP depends on real interactions across the page lifecycle. Lab diagnostics such as blocking time and scripted interactions help explain risk but are not the same population/metric.

**Q:** Why is INP not simply the maximum event callback duration?

**A:** It includes input delay, processing, and presentation delay for interactions, with grouping and a high-interaction outlier allowance. Handler time alone misses important latency.

**Q:** What can a fast HTML response leave slow about LCP?

**A:** Discovery, download, priority, layout, and rendering of the largest eligible content can still be delayed. Trace the actual LCP resource path instead of optimizing TTFB alone.

**Q:** Why reserve image space before loading it?

**A:** Known dimensions or an appropriate aspect ratio prevent later content movement. The rendered layout and responsive behavior must match the reservation.

**Q:** Eligible shifts score 0.1 at 0ms, 0.2 at 500ms and 0.05 at 3000ms. Why is CLS 0.3 rather than 0.35?

**A:** The first two shifts share a session window and sum to 0.3. The later shift follows a gap of more than one second and starts another window. CLS uses the largest window sum, rather than the lifetime total. A raw observer that adds every eligible entry reports a different measure.

## Field aggregation and changed conditions

Source: [Core Web Vitals](50.3.1.01-core-web-vitals.md)

**Q:** Eight sorted mobile LCP values end with 3,500, 3,900, 4,200 and 6,000 ms. Which value does nearest-rank p75 select?

**A:** The sixth observation, 3,900 ms. It needs improvement. The estimator and population must be explicit; averaging several subgroup p75 values does not reconstruct the combined distribution.

**Q:** Why is INP of 320 ms neither good nor poor?

**A:** Good ends at 200 ms and poor starts above 500 ms. The middle interval needs improvement. A universal multiplier of 1.6 would misclassify this metric.

**Q:** What changes when a visit has no qualifying interaction?

**A:** It may have no INP observation. Keep the missing value and collection coverage visible; substituting zero invents evidence of fast responsiveness.

**Q:** Why can registering web-vitals callbacks in a repeated React effect distort reporting?

**A:** Repeated registration can add collectors/callbacks; the normal library functions do not return an effect cleanup handle. Register once at document bootstrap and aggregate updates under the metric ID.

**Q:** Why must an ingestion service distinguish value from delta?

**A:** Value is the current metric; delta is the change since its previous report. Upsert values or accumulate deltas deliberately. Counting each callback as a new visit changes the sample distribution.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — separate per-visit metric boundaries from a field distribution

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
