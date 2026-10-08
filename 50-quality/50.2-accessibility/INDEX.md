# Accessibility — Index

> **Study time:** ≈ 1 h 14 m of reading (10 files, ~7 min average).
> **10 files** — Web accessibility from WCAG and ARIA to keyboard navigation, accessible charts, design systems, testing, color & contrast, forms, and interview questions.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

## Read from the task to its implemented evidence

Start with the barriers and the WCAG target, then connect semantic meaning to keyboard behavior, visible information and recoverable input. Continue through equivalent data and shared components before evaluating complete journeys. The [section revision](REVISION.md) belongs after the learning chapters and before interview practice.

## Topic Categories

| Category | Files | Why it matters |
| -------------------------------------------------- | ----: | ------------------------------------------------------ |
| [Standards](#standards) | 1 | Principles, criteria, target version and process scope |
| [Semantic HTML & ARIA](#semantic-html--aria) | 1 | Roles, names, states and behavior boundaries |
| [Interaction](#interaction) | 2 | Keyboard navigation, forms — how users interact |
| [Visual Design](#visual-design) | 1 | Rendered contrast pairs, non-color cues and themes |
| [Charts & Design Systems](#charts--design-systems) | 2 | Data viz a11y, primitives + governance — scaling a11y |
| [Testing & Interview](#testing--interview) | 2 | Evaluation methods and original interview questions |

---

## Standards

Name the target version/level and understand principles, criteria, techniques and complete-process scope.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [WCAG Overview](50.2.01-wcag-overview.md) | POUR principles (Perceivable, Operable, Understandable, Robust), conformance levels A/AA/AAA, success criteria | Essential | Foundational | 5 min |

## Semantic HTML & ARIA

Trace the disclosure before comparing roles, names, states and relationships. Exposed meaning and working behavior are separate responsibilities.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 02 | [ARIA](50.2.02-aria.md) | Roles, states, properties, ARIA patterns (combobox, dialog, menu), best practices, when NOT to use | Essential | Foundational | 6 min |

**Rule of thumb:** Semantic HTML first, ARIA second. ARIA is for filling gaps, not replacing HTML.

---

## Interaction

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 03 | [Keyboard Navigation](50.2.03-keyboard-navigation.md) | Tab order, focus management, focus traps, skip links, keyboard shortcuts, visible focus | Essential | Foundational | 10 min |
| 05 | [Forms & Labels](50.2.05-forms-and-labels.md) | Label association, validation, fieldset/legend, autocomplete, error handling, accessible error messages | Essential | Foundational | 10 min |

---

## Visual Design

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Color & Contrast](50.2.04-color-and-contrast.md) | WCAG 1.4.3 contrast ratios (4.5:1 text, 3:1 UI), color-vision-deficiency-safe palettes, forced-colors mode | Essential | Foundational | 7 min |

---

## Charts & Design Systems

Preserve both a chart’s information and tasks, then assign shared-component and consumer responsibilities.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [Accessible Charts & Data Viz](50.2.06-accessible-charts-data-viz.md) | SVG chart a11y (`role="img"`, labels), table fallbacks, color independence, sonification, screen-reader testing of dashboards, Recharts/Highcharts gaps | Optional | Specialized | 9 min |
| 07 | [Accessibility Design Systems](50.2.07-accessibility-design-systems.md) | Radix/React Aria primitives, focus management baked in, contrast tokens, jsx-a11y + CI gates, definition-of-done governance, audit-to-component pipeline | Optional | Specialized | 8 min |

A shared fix reaches a product only after adoption, correct composition and evaluation of its actual journey.

---

## Testing & Interview

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [Testing A11y](50.2.08-testing-a11y.md) | Automated tools (axe-core, Lighthouse), manual testing, screen readers (NVDA, VoiceOver, JAWS), keyboard-only testing | Essential | Foundational | 8 min |
| 09 | [Interview Questions](50.2.09-interview-questions.md) | Original questions, reasoned answers and changed-condition probes | Essential | Foundational | 8 min |

---

## Learning passes

1. **Meaning and operation:** WCAG, ARIA and keyboard chapters connect the task, accessibility representation and complete interaction lifecycle. Reproduce the disclosure, tabs and dialog transitions.
2. **Perception and recovery:** contrast and forms explain actual rendered pairs, names/descriptions, invalid state, feedback and correction. Change a theme or error condition and predict the result.
3. **Information and reuse:** charts preserve insight, exact data and interaction; design systems define layer contracts, evaluation and adoption.
4. **Evidence:** testing distinguishes encoded rules, browser input, manual meaning and assistive-technology evaluation. Inspect violations, incomplete checks and scope.
5. **Revision, then interview:** complete [revision](REVISION.md) before the [interview bank](50.2.09-interview-questions.md), using its probes to vary a consequential condition.

## Cross-References

- [Performance Monitoring](../50.3-performance-monitoring/INDEX.md) — Lighthouse a11y audits
- [React (ARIA)](../../10-frontend/10.3-react/INDEX.md) — ARIA patterns in React
- [Testing (RTL)](../50.1-testing/INDEX.md) — testing-library/jest-dom for a11y assertions
- [HTML/CSS](../../10-frontend/10.7-html-css/INDEX.md) — semantic HTML

---

## Navigation

[← Previous: Testing](../50.1-testing/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Performance Monitoring →](../50.3-performance-monitoring/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) supplies companion artifacts to inspect. Verify their current assertions, revision and evaluated states before claiming a pass; a script’s existence does not establish keyboard or screen-reader task completion.

| Topic | Docita evidence |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Automated a11y audit script | `scripts/perf/accessibility-audit.ts` + `run-app-accessibility-audit.mjs` |
| A11y budget gate (CI-style) | `scripts/perf/check-a11y-budget.mjs` + `sync-a11y-baseline.mjs` |
| A11y E2E coverage | `apps/app/e2e/accessibility.spec.ts` |
| Keyboard focus styling | `focus-visible` rules in `packages/ui/src/styles/globals.css` and form components (`switch.tsx`, `radio-group.tsx`, …) |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
