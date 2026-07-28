---
section: Accessibility
category: Quality
tags: [concept]
---

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

```text
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


## Summary
ARIA enhances accessibility for complex web applications. Use it when native HTML is insufficient, follow established patterns, and test with screen readers. Remember: first rule of ARIA is don't use ARIA if you can use native HTML.

---

## See Also
- [React](../03-React/)
- [Testing](../16-Testing/)
- [Performance Monitoring](../26-Performance-Monitoring/)

## References & Learn More

- [WAI-ARIA Specification](https://www.w3.org/TR/wai-aria/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN ARIA Documentation](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
- [WebAIM ARIA Introduction](https://webaim.org/techniques/aria/)
- [Deque ARIA Resources](https://www.deque.com/aria/)
