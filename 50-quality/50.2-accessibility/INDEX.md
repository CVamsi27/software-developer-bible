# Accessibility — Index

> **Study time:** ≈ 1 h 4 m of reading (10 files, ~6 min average).
> **10 files** — Web accessibility from WCAG and ARIA to keyboard navigation, accessible charts, design systems, testing, color & contrast, forms, and interview questions.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

## Follow one accessibility review from requirement to evidence

1. Start with [WCAG](50.2.01-wcag-overview.md): name the target version and level, then define the user task and evaluation scope.
2. Read [ARIA](50.2.02-aria.md) and [Keyboard Navigation](50.2.03-keyboard-navigation.md) together. Trace one control from its exposed meaning through focus, activation and state change.
3. Check what users can see and enter with [Color & Contrast](50.2.04-color-and-contrast.md) and [Forms & Labels](50.2.05-forms-and-labels.md). Follow the same form from its label to an error the user can correct.
4. If the product contains charts or shared UI, continue with [Accessible Charts & Data Visualization](50.2.06-accessible-charts-data-viz.md) and [Accessibility in Design Systems](50.2.07-accessibility-design-systems.md). Keep equivalent data, interaction and consumer responsibilities explicit.
5. Finish with [Testing Accessibility](50.2.08-testing-a11y.md): repeat the task in its important states, combine automated and human checks, and record what the evidence does not establish.

Close the chapters and complete the [revision questions](REVISION.md). Then use the [interview bank](50.2.09-interview-questions.md) to explain the decisions and respond to changed conditions.

## Cross-References

- [Performance Monitoring](../50.3-performance-monitoring/INDEX.md) — Lighthouse a11y audits
- [React (ARIA)](../../10-frontend/10.3-react/INDEX.md) — ARIA patterns in React
- [Testing (RTL)](../50.1-testing/INDEX.md) — testing-library/jest-dom for a11y assertions
- [HTML/CSS](../../10-frontend/10.7-html-css/INDEX.md) — semantic HTML

---

## Navigation

[← Previous: Testing](../50.1-testing/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Performance Monitoring →](../50.3-performance-monitoring/INDEX.md)

---

## Optional repository exercise: Docita

[Docita](https://github.com/CVamsi27/docita) gives you a real React application to trace after the concepts. Follow an audit result into its browser test and focus styles; verify the actual assertions and tested states before treating a report as evidence of a complete journey.

| Topic | Docita evidence |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Automated a11y audit script | `scripts/perf/accessibility-audit.ts` + `run-app-accessibility-audit.mjs` |
| A11y budget gate (CI-style) | `scripts/perf/check-a11y-budget.mjs` + `sync-a11y-baseline.mjs` |
| A11y E2E coverage | `apps/app/e2e/accessibility.spec.ts` |
| Keyboard focus styling | `focus-visible` rules in `packages/ui/src/styles/globals.css` and form components (`switch.tsx`, `radio-group.tsx`, …) |
