<!-- section: Monorepo | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Monorepo-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Monorepo — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Monorepo Overview

Source: [Monorepo Overview](40.8.01-monorepo-overview.md)

**Q:** What does one repository make atomic, and what does it not?

**A:** A commit can change related packages together. Runtime deployment, database changes, and publication still require compatibility and release coordination.

**Q:** Why can a workspace package import work locally but fail for a registry consumer?

**A:** The workspace link may expose files that were never built or exported in the package manifest. Build the package, inspect its tarball and workspace-range rewrites, then install it in a clean consumer. See pnpm's [workspace protocol](https://pnpm.io/workspaces) and Node's [package entry-point rules](https://nodejs.org/api/packages.html).

## Turborepo

Source: [Turborepo](40.8.02-turborepo.md)

**Q:** Why can an undeclared environment input produce a wrong cache hit?

**A:** The hash may treat different build behavior as identical and restore an artifact from another configuration. Declare output-affecting inputs and avoid caching side-effecting tasks. See Turborepo’s [cache inputs and outputs](https://turborepo.dev/docs/crafting-your-repository/caching) and [task configuration](https://turborepo.dev/docs/reference/configuration).

## Nx

Source: [Nx](40.8.03-nx.md)

**Q:** Why are dependency boundaries needed even with an accurate project graph?

**A:** A graph describes coupling; it does not prevent unwanted coupling. Tags and rules establish which dependencies are allowed, and lint or conformance must run as a required check. See Nx’s [module-boundary enforcement](https://nx.dev/docs/features/enforce-module-boundaries).

**Q:** Why can two Nx 24 workspaces select different tasks for the same change?

**A:** New workspaces default to task-based affected selection, while a migration preserves project-based selection with `affected.legacy: true`. `NX_LEGACY_AFFECTED` can override the mode. In task mode, inputs and consumed outputs propagate changes; a `dependsOn` edge alone only orders work. Check the [affected contract](https://nx.dev/docs/features/ci-features/affected) and the resolved CI mode.

## Monorepo Tools Deep-Dive (Lerna, pnpm, Yarn, Rush, Bazel)

Source: [Monorepo Tools Deep-Dive (Lerna, pnpm, Yarn, Rush, Bazel)](40.8.04-monorepo-tools.md)

**Q:** What are the three toolchain layers you should keep separate?

**A:** Package management resolves/links dependencies, task orchestration schedules/caches work, and compilers/bundlers produce artifacts. Some tools overlap, but each contract still needs an owner. The [Nx mental model](https://nx.dev/docs/concepts/mental-model) shows why project and task graphs answer different questions.

**Q:** Can engineer count determine whether a repository needs Bazel?

**A:** No. Compare declared toolchains, generated inputs and reproducibility needs with supported rules and maintenance cost. A small repository can need those controls; a large one can still have a simple script graph. Bazel’s [build model](https://bazel.build/) makes targets and actions explicit, so pilot the rules required by your languages.

**Q:** What should a monorepo tooling pilot prove before trusting remote cache hits?

**A:** Prove uncached dependency order and outputs first, then test invalidation for source, configuration, environment and toolchain changes. Protect cache writers and check editor/install compatibility as separate requirements.

## Versioning & Publishing Strategies

Source: [Versioning & Publishing Strategies](40.8.05-versioning-publishing-strategies.md)

**Q:** Why does a package release need dependency-range changes as well as a new version?

**A:** Consumers need compatible dependency and peer ranges, and the packed manifest must contain registry-resolvable references. Bumping the package alone may leave workspace-only references or incompatible dependents. Review the [Changesets versioning flow](https://changesets.dev/guide/versioning-and-publishing) and the [SemVer contract](https://semver.org/).

## Boundaries to Recheck

Source: [Monorepo Overview](40.8.01-monorepo-overview.md)

**Q:** Can CODEOWNERS keep a package's source hidden from another team?

**A:** No. It assigns review ownership; repository read permissions govern source access. Use separate repositories when confidential code needs a separate read boundary.

Source: [Nx](40.8.03-nx.md)

**Q:** A UI project may depend on targets tagged UI or util. Why might an API library tagged util pass unexpectedly?

**A:** The allowed tag list is an OR condition. Separate scope constraints from type constraints so a utility label cannot bypass a required scope boundary.

Source: [Versioning & Publishing](40.8.05-versioning-publishing-strategies.md)

**Q:** Does enabling npm provenance remove the need for publish authorization?

**A:** No. Provenance supplies verifiable build-origin information; trusted publishing or a scoped credential authorizes the registry operation. Verify both independently against npm’s [trusted-publisher](https://docs.npmjs.com/trusted-publishers/) and [provenance](https://docs.npmjs.com/generating-provenance-statements/) guidance.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
