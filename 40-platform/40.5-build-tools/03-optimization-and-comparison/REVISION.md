<!-- section: Build Tools | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Build%20Tools-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Build Tools — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Build Optimization

Source: [Build Optimization](40.5.3.01-build-optimization.md)

**Q:** Why separate cold builds from incremental edit timings?

**A:** They reuse different work. Cache state, affected dependency scope, and plugin transforms must be controlled before a speed comparison is meaningful.

**Q:** Why can aggressive chunk splitting slow a route?

**A:** It may add dependency waterfalls and loading overhead while improving cache reuse. Measure the route's network and execution path rather than minimizing every individual chunk.

**Q:** Why is one JavaScript file's gzip size not a route-level performance budget?

**A:** The route may request several JavaScript chunks plus CSS, fonts and images. A gzip value describes one encoded file, not the full dependency waterfall, actual response encoding, parse/execute work or rendered result. Resolve the entry's required assets from the manifest and fail when that evidence is missing. See [the route budget boundary](40.5.3.01-build-optimization.md#measure-what-the-route-actually-ships) and [Vite's production output guide](https://vite.dev/guide/build).

**Q:** How do `usedExports` analysis and `sideEffects` metadata prevent different work?

**A:** Export-use analysis can remove unused exports; `sideEffects` tells the bundler whether evaluating an entire module can be skipped. A false side-effect declaration can drop an imported stylesheet or registration module even when a component export is retained. See [the module-graph boundary](40.5.3.01-build-optimization.md#trace-from-the-module-graph-to-the-route) and [Webpack tree shaking](https://webpack.js.org/guides/tree-shaking/).

**Q:** Why must build-time size and field LCP/INP results be measured separately?

**A:** Build time measures compiler work, while Largest Contentful Paint (LCP) records visible main-content rendering and Interaction to Next Paint (INP) measures interaction responsiveness. A static lab load cannot establish INP because the page needs real interactions. See [the runtime measurement boundary](40.5.3.01-build-optimization.md#match-the-technique-to-the-measured-cost) and the [Web Vitals measurement guide](https://web.dev/articles/vitals-measurement-getting-started).

## Asset Pipelines — CSS, Images & Fonts

Source: [Asset Pipelines — CSS, Images & Fonts](40.5.3.02-asset-pipelines-css-images-fonts.md)

**Q:** What makes a content-hashed asset safe for immutable caching?

**A:** Its content must never change at the same URL. Entry HTML/manifests need a refresh policy so clients can discover new hashes, and old assets must remain available during rollout.

**Q:** Does a hidden source map make the map private?

**A:** No. It removes the bundle's map-discovery comment. The emitted map must still be excluded from public hosting when privacy is required.

**Q:** In Vite, does choosing Lightning CSS as the production minifier also opt into it as the CSS transformer?

**A:** No. Production CSS minification and the CSS transformer are separate options. Current Vite uses PostCSS as its default transformer and Lightning CSS for production minification by default; selecting Lightning CSS for the full transform path is experimental and can change plugin compatibility. See the [current Vite CSS options](https://vite.dev/config/shared-options) and [build options](https://vite.dev/config/build-options).

**Q:** Why can a correctly hashed image import still deliver the wrong amount of image data?

**A:** Hashing identifies emitted bytes; it does not create responsive variants or tell the browser their rendered widths. Generate candidates, connect them with truthful `srcset` and `sizes`, reserve layout dimensions, then inspect which candidate production selects. See [responsive asset handling](40.5.3.02-asset-pipelines-css-images-fonts.md#let-the-browser-choose-an-image) and [responsive image guidance](https://web.dev/articles/serve-responsive-images).

**Q:** Why can a font swap change layout even when fallback text appears immediately?

**A:** The fallback and web font can have different glyph widths and line metrics. `font-display: swap` controls when text appears, not metric equivalence; use an appropriate fallback and metric overrides, and measure layout shifts with the page's real text. See [font delivery and layout](40.5.3.02-asset-pipelines-css-images-fonts.md#deliver-fonts-without-hiding-text-or-shifting-layout), [font best practices](https://web.dev/articles/font-best-practices), and the [CSS Fonts descriptors](https://www.w3.org/TR/css-fonts-4/).

**Q:** Is `limitInputPixels` by itself a sufficient defense when transforming arbitrary uploads with sharp?

**A:** No. The documented limit uses dimensions from input metadata and assumes those dimensions are trustworthy. Also bound request bytes, accepted formats, concurrent conversions and total output, then isolate or time-limit processing to match the upload threat model. See [bounded image processing](40.5.3.02-asset-pipelines-css-images-fonts.md#generate-variants-within-explicit-limits) and [sharp constructor limits](https://sharp.pixelplumbing.com/api-constructor/).

## Build Tool Comparison

Source: [Build Tool Comparison](40.5.3.03-build-tool-comparison.md)

**Q:** Why is the fastest benchmark not enough to select a tool?

**A:** Framework support, extension compatibility, output behavior, memory, and migration cost determine whether the measured gain is useful and safe.

**Q:** Why can't a `vite dev` startup time be compared with a Webpack production build time?

**A:** They perform different work. Development startup includes server readiness and requested-route compilation; a production build resolves and emits the application output. Compare matching workloads and report cache state for both rather than ranking tools from unlike commands. See [equivalent workload measurement](40.5.3.03-build-tool-comparison.md#measure-equivalent-work) and [Vite's toolchain explanation](https://vite.dev/guide/why).

**Q:** What evidence distinguishes slow bundling from repeated package-task work in CI?

**A:** Time a single representative package build separately from the orchestrated workspace run, then inspect task cache hits and which input changes invalidate each output. A task orchestrator can reuse package work without changing module resolution or the bundler. See [the tool-layer map](40.5.3.03-build-tool-comparison.md#name-the-layer-before-comparing-tools) and [Turborepo caching](https://turborepo.dev/docs/crafting-your-repository/caching).

**Q:** What must pass before calling a Webpack-to-Rspack migration compatible?

**A:** Verify every required loader, plugin hook, alias, asset rule, target, and runtime integration on a representative slice. Then run the same type checks and tests, inspect production output and maps, and compare the same cold or warm workload. See [the migration proof](40.5.3.03-build-tool-comparison.md#prove-the-migration-on-a-representative-slice) and [Rspack's compatibility guidance](https://rspack.rs/guide/migration/webpack).

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — return to prerequisites and compare the tool’s output boundary

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
