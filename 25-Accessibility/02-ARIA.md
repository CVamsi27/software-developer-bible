# ARIA (Accessible Rich Internet Applications)

## Definition
ARIA (Accessible Rich Internet Applications) is a set of attributes that define ways to make web content and web applications more accessible to people with disabilities. It provides additional semantics for dynamic content and complex UI components.

## Why Do We Need It?
- **Complex components**: Native HTML lacks semantics for custom widgets
- **Dynamic content**: Live regions for real-time updates
- **Enhanced semantics**: Better screen reader support
- **State information**: Communicate UI state to assistive technology
- **Role definition**: Define purpose of custom elements

## How It Works
ARIA has three main categories: Roles, States, and Properties:

### ARIA Categories
```
┌─────────────────────────────────────────────────────────────────┐
│                    ARIA Categories                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Roles              States             Properties               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  Define     │    │  Describe   │    │  Provide additional │ │
│  │  element    │    │  current    │    │  semantics          │ │
│  │  purpose    │    │  condition  │    │                     │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### ARIA Roles
```html
<!-- Landmark roles -->
<div role="banner">Site header</div>
<div role="navigation">Main nav</div>
<div role="main">Main content</div>
<div role="complementary">Sidebar</div>
<div role="contentinfo">Footer</div>
<div role="search">Search</div>

<!-- Widget roles -->
<div role="button">Click me</div>
<div role="checkbox" aria-checked="false">Option</div>
<div role="tablist">
  <div role="tab" aria-selected="true">Tab 1</div>
  <div role="tab" aria-selected="false">Tab 2</div>
</div>
<div role="tabpanel">Tab content</div>

<!-- Live region roles -->
<div role="alert">Error message</div>
<div role="status">Status update</div>
<div role="timer">Countdown</div>
```

### ARIA States
```html
<!-- Checkbox state -->
<div
  role="checkbox"
  aria-checked="true"
  tabindex="0">
  Option
</div>

<!-- Expanded state -->
<button
  aria-expanded="true"
  aria-controls="menu1">
  Menu
</button>
<div id="menu1" role="menu">
  <div role="menuitem">Item 1</div>
</div>

<!-- Selected state -->
<div role="tab" aria-selected="true">Active Tab</div>

<!-- Disabled state -->
<button aria-disabled="true">Disabled</button>

<!-- Hidden state -->
<div aria-hidden="true">Hidden from screen readers</div>

<!-- Invalid state -->
<input
  type="email"
  aria-invalid="true"
  aria-describedby="email-error">
<div id="email-error" role="alert">Invalid email</div>
```

### ARIA Properties
```html
<!-- Label properties -->
<input aria-label="Search">
<input aria-labelledby="label1">
<label id="label1">Name</label>

<!-- Description properties -->
<input aria-describedby="hint1">
<div id="hint1">Enter your email address</div>

<!-- Required property -->
<input aria-required="true">

<!-- Autocomplete property -->
<input autocomplete="email">

<!-- Current property (navigation) -->
<a aria-current="page" href="/current">Current Page</a>

<!-- Active descendant property -->
<div role="listbox" aria-activedescendant="option1">
  <div role="option" id="option1">Option 1</div>
</div>
```

### Complex Widget Patterns
```html
<!-- Tabs -->
<div role="tablist" aria-label="Tabs">
  <button
    role="tab"
    id="tab1"
    aria-selected="true"
    aria-controls="panel1"
    tabindex="0">
    Tab 1
  </button>
  <button
    role="tab"
    id="tab2"
    aria-selected="false"
    aria-controls="panel2"
    tabindex="-1">
    Tab 2
  </button>
</div>

<div
  role="tabpanel"
  id="panel1"
  aria-labelledby="tab1"
  tabindex="0">
  Panel 1 content
</div>

<div
  role="tabpanel"
  id="panel2"
  aria-labelledby="tab2"
  tabindex="0"
  hidden>
  Panel 2 content
</div>

<!-- Modal dialog -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc">
  <h2 id="dialog-title">Dialog Title</h2>
  <p id="dialog-desc">Dialog description</p>
  <button autofocus>Close</button>
