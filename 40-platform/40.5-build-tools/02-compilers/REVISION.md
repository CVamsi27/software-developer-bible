<!-- section: Build Tools | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Build%20Tools-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Build Tools — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Babel

Source: [Babel](40.5.2.01-babel.md)

**Q:** Why does syntax transformation not guarantee browser API support?

**A:** A transform can rewrite language syntax while APIs such as fetch or Intl still need target-environment support or a deliberate polyfill strategy.

**Q:** What do presets and plugins configure at different levels?

**A:** A plugin performs a transform; a preset groups/configures transforms for a broader target or framework. Their ordering can change output.

**Q:** Why does a target list matter to emitted code size?

**A:** It determines which syntax needs lowering and which optional polyfills are selected. Broadening targets can add compatibility code that modern-only output does not need.

**Q:** A Babel 7 project used `useBuiltIns` and `corejs` in `preset-env`. What must be checked before moving to Babel 8?

**A:** Babel 8 removed those options from `preset-env` and removed `corejs` from `transform-runtime`; configure `babel-plugin-polyfill-corejs3` for Babel-managed `core-js` injection. Also check the new default targets/module output and Babel 8's Node.js minimum. See the [Babel 8 migration guide](https://babeljs.io/docs/v8-migration/).

## ESBuild & SWC

Source: [ESBuild & SWC](40.5.2.02-esbuild-swc.md)

**Q:** How does type stripping differ from checking TypeScript?

**A:** Stripping removes type syntax to emit JavaScript. A checker verifies type relationships; declaration generation is another output step. A fast bundle does not replace either.

**Q:** Why compare compiler output as well as elapsed time?

**A:** Class fields, decorators, target lowering, interop, and source maps can differ. A faster transform must preserve the application's required runtime behavior.

**Q:** How do esbuild and SWC differ when a project needs browser API polyfills?

**A:** esbuild transforms syntax but leaves API polyfills to another stage. SWC can opt in through `env.mode` with a pinned `env.coreJs` version; this does not cover every Web API. Compare the [esbuild target contract](https://esbuild.github.io/api/#target) with [SWC's supported-browser configuration](https://swc.rs/docs/configuration/supported-browsers).

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — return to prerequisites and compare the tool’s output boundary

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
