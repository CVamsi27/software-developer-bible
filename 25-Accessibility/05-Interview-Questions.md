# Accessibility Interview Questions

## Comprehensive Interview Guide

This chapter contains 25 carefully curated interview questions covering accessibility concepts, WCAG guidelines, ARIA, testing, and implementation. Questions are organized by difficulty level and include detailed answers.

---

## Beginner (5-10)

### 1. What is web accessibility and why is it important?
**Answer:**
Web accessibility (a11y) ensures websites and applications are usable by people with disabilities. It's important because:
- **Legal compliance**: Many countries require accessibility (ADA, Section 508, EAA)
- **Inclusivity**: 15% of world population has some form of disability
- **Better UX**: Accessible sites work better for everyone
- **SEO benefits**: Many accessibility practices improve SEO
- **Market reach**: Access to wider audience

### 2. What are the four principles of WCAG?
**Answer:**
WCAG is built on four principles (POUR):
1. **Perceivable**: Information must be presentable to users
2. **Operable**: UI components must be operable
3. **Understandable**: Information and UI must be understandable
4. **Robust**: Content must be robust for assistive technologies

### 3. What is the difference between Level A, AA, and AAA?
**Answer:**
- **Level A**: Minimum accessibility requirements
- **Level AA**: Standard accessibility (most common requirement)
- **Level AAA**: Enhanced accessibility (highest level)

Most organizations aim for Level AA compliance.

### 4. What is semantic HTML and why does it matter?
**Answer:**
Semantic HTML uses elements for their intended purpose:
```html
<!-- Bad -->
<div class="header">Title</div>

<!-- Good -->
<header>
  <h1>Title</h1>
</header>
```
It matters because:
- Screen readers understand page structure
- Better SEO
- Easier maintenance
- Accessibility by default

### 5. What is alt text and when should you use it?
**Answer:**
Alt text describes image content for screen readers:
```html
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2">
```
Use it for:
- Informative images
- Images with text
- Charts and graphs
- Complex images

### 6. Why is color contrast important?
**Answer:**
Color contrast ensures text is readable for people with:
- Low vision
- Color blindness
- Aging eyes

WCAG requires:
- 4.5:1 for normal text
- 3:1 for large text

### 7. What are landmark roles?
**Answer:**
Landmark roles define page regions for screen readers:
```html
<header>Site header</header>
<nav aria-label="Main">Navigation</nav>
<main>Main content</main>
<aside>Sidebar</aside>
<footer>Site footer</footer>
```

### 8. What is keyboard accessibility?
**Answer:**
Keyboard accessibility means all functionality is available via keyboard:
- Tab navigation
- Enter/Space to activate
- Arrow keys for composite widgets
- Escape to close modals

---

## Intermediate (5-10)

### 9. What is ARIA and when should you use it?
**Answer:**
ARIA (Accessible Rich Internet Applications) provides additional semantics:
```html
<button aria-expanded="false" aria-controls="menu1">Menu</button>
```
Use when:
- Native HTML semantics are insufficient
- Complex custom widgets
- Dynamic content updates

### 10. What is the difference between `aria-label` and `aria-labelledby`?
**Answer:**
- **aria-label**: Provides text label
- **aria-labelledby**: References visible text

```html
<!-- aria-label -->
<input aria-label="Search">

<!-- aria-labelledby -->
<label id="search-label">Search</label>
<input aria-labelledby="search-label">
```

### 11. What are live regions?
**Answer:**
Live regions announce dynamic content changes:
```html
<div aria-live="polite">Updates announced politely</div>
<div role="alert">Urgent messages</div>
<div role="status">Status updates</div>
```

### 12. How do you make forms accessible?
**Answer:**
- Labels for all inputs
- Fieldsets and legends for groups
- Error messages with aria-describedby
- Required fields with aria-required
- Clear instructions

### 13. What is focus management?
**Answer:**
Focus management controls where keyboard focus goes:
- Trap focus in modals
- Return focus on close
- Manage focus in SPAs
- Skip links for navigation

### 14. What is the difference between `aria-hidden` and `hidden`?
**Answer:**
- **aria-hidden="true"**: Hides from screen readers only
- **hidden**: Hides from all users (screen readers and visual)

### 15. How do you test accessibility?
**Answer:**
Combine multiple approaches:
- **Automated**: axe-core, Lighthouse, WAVE
- **Manual**: Keyboard testing, screen reader testing
- **User testing**: Real users with disabilities