</div>

<!-- Accordion -->
<div>
  <h3>
    <button
      aria-expanded="true"
      aria-controls="section1">
      Section 1
    </button>
  </h3>
  <div
    id="section1"
    role="region"
    aria-labelledby="section1-heading">
    <p>Section 1 content</p>
  </div>
</div>
```

### Live Regions
```html
<!-- Polite: Waits for user to finish -->
<div aria-live="polite" aria-atomic="true">
  Content updates will be announced politely
</div>

<!-- Assertive: Interrupts immediately -->
<div aria-live="assertive">
  Urgent message
</div>

<!-- Status: Implicit polite -->
<div role="status">
  3 items in cart
</div>

<!-- Alert: Implicit assertive -->
<div role="alert">
  Error: Invalid input
</div>

<!-- Timer -->
<div role="timer" aria-live="off" aria-label="Countdown">
  05:00
</div>
```

### Form Accessibility
```html
<!-- Required fields -->
<div>
  <label for="email">
    Email <span aria-hidden="true">*</span>
    <span class="sr-only">(required)</span>
  </label>
  <input
    type="email"
    id="email"
    aria-required="true"
    aria-invalid="false"
    aria-describedby="email-hint">
  <div id="email-hint">We'll never share your email</div>
  <div id="email-error" role="alert" aria-live="polite"></div>
</div>

<!-- Password strength -->
<div>
  <label for="password">Password</label>
  <input
    type="password"
    id="password"
    aria-describedby="password-strength"
    aria-invalid="false">
  <div id="password-strength" aria-live="polite">
    Password strength: <span>Weak</span>
  </div>
</div>

<!-- Search -->
<form role="search" aria-label="Site search">
  <label for="search-input">Search</label>
  <input
    type="search"
    id="search-input"
    aria-describedby="search-hint">
  <div id="search-hint">Type to search</div>
  <button type="submit">Search</button>
</form>
```

### Navigation Patterns
```html
<!-- Breadcrumb -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/widget" aria-current="page">Widget</a></li>
  </ol>
</nav>

<!-- Pagination -->
<nav aria-label="Pagination">
  <a href="/page1" aria-label="Previous page">←</a>
  <a href="/page1" aria-label="Page 1">1</a>
  <a href="/page2" aria-current="page" aria-label="Page 2, current page">2</a>
  <a href="/page3" aria-label="Page 3">3</a>
  <a href="/page3" aria-label="Next page">→</a>
</nav>

