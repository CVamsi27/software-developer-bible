<!-- section: Build Tools | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Build%20Tools-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Build Tools — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Webpack

Source: [Webpack](40.5.1.01-webpack.md)

**Q:** Why do ESM export analysis and `sideEffects` metadata affect different pruning decisions?

**A:** Static ESM exports let Webpack identify unused exports inside a module. `sideEffects` describes whether evaluating a module can be skipped entirely. Incorrect metadata can remove required CSS imports or registration code. See [Webpack tree shaking](40.5.1.01-webpack.md#follow-one-import-through-the-build).

**Q:** Why can an HMR update still cause a full page reload?

**A:** The runtime can replace changed code only if the changed module or a dependency boundary accepts the update and its side effects can be handled. An unaccepted update cannot safely propagate, so the development client may reload the page. See [Webpack HMR](40.5.1.01-webpack.md#development-updates-and-production-boundaries) and the [official HMR guide](https://webpack.js.org/guides/hot-module-replacement/).

**Q:** Why retain prior content-hashed chunks after deploying a new build?

**A:** A tab can keep the old entry code in memory and later request a chunk whose old content-hashed URL it already knows. If deployment deletes that asset immediately, the request fails even though the new build works for fresh visits. See [Webpack's lazy-chunk deployment boundary](40.5.1.01-webpack.md#example-load-a-feature-on-demand) and the [official caching guide](https://webpack.js.org/guides/caching/).

**Q:** When should an imported image use `asset/resource` rather than `asset/inline`?

**A:** `asset/resource` emits a separately cacheable file and exports its URL; `asset/inline` puts a data URI into the referring output. The automatic `asset` type chooses between these forms by a size threshold. See [Webpack Asset Modules](40.5.1.01-webpack.md#follow-one-import-through-the-build) and the [official Asset Modules guide](https://webpack.js.org/guides/asset-modules/).

## Vite

Source: [Vite](40.5.1.02-vite.md)

**Q:** What changed in Vite 8 without removing the dev/build split?

**A:** Rolldown replaced Rollup/dependency optimization and Oxc replaced JavaScript transforms/minification. Development still defers source work while production optimizes deployable output.

**Q:** Why is a development proxy insufficient after deploying dist?

**A:** It belongs to the dev server. Static production hosting needs its own API routing/reverse proxy, CORS policy, and SPA fallback.

## Turbopack

Source: [Turbopack](40.5.1.03-turbopack.md)

**Q:** Why is Turbopack not interchangeable with Turborepo?

**A:** Turbopack bundles module graphs inside Next.js. Turborepo schedules workspace tasks and caches their declared outputs, which may be produced by Turbopack or another tool.

## Rspack

Source: [Rspack](40.5.1.04-rspack.md)

**Q:** Why test every required Webpack integration during a Rspack migration?

**A:** Compatibility is broad but not universal. Custom plugins, loader behavior, and output semantics must be demonstrated on the application rather than inferred from similar configuration.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — return to prerequisites and compare the tool’s output boundary

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
