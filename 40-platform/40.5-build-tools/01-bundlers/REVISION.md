<!-- section: Build Tools | category: Reference | tags: revision, practice| general-importance: specialized| general-importance: specialized | role-priority: important | general-importance: specialized -->
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

**Q:** Why do ESM and sideEffects metadata affect different pruning decisions?

**A:** Static exports enable unused-export analysis; sideEffects describes whether evaluating an otherwise unused module must be preserved. Incorrect metadata can remove required CSS or registration.

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

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
