<!-- section: Accessibility | category: Reference | tags: revision, practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Accessibility-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../docs/topic-importance.md)

# Accessibility — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## WCAG Overview

Source: [WCAG Overview](50.2.01-wcag-overview.md)

**Q:** Why does automated WCAG testing not establish conformance?

**A:** Tools detect a subset of failures. Keyboard flows, meaningful alternatives, focus order, language, and assistive-technology behavior require human evaluation.

**Q:** How does the booking-error trace connect a visible failure to correction?

**A:** Identify the field and error in text, associate them programmatically, provide a usable return path and clear obsolete state after correction. Each step addresses a different part of the task.

**Q:** Can a passing first checkout page establish AA conformance of the whole checkout?

**A:** No. Name the version and level and evaluate full pages and the complete process, including consequential later steps and supported technology requirements.

## ARIA (Accessible Rich Internet Applications)

Source: [ARIA (Accessible Rich Internet Applications)](50.2.02-aria.md)

**Q:** Why does role button not make a div behave like a native button?

**A:** ARIA tells assistive technology what an element represents; it does not make the element keyboard-operable or able to receive focus. A custom control needs activation, focus, disabled-state handling, and interaction logic. Prefer the native element.

**Q:** What changes when Enter opens the shipping disclosure?

**A:** The native button activates; the script reveals the panel and changes expanded to true. Focus stays on the button and Tab can reach the revealed link. Semantics and behavior derive from the same transition.

**Q:** Does aria-hidden prevent an element from receiving keyboard focus?

**A:** No. It changes the accessibility representation, so an operable descendant can become unidentified. Use the appropriate visibility/inertness behavior instead of hiding its meaning alone.

**Q:** Does following an APG pattern establish that a product conforms to WCAG?

**A:** No. The APG is informative implementation guidance; WCAG and WAI-ARIA specifications define normative requirements. Follow the pattern where it fits, then evaluate the applicable criteria and the complete user task.

## Keyboard Navigation

Source: [Keyboard Navigation](50.2.03-keyboard-navigation.md)

**Q:** Why should Tab reach the widget but not necessarily every item?

**A:** Composite widgets often use one tab stop and arrow-key movement via roving tabindex or aria-activedescendant. Match the widget's established interaction pattern.

**Q:** Why does ArrowRight focus Delivery without displaying its panel in the fixture?

**A:** The example uses manual activation: movement updates focus and the roving Tab stop, while Enter, Space or click changes selection and panel visibility.

**Q:** What changes if a dialog trigger disappears before dismissal?

**A:** Restoring that removed element cannot provide task continuity. Choose a sensible remaining target; custom modality also needs working background blocking and lifecycle cleanup.

## Color & Contrast

Source: [Color & Contrast](50.2.04-color-and-contrast.md)

**Q:** How do text contrast and non-text contrast requirements differ?

**A:** Normal text generally requires 4.5:1 at AA, large text 3:1; necessary component boundaries/states and graphical objects have separate 3:1 rules and exceptions. Check the relevant criterion.

**Q:** Why does #777 on white fail normal-text AA although its ratio rounds to 4.5?

**A:** The unrounded ratio is below the threshold. Use formatting only for display, and compare the actual ratio against the applicable requirement.

**Q:** Does a passing white-surface token guarantee its use on a dark card?

**A:** No. Evaluate the actual foreground/background pair and relevant state. Transparency, inheritance and changing backgrounds can alter the measurement.

## Forms & Labels

Source: [Forms & Labels](50.2.05-forms-and-labels.md)

**Q:** Why is a placeholder insufficient as a form label?

**A:** It disappears during input and may not provide a reliable accessible name. Associate a persistent label and connect relevant help/errors programmatically.

**Q:** Why does the validation fixture remove an error ID from describedby after correction?

**A:** A directly referenced hidden message can still contribute to the description. Clear obsolete content and its relationship, not only its visibility.

**Q:** Do client checks passing establish that the account was created?

**A:** No. The fixture sends no request. Server validation and a confirmed outcome are separate boundaries, and a timeout may leave an unknown result.

## Accessible Charts & Data Visualization

Source: [Accessible Charts & Data Visualization](50.2.06-accessible-charts-data-viz.md)

**Q:** How can a chart expose information beyond a colored picture?

**A:** Provide a useful text summary and accessible data representation, and make any interaction keyboard/screen-reader usable. A title alone cannot communicate all values and relationships.

**Q:** What data supports the example’s Q1-to-Q4 growth summary?

**A:** The increase is 700,000 euros divided by the Q1 baseline of 1,200,000, approximately 58.3%. The same four-quarter array supplies the graphic, summary and exact table.

**Q:** Why can role=img be wrong around an interactive chart?

**A:** It treats the graphic as an atomic image-like object and can conceal independently operable descendants. Expose the required actions with an appropriate navigation/semantic model.

## Accessibility in Design Systems

Source: [Accessibility in Design Systems](50.2.07-accessibility-design-systems.md)

**Q:** Why can an accessible component library still produce an inaccessible page?

**A:** Consumers choose labels, composition, content, focus flow, and states. Define usage contracts and test complete journeys, not only isolated components.

**Q:** Why is a published dialog fix insufficient evidence for every product?

**A:** Consumers may still deploy an older version or compose the component incorrectly. Track adoption and re-evaluate the actual journey after the upgrade.

**Q:** Can a successful JSX lint establish modal focus behavior?

**A:** No. Static rules inspect source relationships; actual open, movement, dismissal and restoration require rendered interaction evaluation.

## Testing Accessibility

Source: [Testing Accessibility](50.2.08-testing-a11y.md)

**Q:** What should a keyboard-only test observe?

**A:** Reachability, visible focus, logical order, expected keys, modal trapping/escape where appropriate, and focus restoration. Combine it with screen-reader and automated checks.

**Q:** What does the browser audit do with violations and incomplete checks?

**A:** Violations and failed interactions cause a nonzero exit. Incomplete findings are retained for review; the example does not turn unresolved manual work into a conformance pass.

**Q:** Why does directly focusing every element not establish natural Tab order?

**A:** It bypasses sequential browser navigation, hidden/disabled behavior and the task’s movement model. Use actual input and observe the resulting focus and state.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — return to operation and perception prerequisites before attempting the interview bank

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
