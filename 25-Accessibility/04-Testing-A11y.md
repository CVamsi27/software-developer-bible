# Testing Accessibility

## Definition
Accessibility testing is the practice of verifying that web content is usable by people with disabilities. It involves automated tools, manual testing, and assistive technology testing to ensure compliance with WCAG guidelines.

## Why Do We Need It?
- **Legal compliance**: Many jurisdictions require accessibility
- **Quality assurance**: Ensure all users can access content
- **User trust**: Demonstrate commitment to inclusion
- **Market reach**: Access to wider audience
- **Continuous improvement**: Catch issues early

## How It Works
Accessibility testing combines multiple approaches:

### Testing Strategy
```
┌─────────────────────────────────────────────────────────────────┐
│                    Accessibility Testing Strategy                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Automated Testing         Manual Testing        User Testing   │
│  ┌─────────────┐          ┌─────────────┐       ┌─────────────┐ │
│  │  axe-core   │          │  Keyboard   │       │  Disabled   │ │
│  │  Lighthouse │          │  Screen     │       │  Users      │ │
│  │  WAVE       │          │  Reader     │       │  Feedback   │ │
│  └─────────────┘          └─────────────┘       └─────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### axe-core Integration
```javascript
// Install axe-core
// npm install axe-core

// Browser extension
// Chrome: axe DevTools
// Firefox: axe DevTools

// Programmatic testing
const axe = require('axe-core');

// Test entire page
axe.run().then(results => {
  console.log('Violations:', results.violations);
  console.log('Passes:', results.passes);
  console.log('Incomplete:', results.incomplete);
});

// Test specific element
const element = document.querySelector('#my-component');
axe.run(element).then(results => {
  // Handle results
});

// React Testing Library integration
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('accessibility', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Lighthouse Testing
```bash
# Install Lighthouse
npm install -g lighthouse

# Run accessibility audit
lighthouse https://example.com --only-categories=accessibility --output=json

# Chrome DevTools
# Open DevTools > Lighthouse > Accessibility

# Programmatic testing
const lighthouse = require('lighthouse');

async function runLighthouse(url) {
  const result = await lighthouse(url, {
    onlyCategories: ['accessibility'],
    output: 'json'
  });
  
  const score = result.report.categories.accessibility.score * 100;
  console.log(`Accessibility score: ${score}`);
}
```

### WAVE Testing
```bash
# WAVE API
curl "https://wave.webaim.org/api/request?key=YOUR_KEY&url=https://example.com"

# Browser extension
# Install WAVE Evaluation Tool

# Command line
npm install -g wave-cli
wave https://example.com
```

### Screen Reader Testing
```bash
# NVDA (Windows - free)
# Download from https://www.nvaccess.org/download/

# JAWS (Windows - commercial)
# Download from https://www.freedomscientific.com/products/software/jaws/

# VoiceOver (macOS - built-in)
# Enable: System Preferences > Accessibility > VoiceOver

# TalkBack (Android - built-in)
# Enable: Settings > Accessibility > TalkBack

# VoiceOver (iOS - built-in)
# Enable: Settings > Accessibility > VoiceOver
```

### Keyboard Testing Script
```javascript
// Automated keyboard testing
async function testKeyboardNavigation() {
  // Get all focusable elements
  const focusable = document.querySelectorAll(
    'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  // Test tab order
  for (const element of focusable) {
    element.focus();
    
    // Check if element is focused
    if (document.activeElement !== element) {
      console.error('Focus not moving correctly:', element);
    }
    
    // Check for visible focus indicator
    const styles = window.getComputedStyle(element);
    if (styles.outline === 'none' && styles.boxShadow === 'none') {
      console.warn('Missing focus indicator:', element);
    }
  }
}

// Test keyboard interactions
async function testKeyboardInteractions() {
  const buttons = document.querySelectorAll('button');
  
  for (const button of buttons) {
    // Test Enter key
    button.focus();
    const enterEvent = new KeyboardEvent('keydown', { key: 'Enter' });
    button.dispatchEvent(enterEvent);
    
    // Test Space key
    const spaceEvent = new KeyboardEvent('keydown', { key: ' ' });
    button.dispatchEvent(spaceEvent);
  }
}
```

### Automated Testing with Jest
```javascript
// jest.config.js
module.exports = {
  setupFilesAfterSetup: ['@testing-library/jest-dom'],
  testEnvironment: 'jsdom'
};

// accessibility.test.js
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  test('form has no accessibility violations', async () => {
    const { container } = render(
      <form>
        <label htmlFor="email">Email</label>
        <input type="email" id="email" required />
        <button type="submit">Submit</button>
      </form>
    );
    
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  test('navigation has no accessibility violations', async () => {
    const { container } = render(
      <nav aria-label="Main">
        <a href="/">Home</a>
        <a href="/about">About</a>
      </nav>
    );
    
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Cypress Accessibility Testing
```javascript
// cypress/e2e/accessibility.cy.js
describe('Accessibility', () => {
  it('has no axe violations', () => {
    cy.visit('/');
    cy.injectAxe();
    cy.checkA11y();
  });
  
  it('has no axe violations on form page', () => {
    cy.visit('/form');
    cy.injectAxe();
    cy.checkA11y('#form-container');
  });
  
  it('tests keyboard navigation', () => {
    cy.visit('/');
    
    // Tab through elements
    cy.get('body').tab();
    cy.focused().should('have.attr', 'href', '#main-content');
    
    cy.focused().tab();
    cy.focused().should('have.attr', 'href', '/');
  });
});
```

### Manual Testing Checklist
```markdown
## Manual Testing Checklist

### Visual
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text)
- [ ] Content is readable at 200% zoom
- [ ] Focus indicators are visible
- [ ] No information conveyed by color alone
- [ ] Text can be resized to 200% without loss

