# Testing Frameworks

> **4 files.** The runner-tier tools: Jest, Vitest, React Testing Library, and a head-to-head comparison so you can defend a stack choice in an interview.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What this category covers

Picking a framework is a team-level decision with long tail costs (config, plugins, CI time, migration pain). These four files give you working fluency in the dominant JS/TS options and the judgment to choose between them.

---

## The 4 files

| #  | File                                                                        | Topics                                                                               | When to use                                      | Read time |
| --:  | ------                                                                        | --------                                                                               | -------------                                      | ----------: |
| 01 | [Jest](50.1.2.01-jest.md)                                                   | Configuration, matchers, snapshots, mocking, code coverage                           | Most React/Node projects — the default ecosystem | 30 min    |
| 02 | [Vitest](50.1.2.02-vitest.md)                                               | Native ESM, Vite integration, HMR, Jest-compatible API, worker threads               | Vite-based projects; faster runs                 | 30 min    |
| 03 | [React Testing Library](50.1.2.03-react-testing-library.md)                 | Render, queries, events, async testing, accessibility (testing-library/jest-dom)     | React component tests                            | 30 min    |
| 04 | [Testing Frameworks Comparison](50.1.2.04-testing-frameworks-comparison.md) | Jest vs Vitest, Playwright for E2E, Supertest for APIs, choosing the right framework | Stack decisions                                  | 20 min    |

---

## Choosing quickly

```text
Vite-based app? ────────────→ Vitest (Jest-compatible, faster)
Legacy CRA / big Jest suite? → stay on Jest (migration cost > benefit)
Testing React components? ──→ + React Testing Library (always)
E2E? ───────────────────────→ Playwright (not a *unit* framework — see comparison)
```

The full decision matrix lives in the [comparison chapter](50.1.2.04-testing-frameworks-comparison.md).

---

## Common signals in interviews

- "Why did your team choose Vitest over Jest?" — answer with ESM support, speed, config reuse.
- "RTL vs Enzyme?" — behavior vs implementation; RTL queries by role/text, Enzyme by internals.
- "What does snapshot testing catch, and what does it miss?"

---

## Cross-References

- [Foundations](../01-foundations/INDEX.md) — the strategy these tools serve.
- [Mocking & Patterns](../04-mocking-and-patterns/INDEX.md) — Jest/Vitest mocking mechanics in depth.

---

## Navigation

[← Foundations](../01-foundations/INDEX.md) · [↑ Testing Home](../INDEX.md) · [Next: Test Levels →](../03-test-levels/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic                       | Docita evidence                                                                                            |
| -------                       | -----------------                                                                                            |
| Shared Vitest runner config | `vitest.shared.config.ts` (workspace-wide base config)                                                     |
| Playwright as E2E runner    | `apps/app/playwright.config.ts`, `apps/internal/playwright.config.ts`, `apps/landing/playwright.config.ts` |
| Component tests (RTL-style) | 27 `*.test.tsx` under `packages/ui`                                                                        |
| Visual regression           | `packages/ui/tests/visual/status-badge.spec.ts`                                                            |
