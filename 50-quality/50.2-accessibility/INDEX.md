# Accessibility — Index

> **9 files** — Web accessibility from WCAG and ARIA to keyboard navigation, accessible charts, design systems, testing, color & contrast, forms, and interview questions.

[![Files](https://img.shields.io/badge/files-9-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why accessibility:** Legal requirement in many jurisdictions (ADA, EAA, Section 508), ethical imperative, and increasingly tested in senior interviews. ~15% of users have some form of disability. WCAG 2.1 AA is the standard most companies aim for. The basics are quick to learn and high-leverage in interviews.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Standards](#standards) | 1 | WCAG (POUR, levels) — the rule book |
| [Semantic HTML & ARIA](#semantic-html--aria) | 1 | ARIA roles, states, properties — extending semantics |
| [Interaction](#interaction) | 2 | Keyboard navigation, forms — how users interact |
| [Visual Design](#visual-design) | 1 | Color, contrast, CVD-safe palettes — the visual side |
| [Charts & Design Systems](#charts--design-systems) | 2 | Data viz a11y, primitives + governance — scaling a11y |
| [Testing & Interview](#testing--interview) | 2 | A11y testing, 50+ Qs |

---

## Standards

The rule book.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [WCAG Overview](50.2.01-wcag-overview.md) | POUR principles (Perceivable, Operable, Understandable, Robust), conformance levels A/AA/AAA, success criteria | 30 min |

**POUR (memorize):**
- **P**erceivable — users can perceive the content (alt text, captions, color contrast)
- **O**perable — users can operate the UI (keyboard, no seizures, navigation)
- **U**nderstandable — users can understand (readable, predictable, input assistance)
- **R**obust — works with assistive tech (valid HTML, ARIA)

---

## Semantic HTML & ARIA

The foundation — semantic HTML is 90% of accessibility.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [ARIA](50.2.02-aria.md) | Roles, states, properties, ARIA patterns (combobox, dialog, menu), best practices, when NOT to use | 30 min |

**Rule of thumb:** Semantic HTML first, ARIA second. ARIA is for filling gaps, not replacing HTML.

---

## Interaction

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Keyboard Navigation](50.2.03-keyboard-navigation.md) | Tab order, focus management, focus traps, skip links, keyboard shortcuts, visible focus | 25 min |
| 05 | [Forms & Labels](50.2.05-forms-and-labels.md) | Label association, validation, fieldset/legend, autocomplete, error handling, accessible error messages | 25 min |

---

## Visual Design

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Color & Contrast](50.2.04-color-and-contrast.md) | WCAG 1.4.3 contrast ratios (4.5:1 text, 3:1 UI), color-vision-deficiency-safe palettes, forced-colors mode | 25 min |

---

## Charts & Design Systems

Where accessibility scales (or dies): dashboards and shared components.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Accessible Charts & Data Viz](50.2.06-accessible-charts-data-viz.md) | SVG chart a11y (`role="img"`, labels), table fallbacks, color independence, sonification, screen-reader testing of dashboards, Recharts/Highcharts gaps | 25 min |
| 07 | [Accessibility Design Systems](50.2.07-accessibility-design-systems.md) | Radix/React Aria primitives, focus management baked in, contrast tokens, jsx-a11y + CI gates, definition-of-done governance, audit-to-component pipeline | 25 min |

**Rule of thumb:** fix a11y once in the design system — every product inherits it.

---

## Testing & Interview

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 08 | [Testing A11y](50.2.08-testing-a11y.md) | Automated tools (axe-core, Lighthouse), manual testing, screen readers (NVDA, VoiceOver, JAWS), keyboard-only testing | 25 min |
| 09 | [Interview Questions](50.2.09-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## Suggested Study Order

1. **WCAG Overview** — must know the framework
2. **ARIA** — the most-asked a11y topic
3. **Keyboard Navigation** — must know
4. **Forms & Labels** — must know
5. **Color & Contrast** — quick win
6. **Accessible Charts / Design Systems** — for senior roles with dashboards or DS ownership
7. **Testing A11y** — for senior roles
8. **Interview Questions** — final review

---

## Common interview topics

- "What is WCAG? What are the POUR principles?"
- "What's the difference between ARIA roles and HTML semantics?"
- "How do you make a custom dropdown accessible?"
- "What's the minimum contrast ratio for text?"
- "How do you test accessibility?"
- "How do you make a modal accessible?" (focus trap, ESC to close, return focus)

---

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

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
|-------|-----------------|
| Automated a11y audit script | `scripts/perf/accessibility-audit.ts` + `run-app-accessibility-audit.mjs` |
| A11y budget gate (CI-style) | `scripts/perf/check-a11y-budget.mjs` + `sync-a11y-baseline.mjs` |
| A11y E2E coverage | `apps/app/e2e/accessibility.spec.ts` |
| Keyboard focus styling | `focus-visible` rules in `packages/ui/src/styles/globals.css` and form components (`switch.tsx`, `radio-group.tsx`, …) |
