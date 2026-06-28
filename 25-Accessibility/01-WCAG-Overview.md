# WCAG Overview

## Definition
WCAG (Web Content Accessibility Guidelines) is a set of guidelines developed by W3C (World Wide Web Consortium) to make web content more accessible to people with disabilities. It provides standards for creating accessible web content.

## Why Do We Need It?
- **Legal compliance**: Many countries require accessibility (ADA, Section 508, EAA)
- **Inclusivity**: 15% of world population has some form of disability
- **Better UX**: Accessible sites work better for everyone
- **SEO benefits**: Many accessibility practices improve SEO
- **Market reach**: Access to wider audience
- **Ethical responsibility**: Equal access to information

## How It Works
WCAG is organized around four principles (POUR) and three levels (A, AA, AAA):

### WCAG Structure
```text
┌─────────────────────────────────────────────────────────────────┐
│                    WCAG Structure                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Principles (POUR)                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Perceivable │ │  Operable   │ │  Understandable│ │  Robust │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│                                                                 │
│  Levels                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │  Level A    │ │  Level AA   │ │  Level AAA  │              │
│  │  (Minimum)  │ │  (Standard) │ │  (Enhanced) │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Four Principles (POUR)
```text
Perceivable - Information must be presentable to users
├── Text alternatives for non-text content
├── Captions for multimedia
├── Content adaptable to different presentations
└── Sufficient contrast

Operable - UI components must be operable
├── Keyboard accessible
├── Time limits adjustable
├── No seizure-inducing content
└── Navigation aids

Understandable - Information and UI must be understandable
├── Readable text
├── Predictable behavior
├── Input assistance
└── Error prevention

Robust - Content must be robust for assistive technologies
├── Compatible with current/future tools
├── Valid, well-formed markup
└── Name, role, value for UI components
```

## Code Examples

### Semantic HTML
```html
<!-- Bad: Non-semantic -->
<div class="header">
  <div class="nav">
    <div class="link" onclick="navigate()">Home</div>
  </div>
</div>
<div class="content">
  <div class="title">Page Title</div>
  <div class="text">Content here</div>
</div>

<!-- Good: Semantic -->
<header>
  <nav aria-label="Main navigation">
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <h1>Page Title</h1>
  <p>Content here</p>
</main>
```

### Image Accessibility
```html
<!-- Bad -->
<img src="chart.png">

<!-- Good: Descriptive alt text -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024">

<!-- Good: Decorative image -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- Good: Complex image with long description -->
<figure>
  <img src="complex-chart.png" alt="Revenue growth chart" aria-describedby="chart-desc">
  <figcaption id="chart-desc">
    Detailed description of chart data...
  </figcaption>
</figure>
```

### Form Accessibility
```html
<!-- Bad -->
<div>
  <div>Name</div>
  <input type="text">
</div>

<!-- Good -->
<div>
  <label for="name">Name (required)</label>
  <input type="text" id="name" name="name" required aria-required="true">
  <span id="name-error" aria-live="polite" role="alert"></span>
</div>

<!-- Good: Fieldset and legend -->
<fieldset>
  <legend>Shipping Address</legend>
  <div>
    <label for="street">Street</label>
    <input type="text" id="street" name="street">
  </div>
  <div>
    <label for="city">City</label>
    <input type="text" id="city" name="city">
  </div>
</fieldset>
```

### Landmark Roles
```html
<!-- HTML5 landmarks -->
<header>Site header</header>
<nav aria-label="Main">Main navigation</nav>
<main>
  <article>
    <h1>Article title</h1>
    <section aria-labelledby="section1">
      <h2 id="section1">Section heading</h2>
      <p>Content</p>
    </section>
  </article>
  <aside>Related content</aside>
</main>
<footer>Site footer</footer>

<!-- ARIA landmarks -->
<div role="banner">Header</div>
<div role="navigation">Nav</div>
<div role="main">Main content</div>
<div role="complementary">Aside</div>
<div role="contentinfo">Footer</div>
<div role="search">Search</div>
```

### Color and Contrast
```css
/* Bad: Low contrast */
.text {
  color: #999;  /* On white background - contrast ratio 2.85:1 */
}

