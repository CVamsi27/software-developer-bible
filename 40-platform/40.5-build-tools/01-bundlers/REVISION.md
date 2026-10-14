<!-- section: Build Tools | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Build%20Tools-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
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

**Q:** In Webpack 5.109 and later, does native CSS/HTML handling in `auto` mode mean existing loaders and plugins can always be removed?

**A:** No. A matching rule can keep the existing loader path, and the built-in CSS and HTML features remain experimental with gaps in loader and plugin behavior. Check the pinned release and migrate one rule or entry at a time. See [Webpack's native CSS and HTML boundary](40.5.1.01-webpack.md#follow-one-import-through-the-build), the [native CSS guide](https://webpack.js.org/guides/native-css/) and the [native HTML guide](https://webpack.js.org/guides/native-html/).

## Vite

Source: [Vite](40.5.1.02-vite.md)

**Q:** What changed in Vite 8 without removing the dev/build split?

**A:** Rolldown now handles dependency optimization and production bundling; Oxc handles JavaScript/TypeScript transforms and JavaScript minification, while Lightning CSS handles CSS minification. The default development flow still serves application modules on demand. Vite 8.1's bundled-development mode is experimental and opt-in.

**Q:** Why does Vite pre-bundle packages when it still serves application source modules separately?

**A:** Browsers cannot resolve bare package names and some dependencies ship as CommonJS or UMD, so Vite must rewrite them into browser-loadable ESM. Pre-bundling also reduces the request count for packages split into many ESM files. It optimizes dependencies, not the application source graph. See [Vite's dependency path](40.5.1.02-vite.md#from-the-html-entry-to-an-edit) and the [official guide](https://vite.dev/guide/dep-pre-bundling).

**Q:** Why is a development proxy insufficient after deploying dist?

**A:** It belongs to the dev server and is not copied into `dist`. Production needs its own API routing; configure CORS only if the deployed browser request is cross-origin, and configure the static host's SPA fallback for client routes. See [Vite's deployment boundaries](40.5.1.02-vite.md#configuration-and-deployment-boundaries).

**Q:** Why does a successful Vite build not prove that TypeScript types are correct?

**A:** Vite's Oxc transform removes TypeScript syntax per file so the browser can execute the result; it does not analyze the whole TypeScript program. Run `tsc --noEmit` as a separate CI/build gate. See [Vite's transform boundary](40.5.1.02-vite.md#configuration-and-deployment-boundaries) and the [official feature guide](https://vite.dev/guide/features).

**Q:** Why is `vite build --mode staging` still normally an optimized production build?

**A:** Vite mode selects `.env.[mode]` files, while `NODE_ENV` controls a separate set of production/development constants. `--mode staging` loads `.env.staging` without changing the build command's production behavior by itself. Any `VITE_` value used in browser code is public build output. See [Vite environment and deployment rules](40.5.1.02-vite.md#configuration-and-deployment-boundaries) and the [official modes guide](https://vite.dev/guide/env-and-mode).

## Turbopack

Source: [Turbopack](40.5.1.03-turbopack.md)

**Q:** Why is Turbopack not interchangeable with Turborepo?

**A:** Turbopack bundles module graphs inside Next.js. Turborepo schedules workspace tasks and caches their declared outputs, which may be produced by Turbopack or another tool.

**Q:** How should a team compare Turbopack build-cache results across local development and CI?

**A:** Next.js 16.1 made development filesystem caching stable and enabled it by default. The 16.3 release notes say build filesystem caching works and is enabled by default, while the current API reference still calls the build option opt-in. Verify the version-matched behavior before changing CI configuration; when caching is enabled, CI must preserve `.next/cache` for warm builds. Compare cold and warm runs separately and key the cache to the lockfile, Next.js version and build configuration. See [Turbopack's cache lifetimes](40.5.1.03-turbopack.md#the-cache-has-two-lifetimes), the [official API reference](https://nextjs.org/docs/app/api-reference/turbopack), and the [Next.js 16.3 release](https://nextjs.org/blog/next-16-3).

**Q:** What must be verified when a Next.js app depends on a Webpack loader or plugin?

**A:** Turbopack supports only part of the Webpack loader API, requires loaders to emit JavaScript, and does not run Webpack plugins. Exercise each needed rule in both `next dev` and `next build`; keep `--webpack` for an unsupported required integration until an alternative is tested. See [the compatibility boundary](40.5.1.03-turbopack.md#keep-migration-compatibility-explicit) and the [official reference](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack).

**Q:** What can a Turbopack trace establish, and what does it not establish?

**A:** A trace shows where a particular development run spent time and how module work is related. It helps locate a slow route or update, but it does not prove a migration improves the user-facing workload; collect comparable measurements and inspect paths and workload details before sharing it. See [the measurement path](40.5.1.03-turbopack.md#measure-the-actual-task) and the [official tracing guide](https://nextjs.org/docs/app/guides/local-development).

## Rspack

Source: [Rspack](40.5.1.04-rspack.md)

**Q:** Why test every required Webpack integration during a Rspack migration?

**A:** Compatibility is broad but not universal. Custom plugins, loader behavior, and output semantics must be demonstrated on the application rather than inferred from similar configuration.

**Q:** In Rspack 2, how do `cache` and `incremental` differ?

**A:** `cache` reuses fine-grained compilation results from memory or persistent storage. `incremental` recovers work between development rebuilds and updates affected passes. They are independent: disabling `cache` does not disable `incremental`, so a fully cold comparison must disable both. See [Rspack's cache boundaries](40.5.1.04-rspack.md#keep-cache-mechanisms-separate) and the [official cache reference](https://rspack.rs/config/cache).

**Q:** Why does a successful Webpack-plugin load not complete a Rspack migration test?

**A:** Rspack supports many, but not all, Webpack plugins and configuration behaviors. A plugin may rely on internal Webpack APIs, while Module Federation can compile but still fail at runtime because a remote is unavailable or shared package versions do not match. Check the versioned compatibility information and exercise real production routes. See [the integration boundary](40.5.1.04-rspack.md#migrate-the-integration-not-just-the-config) and the [plugin documentation](https://rspack.rs/guide/features/plugin).

**Q:** Which dependencies should invalidate a Rspack persistent cache?

**A:** Include configuration and other external files whose contents can affect resolution or transforms. The CLI adds its config file automatically; direct API users and setups that load additional build-configuration files must list those paths in `cache.buildDependencies`. See [the cache migration path](40.5.1.04-rspack.md#keep-cache-mechanisms-separate) and [Rspack's cache reference](https://rspack.rs/config/cache).

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — return to prerequisites and compare the tool’s output boundary

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
