<!-- section: Accessibility | category: Reference | tags: revision, practice| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Accessibility-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../docs/topic-importance.md)

# Accessibility — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## WCAG Overview

Source: [WCAG Overview](50.2.01-wcag-overview.md)

**Q:** Why does automated WCAG testing not establish conformance?

**A:** Tools detect a subset of failures. Keyboard flows, meaningful alternatives, focus order, language, and assistive-technology behavior require human evaluation.

## ARIA (Accessible Rich Internet Applications)

Source: [ARIA (Accessible Rich Internet Applications)](50.2.02-aria.md)

**Q:** Why does role button not make a div behave like a native button?

**A:** ARIA changes semantics, not keyboard behavior or focusability. A custom control needs activation, focus, disabled state, and interaction logic; prefer the native element.

## Keyboard Navigation

Source: [Keyboard Navigation](50.2.03-keyboard-navigation.md)

**Q:** Why should Tab reach the widget but not necessarily every item?

**A:** Composite widgets often use one tab stop and arrow-key movement via roving tabindex or aria-activedescendant. Match the widget's established interaction pattern.

## Color & Contrast

Source: [Color & Contrast](50.2.04-color-and-contrast.md)

**Q:** How do text contrast and non-text contrast requirements differ?

**A:** Normal text generally requires 4.5:1 at AA, large text 3:1; necessary component boundaries/states and graphical objects have separate 3:1 rules and exceptions. Check the relevant criterion.

## Forms & Labels

Source: [Forms & Labels](50.2.05-forms-and-labels.md)

**Q:** Why is a placeholder insufficient as a form label?

**A:** It disappears during input and may not provide a reliable accessible name. Associate a persistent label and connect relevant help/errors programmatically.

## Accessible Charts & Data Visualization

Source: [Accessible Charts & Data Visualization](50.2.06-accessible-charts-data-viz.md)

**Q:** How can a chart expose information beyond a colored picture?

**A:** Provide a useful text summary and accessible data representation, and make any interaction keyboard/screen-reader usable. A title alone cannot communicate all values and relationships.

## Accessibility in Design Systems

Source: [Accessibility in Design Systems](50.2.07-accessibility-design-systems.md)

**Q:** Why can an accessible component library still produce an inaccessible page?

**A:** Consumers choose labels, composition, content, focus flow, and states. Define usage contracts and test complete journeys, not only isolated components.

## Testing Accessibility

Source: [Testing Accessibility](50.2.08-testing-a11y.md)

**Q:** What should a keyboard-only test observe?

**A:** Reachability, visible focus, logical order, expected keys, modal trapping/escape where appropriate, and focus restoration. Combine it with screen-reader and automated checks.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