/* Good: Sufficient contrast */
.text {
  color: #595959;  /* On white background - contrast ratio 7:1 */
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .text {
    color: #000;
    background: #fff;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

### Keyboard Navigation
```html
<!-- Custom interactive elements -->
<button
  aria-label="Close dialog"
  aria-expanded="false"
  onclick="closeDialog()">
  ×
</button>

<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Focus management -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  tabindex="-1">
  <h2 id="dialog-title">Dialog Title</h2>
  <button autofocus>Close</button>
</div>
```

### Live Regions
```html
<!-- Announce dynamic content changes -->
<div aria-live="polite" aria-atomic="true">
  <!-- Content updates will be announced -->
</div>

<!-- Status messages -->
<div role="status" aria-live="polite">
  Form submitted successfully
</div>

<!-- Error messages -->
<div role="alert" aria-live="assertive">
  Error: Invalid email address
</div>
```

### Tables
```html
<!-- Bad -->
<table>
  <tr>
    <td>Name</td>
    <td>Age</td>
  </tr>
  <tr>
    <td>John</td>
    <td>30</td>
  </tr>
</table>

<!-- Good -->
<table>
  <caption>User Information</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Age</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">John</th>
      <td>30</td>
    </tr>
  </tbody>
</table>
```

## Real-World Use Cases
1. **Government websites**: Must comply with Section 508
2. **Educational platforms**: Legal requirement in many countries
3. **E-commerce**: Access to wider market
4. **Healthcare**: Critical for patient access
5. **Financial services**: Regulatory compliance
6. **Enterprise applications**: Employee accessibility

## Common Mistakes
1. **Using divs for everything**: Not using semantic HTML
2. **Missing alt text**: Images without alternatives
3. **Low color contrast**: Hard to read text
4. **No keyboard navigation**: Mouse-only interactions
5. **Missing form labels**: Inputs without labels
6. **No focus indicators**: Can't see where focus is
7. **Autoplay media**: No control over playback
8. **Missing skip links**: No way to skip navigation

## Best Practices
1. **Use semantic HTML**: Correct elements for content
2. **Provide text alternatives**: Alt text, captions, transcripts
3. **Ensure keyboard accessibility**: All functionality via keyboard
4. **Maintain color contrast**: Minimum 4.5:1 for normal text
5. **Use ARIA correctly**: Only when native HTML insufficient
6. **Test with assistive technology**: Screen readers, keyboard only
7. **Follow WCAG guidelines**: Level AA minimum
8. **Include accessibility in design**: Not an afterthought

## Performance Considerations
- **Semantic HTML**: Better performance than div soup
- **Lazy loading images**: With proper alt text
- **ARIA attributes**: Minimal impact on performance
- **Skip links**: No performance impact
- **Focus management**: Important for SPA performance

## Interview Questions

### Beginner (5-10)
1. **What is WCAG?**
   - Web Content Accessibility Guidelines, W3C standard for accessible web content.

2. **What are the four principles of WCAG?**
   - Perceivable, Operable, Understandable, Robust (POUR).

3. **What is the difference between Level A, AA, and AAA?**
   - A is minimum, AA is standard, AAA is enhanced accessibility.

4. **What is alt text?**
   - Alternative text for images, describes image content for screen readers.

5. **Why is color contrast important?**
   - Ensures text is readable for people with low vision or color blindness.

6. **What is semantic HTML?**
   - Using HTML elements for their intended purpose (nav, header, main).

7. **What is a landmark role?**
   - ARIA roles that define page regions (banner, navigation, main).

8. **What is keyboard accessibility?**
   - Ability to use all functionality via keyboard without mouse.

### Intermediate (5-10)
9. **How do you make forms accessible?**
   - Labels, fieldsets, legends, error messages, aria-required.

10. **What is ARIA and when to use it?**
    - Accessible Rich Internet Applications, use when native HTML insufficient.

11. **How do you handle dynamic content?**
    - Use aria-live regions to announce changes to screen readers.

12. **What is the difference between `role="alert"` and `aria-live="assertive"`?**
    - Both interrupt user, but role="alert" has implicit aria-live.

13. **How do you test accessibility?**
    - Automated tools (axe, Lighthouse), manual testing, screen readers.

14. **What are skip links?**
    - Links that allow keyboard users to skip repetitive content.

15. **How do you handle focus in SPAs?**
    - Manage focus on route changes, use aria-live for announcements.

16. **What is `prefers-reduced-motion`?**
    - CSS media query for users who prefer reduced motion.

### Senior (10-15)
17. **How do you implement accessibility in a design system?**
    - Component guidelines, documentation, testing, automation.

18. **What is the impact of accessibility on SEO?**
    - Semantic HTML, alt text, headings improve search rankings.

19. **How do you handle accessibility in complex components?**
    - Proper ARIA attributes, keyboard navigation, focus management.

20. **What is the difference between WCAG 2.0 and 2.1?**
    - 2.1 adds requirements for mobile, cognitive, low vision disabilities.

21. **How do you make video content accessible?**
    - Captions, audio descriptions, transcripts, player controls.

22. **What is cognitive accessibility?**
    - Making content understandable for people with cognitive disabilities.

23. **How do you handle accessibility in micro-frontends?**
    - Consistent patterns, shared components, testing across boundaries.

24. **What is the role of accessibility in design thinking?**
    - Include accessibility from ideation, not as afterthought.

### FAANG-style (5-10)
25. **Design an accessibility testing strategy for a large application.**
    - Automated testing, manual audits, user testing, training, monitoring.

26. **How would you make a complex data visualization accessible?**
    - Text alternatives, keyboard navigation, screen reader support.

27. **What are the business benefits of accessibility?**
    - Legal compliance, wider market, better UX, SEO, brand reputation.

28. **How do you prioritize accessibility issues?**
    - Impact on users, legal risk, effort to fix, frequency.

29. **Design an accessible component library.**
    - Documentation, examples, testing, automation, guidelines.

### Follow-ups (5-10)
30. **How does accessibility affect conversion rates?**
    - Studies show accessible sites have higher conversion rates.

31. **What is the relationship between accessibility and inclusive design?**
    - Accessibility is outcome, inclusive design is process.

32. **How do you handle accessibility in internationalization?**
    - RTL support, language attributes, cultural considerations.

33. **What is the future of accessibility?**
    - AI assistance, better tools, legal requirements, user awareness.

34. **How do you measure accessibility success?**
    - WCAG compliance, user testing, automated scores, bug reports.

## Summary
WCAG provides guidelines for making web content accessible. Follow POUR principles, aim for Level AA compliance, use semantic HTML, and test with assistive technology. Accessibility is not just legal compliance but ethical responsibility and good business.

## References & Learn More
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [W3C WAI](https://www.w3.org/WAI/)
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)