### Keyboard
- [ ] All functionality available via keyboard
- [ ] Logical tab order
- [ ] Skip link present and functional
- [ ] Focus trap in modals
- [ ] No keyboard traps
- [ ] Arrow keys work in composite widgets

### Screen Reader
- [ ] Images have descriptive alt text
- [ ] Forms have labels
- [ ] Headings are hierarchical
- [ ] Landmarks are present
- [ ] Dynamic content announced
- [ ] Tables have headers

### Content
- [ ] Language attribute present
- [ ] Page titles are descriptive
- [ ] Links have descriptive text
- [ ] Error messages are clear
- [ ] Instructions don't rely solely on sensory characteristics
```

### Testing with Real Users
```markdown
## User Testing Protocol

### Participants
- Screen reader users (NVDA, JAWS, VoiceOver)
- Keyboard-only users
- Users with low vision
- Users with cognitive disabilities

### Tasks
1. Complete a purchase
2. Fill out a form
3. Navigate to specific page
4. Use search functionality
5. Play media content

### Metrics
- Task completion rate
- Time on task
- Error rate
- Satisfaction score
- Accessibility issues found
```

## Real-World Use Cases
1. **CI/CD integration**: Automated testing in build pipeline
2. **Regression testing**: Catch new accessibility issues
3. **User acceptance testing**: Real user feedback
4. **Compliance auditing**: Legal requirements
5. **Component library testing**: Ensure accessible components
6. **Cross-browser testing**: Different assistive technologies

## Common Mistakes
1. **Relying only on automated tools**: Can't catch all issues
2. **Not testing with real users**: Missing real-world problems
3. **Ignoring manual testing**: Automated tools have limitations
4. **Not testing early**: Fixing issues late is expensive
5. **Ignoring mobile accessibility**: Different challenges
6. **Not documenting issues**: Hard to track and fix
7. **Skipping regular testing**: Issues can reappear

## Best Practices
1. **Test early and often**: Integrate into development workflow
2. **Combine automated and manual testing**: Catch different issues
3. **Test with real assistive technology**: Not just tools
4. **Include accessibility in code reviews**: Catch issues early
5. **Document testing procedures**: Consistency
6. **Train team on testing**: Everyone responsible
7. **Track metrics**: Measure improvement
8. **Get user feedback**: Real-world validation

## Performance Considerations
- **Automated testing**: Fast, can run in CI/CD
- **Manual testing**: Time-consuming but thorough
- **User testing**: Most valuable but resource-intensive
- **Screen reader testing**: Requires setup and expertise
- **Regression testing**: Important for maintenance

## Interview Questions

### Beginner (5-10)
1. **What is accessibility testing?**
   - Verifying web content is usable by people with disabilities.

2. **What is axe-core?**
   - Automated accessibility testing engine for web applications.

3. **What is Lighthouse?**
   - Google's tool for auditing web page quality, including accessibility.

4. **Why is manual testing important?**
   - Automated tools can't catch all accessibility issues.

5. **What is a screen reader?**
   - Assistive technology that reads screen content aloud.

6. **What is WAVE?**
   - Web Accessibility Evaluation Tool for identifying accessibility issues.

7. **What is the difference between automated and manual testing?**
   - Automated finds technical issues, manual finds user experience issues.

8. **Why should you test with real users?**
   - Real users provide valuable feedback on actual usability.

### Intermediate (5-10)
9. **How do you integrate accessibility testing into CI/CD?**
   - Use axe-core, Lighthouse, or pa11y in build pipeline.

10. **What are the limitations of automated testing?**
    - Can't catch keyboard navigation, color contrast context, usability issues.

11. **How do you test color contrast?**
    - Use tools like axe, Colour Contrast Analyser, browser extensions.

12. **What is the difference between WCAG A, AA, and AAA testing?**
    - A is minimum, AA is standard, AAA is enhanced requirements.

13. **How do you test keyboard navigation?**
    - Tab through all elements, test arrow keys, check focus indicators.

14. **What is the role of screen readers in testing?**
    - Test that content is properly announced and navigable.

15. **How do you test dynamic content?**
    - Verify live regions announce changes, focus management works.

16. **What is regression testing for accessibility?**
    - Ensuring new code doesn't introduce accessibility issues.

### Senior (10-15)
17. **How do you design an accessibility testing strategy?**
    - Automated, manual, user testing, training, documentation.

18. **What are the metrics for accessibility testing?**
    - WCAG compliance, violation count, user satisfaction, task completion.

19. **How do you handle accessibility testing in micro-frontends?**
    - Test at component and integration levels, shared testing utilities.

20. **What is the cost of not testing accessibility?**
    - Legal risks, lost users, brand damage, remediation costs.

21. **How do you test accessibility in complex components?**
    - Manual testing, ARIA validation, keyboard testing, screen reader testing.

22. **What is the role of accessibility in code reviews?**
    - Review for semantic HTML, ARIA usage, keyboard support.

23. **How do you test accessibility across browsers?**
    - Test with different screen readers, browser combinations.

24. **What is the impact of testing on development velocity?**
    - Initial slowdown, but reduces bugs and rework.

### FAANG-style (5-10)
25. **Design an accessibility testing system for a large application.**
    - Automated testing, manual audits, user testing, training, monitoring.

26. **How would you implement accessibility testing at scale?**
    - Centralized testing, shared utilities, automated reporting, metrics.

27. **What are the trade-offs between different testing approaches?**
    - Speed vs thoroughness, cost vs value, automation vs manual.

28. **How do you prioritize accessibility issues?**
    - User impact, legal risk, effort to fix, frequency.

29. **Design an accessibility testing dashboard.**
    - Metrics, trends, violations, user feedback, compliance status.

### Follow-ups (5-10)
30. **How does accessibility testing affect release cycles?**
    - Adds testing time, but reduces post-release issues.

31. **What is the future of accessibility testing?**
    - AI-powered testing, better automation, real-time feedback.

32. **How do you train QA teams on accessibility testing?**
    - Workshops, documentation, hands-on practice, certifications.

33. **What is the role of accessibility in agile development?**
    - Include in sprint planning, acceptance criteria, Definition of Done.

34. **How do you measure accessibility success?**
    - WCAG compliance, user testing results, bug reports, metrics.

## Summary
Accessibility testing combines automated tools, manual testing, and real user feedback. Use axe-core and Lighthouse for automated testing, test keyboard navigation manually, and validate with screen readers. Include accessibility in your development workflow and test early and often.

## References & Learn More
- [axe-core](https://github.com/dequelabs/axe-core)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [WAVE](https://wave.webaim.org/)
- [WebAIM](https://webaim.org/)
- [A11Y Project](https://www.a11yproject.com/)
- [Deque University](https://dequeuniversity.com/)