### 16. What is skip navigation?
**Answer:**
Skip navigation allows users to bypass repetitive content:
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

---

## Senior (10-15)

### 17. How do you implement accessibility in a design system?
**Answer:**
- Component guidelines with ARIA patterns
- Documentation with examples
- Automated testing
- Regular audits
- Team training

### 18. What is the impact of accessibility on SEO?
**Answer:**
- Semantic HTML improves crawlability
- Alt text helps image search
- Headings improve content structure
- Better UX reduces bounce rate

### 19. How do you handle accessibility in SPAs?
**Answer:**
- Manage focus on route changes
- Use live regions for dynamic content
- Maintain heading hierarchy
- Test with screen readers

### 20. What are the challenges of accessibility in complex components?
**Answer:**
- Custom widgets need ARIA
- Keyboard navigation patterns
- Focus management
- Dynamic state updates

### 21. How do you make video content accessible?
**Answer:**
- Captions for deaf/hard of hearing
- Audio descriptions for blind users
- Transcripts for all users
- Player controls accessible via keyboard

### 22. What is cognitive accessibility?
**Answer:**
Making content understandable for people with:
- Learning disabilities
- Memory issues
- Attention disorders
- Language barriers

Strategies:
- Clear language
- Consistent layout
- Predictable navigation
- Error prevention

### 23. How do you handle accessibility in internationalization?
**Answer:**
- RTL support
- Language attributes
- Cultural considerations
- Text expansion/contraction

### 24. What is the role of accessibility in inclusive design?
**Answer:**
- Accessibility is the outcome
- Inclusive design is the process
- Design for diverse users from start
- Not an afterthought

### 25. How do you measure accessibility success?
**Answer:**
- WCAG compliance rate
- User testing results
- Bug reports and fixes
- Automated test scores
- User satisfaction surveys

---

## FAANG-style (5-10)

### 26. Design an accessibility testing strategy for a large application.
**Answer:**
Consider:
- Automated testing in CI/CD
- Manual audits quarterly
- User testing with disabled users
- Training for developers
- Metrics and reporting
- Continuous improvement

### 27. How would you make a complex data visualization accessible?
**Answer:**
- Text alternatives for all data
- Keyboard navigation for interactive elements
- Screen reader support
- Color contrast
- Multiple ways to access data

### 28. What are the business benefits of accessibility?
**Answer:**
- Legal compliance
- Wider market reach
- Better SEO
- Improved brand reputation
- Reduced liability
- Higher conversion rates

### 29. How do you prioritize accessibility issues?
**Answer:**
Consider:
- User impact (high/medium/low)
- Legal risk
- Effort to fix
- Frequency of occurrence
- Business value

### 30. Design an accessible component library.
**Answer:**
- Follow WAI-ARIA Authoring Practices
- Document usage patterns
- Include examples
- Automated testing
- Regular audits
- Team training

---

## Follow-ups (5-10)

### 31. How does accessibility affect conversion rates?
**Answer:**
Studies show:
- Accessible sites have 28% higher conversion rates
- 71% of users leave inaccessible sites
- $6.9 billion lost annually due to inaccessibility

### 32. What is the relationship between accessibility and progressive enhancement?
**Answer:**
- Progressive enhancement: Build from base up
- Accessibility: Ensure base is accessible
- Both improve user experience

### 33. How do you handle accessibility with JavaScript frameworks?
**Answer:**
- Use semantic HTML
- Manage focus properly
- Test with screen readers
- Follow framework-specific patterns

### 34. What is the future of accessibility?
**Answer:**
- AI-powered testing and remediation
- Better browser support
- More legal requirements
- Improved tools and standards

### 35. How do you train developers on accessibility?
**Answer:**
- Hands-on workshops
- Real-world exercises
- Documentation and guidelines
- Code reviews with accessibility focus
- Regular updates on standards

## Summary
Accessibility is essential for creating inclusive web experiences. Understanding WCAG principles, semantic HTML, ARIA, testing techniques, and implementation patterns is crucial for modern web development. Remember: accessibility is not just a checklist but a mindset.

## References & Learn More
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM](https://webaim.org/)
- [A11Y Project](https://www.a11yproject.com/)
- [Deque University](https://dequeuniversity.com/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)