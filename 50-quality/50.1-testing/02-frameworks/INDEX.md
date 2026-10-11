# Testing Frameworks

> **Study time:** ≈ 37 min of reading (5 files, ~7 min average).
> **5 files.** The runner-tier tools: Jest, Vitest, React Testing Library, and a head-to-head comparison so you can defend a stack choice in an interview.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What this category covers

Choosing a framework affects the whole team for a long time: configuration, plugins, continuous integration (CI) time and later migration work. These four chapters show how to use the main JavaScript and TypeScript options and decide which fits your project.

---

## The 4 files

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Jest](50.1.2.01-jest.md) | Configuration, matchers, snapshots, mocking, code coverage | Existing Jest suites; configured Node/DOM tests | Essential | Foundational | 10 min |
| 02 | [Vitest](50.1.2.02-vitest.md) | Module transforms, runtime choices, controlled retries, migration differences, worker pools | Vite-aligned tooling; verify runtime and measured performance | Essential | Foundational | 9 min |
| 03 | [React Testing Library](50.1.2.03-react-testing-library.md) | Render, queries, events, async testing, accessibility (testing-library/jest-dom) | React component tests | Essential | Foundational | 11 min |
| 04 | [Testing Frameworks Comparison](50.1.2.04-testing-frameworks-comparison.md) | Jest vs Vitest, Playwright for E2E, Supertest for APIs, choosing the right framework | Stack decisions | Essential | Foundational | 5 min |

---

## Reading Passes

1. **Understand the runner:** read [Jest](50.1.2.01-jest.md) for discovery, environment, awaited assertions and mock lifecycle. Trace the controlled notification failure before comparing APIs.
2. **Reuse the toolchain:** read [Vitest](50.1.2.02-vitest.md) for module/runtime choices, a bounded retry trace and migration checks. Measure speed on the actual suite.
3. **Observe the interface:** use [React Testing Library](50.1.2.03-react-testing-library.md) to test behavior through the rendered DOM. Distinguish an emulator from a real browser.
4. **Choose by boundary:** read [the comparison](50.1.2.04-testing-frameworks-comparison.md), complete [revision](REVISION.md), then practice interview explanations. Node, HTTP integration and browser journeys can require different tools.

## Cross-References

- [Foundations](../01-foundations/INDEX.md) — the strategy these tools serve.
- [Mocking & Patterns](../04-mocking-and-patterns/INDEX.md) — Jest/Vitest mocking mechanics in depth.

---

## Navigation

[← Foundations](../01-foundations/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Test Levels →](../03-test-levels/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Shared Vitest runner config | `vitest.shared.config.ts` (workspace-wide base config) |
| Playwright as E2E runner | `apps/app/playwright.config.ts`, `apps/internal/playwright.config.ts`, `apps/landing/playwright.config.ts` |
| Component tests (RTL-style) | Component test files under `packages/ui` |
| Visual regression | `packages/ui/tests/visual/status-badge.spec.ts` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
