<!-- section: Performance Monitoring | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Performance%20Monitoring-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

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

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