<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>
```

## Real-World Use Cases
1. **Custom widgets**: Tabs, accordions, modals, tooltips
2. **Dynamic content**: Real-time updates, notifications
3. **Complex forms**: Multi-step forms, validation
4. **Data tables**: Sortable, filterable tables
5. **Charts and graphs**: Data visualization accessibility
6. **Rich text editors**: Editable content areas

## Common Mistakes
1. **Using ARIA when native HTML suffices**: Don't add ARIA if not needed
2. **Wrong role usage**: Using roles incorrectly
3. **Missing required states**: Not providing all required ARIA states
4. **Overusing aria-label**: When visible text is better
5. **Not testing with screen readers**: ARIA doesn't work without testing
6. **Conflicting ARIA**: Multiple ARIA attributes contradicting
7. **Dynamic ARIA not updated**: States not updated with JavaScript

## Best Practices
1. **Use native HTML first**: ARIA is last resort
2. **Follow WAI-ARIA Authoring Practices**: Use established patterns
3. **Test with screen readers**: NVDA, JAWS, VoiceOver
4. **Keep ARIA minimal**: Only add what's needed
5. **Update ARIA dynamically**: Keep states in sync
6. **Use aria-live sparingly**: Only for important updates
7. **Provide fallbacks**: For older browsers
8. **Document ARIA usage**: Team understanding

## Performance Considerations
- **Minimal impact**: ARIA attributes don't affect rendering
- **Screen reader performance**: Complex ARIA can slow screen readers
- **Dynamic updates**: Frequent updates can be overwhelming
- **Caching**: Screen readers cache page structure

## Interview Questions

### Beginner (5-10)
1. **What is ARIA?**
   - Accessible Rich Internet Applications, attributes for accessibility.

2. **What are the three types of ARIA?**
   - Roles, States, and Properties.

3. **When should you use ARIA?**
   - When native HTML semantics are insufficient for complex widgets.

4. **What is `aria-label`?**
   - Provides accessible name for element without visible text.

5. **What is `aria-describedby`?**
   - Associates element with description for additional context.

6. **What is a live region?**
   - Area that updates dynamically, announced to screen readers.

7. **What is the difference between `aria-hidden` and `hidden`?**
   - aria-hidden hides from screen readers only, hidden hides from all.

8. **What is `role="button"`?**
   - Defines element as interactive button for screen readers.

### Intermediate (5-10)
9. **When should you NOT use ARIA?**
   - When native HTML provides same semantics (use button, not role="button").

10. **What is `aria-expanded`?**
    - Indicates whether collapsible section is expanded or collapsed.

11. **How do you make a custom dropdown accessible?**
    - role="listbox", aria-expanded, aria-activedescendant, keyboard navigation.

12. **What is `aria-live` and its values?**
    - Indicates live region, values: polite, assertive, off.

13. **How do you handle focus in modals?**
    - Trap focus, return focus on close, aria-modal="true".

14. **What is `aria-controls`?**
    - Associates element with controlled element (like dropdown menu).

15. **How do you make drag-and-drop accessible?**
    - Provide keyboard alternative, aria-grabbed, aria-dropeffect.

16. **What is `aria-activedescendant`?**
    - Manages focus in composite widgets without moving DOM focus.

### Senior (10-15)
17. **How do you implement ARIA in a design system?**
    - Component guidelines, documentation, testing, examples.

18. **What are the WAI-ARIA Authoring Practices?**
    - Patterns for common widgets with ARIA examples and keyboard interaction.

19. **How do you test ARIA implementation?**
    - Screen readers, axe-core, manual testing, automated tools.

20. **What is the difference between `aria-label` and `aria-labelledby`?**
    - label provides text,-labelledby references visible text.

21. **How do you handle ARIA in SPAs?**
    - Live regions for route changes, focus management, dynamic content.

22. **What is `role="presentation"`?**
    - Removes semantic meaning from element (for layout tables).

23. **How do you make charts accessible with ARIA?**
    - Text alternatives, keyboard navigation, data tables as alternative.

24. **What is `aria-busy`?**
    - Indicates element is being updated, screen readers should wait.

### FAANG-style (5-10)
25. **Design an ARIA testing strategy for a complex application.**
    - Automated testing, manual audits, screen reader testing, user feedback.

26. **How would you make a rich text editor accessible?**
    - ARIA properties, keyboard shortcuts, role="textbox", aria-multiline.

27. **What are the challenges of ARIA in micro-frontends?**
    - Consistent patterns, shared components, focus management across boundaries.

28. **How do you prioritize ARIA implementation?**
    - User impact, legal requirements, effort, frequency of use.

29. **Design an accessible data table component.**
    - role="grid", aria-sort, aria-selected, keyboard navigation.

### Follow-ups (5-10)
30. **How does ARIA affect SEO?**
    - Minimal direct impact, but better semantics can help.

31. **What is the future of ARIA?**
    - Better browser support, more native semantics, tooling improvements.

32. **How do you handle ARIA with framework components?**
    - Framework-specific patterns, component libraries, documentation.

33. **What are common ARIA mistakes in React/Vue?**
    - Missing state updates, wrong role usage, overcomplicating.

34. **How do you train developers on ARIA?**
    - Workshops, documentation, code reviews, testing exercises.

## Summary
ARIA enhances accessibility for complex web applications. Use it when native HTML is insufficient, follow established patterns, and test with screen readers. Remember: first rule of ARIA is don't use ARIA if you can use native HTML.

## References & Learn More
- [WAI-ARIA Specification](https://www.w3.org/TR/wai-aria/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN ARIA Documentation](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
- [WebAIM ARIA Introduction](https://webaim.org/techniques/aria/)
- [Deque ARIA Resources](https://www.deque.com/aria/)