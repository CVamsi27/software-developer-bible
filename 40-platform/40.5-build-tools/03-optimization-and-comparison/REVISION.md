<!-- section: Build Tools | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Build%20Tools-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Build Tools — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Build Optimization

Source: [Build Optimization](40.5.3.01-build-optimization.md)

**Q:** Why separate cold builds from incremental edit timings?

**A:** They reuse different work. Cache state, affected dependency scope, and plugin transforms must be controlled before a speed comparison is meaningful.

**Q:** Why can aggressive chunk splitting slow a route?

**A:** It may add dependency waterfalls and loading overhead while improving cache reuse. Measure the route's network and execution path rather than minimizing every individual chunk.

## Asset Pipelines — CSS, Images & Fonts

Source: [Asset Pipelines — CSS, Images & Fonts](40.5.3.02-asset-pipelines-css-images-fonts.md)

**Q:** What makes a content-hashed asset safe for immutable caching?

**A:** Its content must never change at the same URL. Entry HTML/manifests need a refresh policy so clients can discover new hashes, and old assets must remain available during rollout.

**Q:** Does a hidden source map make the map private?

**A:** No. It removes the bundle's map-discovery comment. The emitted map must still be excluded from public hosting when privacy is required.

## Build Tool Comparison

Source: [Build Tool Comparison](40.5.3.03-build-tool-comparison.md)

**Q:** Why is the fastest benchmark not enough to select a tool?

**A:** Framework support, extension compatibility, output behavior, memory, and migration cost determine whether the measured gain is useful and safe.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
