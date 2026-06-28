# Keyboard Navigation

## Definition
Keyboard navigation is the ability to access and interact with all website functionality using only a keyboard, without requiring a mouse. It's essential for users with motor disabilities, power users, and screen reader users.

## Why Do We Need It?
- **Motor disabilities**: Users who cannot use a mouse
- **Power users**: Many prefer keyboard for efficiency
- **Screen reader users**: Primarily keyboard-based navigation
- **Legal requirements**: Part of WCAG guidelines
- **Better UX**: Benefits all users

## How It Works
Keyboard navigation involves:
- **Focus management**: Moving between interactive elements
- **Tab order**: Sequential navigation through elements
- **Keyboard shortcuts**: Direct access to functionality
- **Focus indicators**: Visual feedback for focus position

### Keyboard Navigation Flow
```text
┌─────────────────────────────────────────────────────────────────┐
│                    Keyboard Navigation Flow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Tab/Shift+Tab         Arrow Keys           Enter/Space         │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │  Navigate   │ ───▶ │  Navigate   │ ───▶ │  Activate   │     │
│  │  between    │      │  within     │      │  element    │     │
│  │  elements   │      │  composite  │      │             │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Focus Indicators
```css
/* Default focus styles - don't remove! */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Custom focus styles */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(0, 95, 204, 0.25);
}

/* Remove focus for mouse users, keep for keyboard */
:focus:not(:focus-visible) {
  outline: none;
}

/* High contrast focus */
@media (prefers-contrast: high) {
  :focus-visible {
    outline: 3px solid #000;
    outline-offset: 2px;
  }
}
```

### Skip Links
```html
<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #005fcc;
  color: white;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>

<!-- Usage -->
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header>
    <nav><!-- Navigation --></nav>
  </header>
  <main id="main-content" tabindex="-1">
    <!-- Main content -->
  </main>
</body>
```

### Tab Order
```html
<!-- Good: Logical tab order -->
<form>
  <label for="name">Name</label>
  <input type="text" id="name" tabindex="0">

  <label for="email">Email</label>
  <input type="email" id="email" tabindex="0">

  <button type="submit" tabindex="0">Submit</button>
</form>

<!-- Bad: Custom tabindex breaks natural order -->
<div tabindex="1">First</div>
<div tabindex="2">Second</div>
<div tabindex="3">Third</div>

<!-- Good: Use tabindex="0" for focusable elements -->
<button tabindex="0">Click me</button>

<!-- Good: tabindex="-1" for programmatically focusable -->
<div tabindex="-1" id="target">Focusable via script</div>
```

### Roving Tabindex
```html
<!-- Tab list with roving tabindex -->
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
  <button
    role="tab"
    id="tab3"
    aria-selected="false"
    aria-controls="panel3"
    tabindex="-1">
    Tab 3
  </button>
</div>

<script>
// Arrow key navigation
const tablist = document.querySelector('[role="tablist"]');
const tabs = tablist.querySelectorAll('[role="tab"]');

tablist.addEventListener('keydown', (e) => {
  const currentIndex = Array.from(tabs).indexOf(document.activeElement);
  let newIndex;

  switch (e.key) {
    case 'ArrowRight':
      newIndex = (currentIndex + 1) % tabs.length;
      break;
    case 'ArrowLeft':
      newIndex = (currentIndex - 1 + tabs.length) % tabs.length;
      break;
    case 'Home':
      newIndex = 0;
      break;
    case 'End':
      newIndex = tabs.length - 1;
      break;
    default:
      return;
  }

  // Update tabindex
  tabs[currentIndex].setAttribute('tabindex', '-1');
  tabs[newIndex].setAttribute('tabindex', '0');
  tabs[newIndex].focus();
  tabs[newIndex].click();
});
</script>
```

### Keyboard Shortcuts
```html
<!-- Keyboard shortcut handler -->
<div
  role="button"
  tabindex="0"
  aria-keyshortcuts="Ctrl+S"
  onclick="save()">
  Save
</div>

<script>
// Global keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Ctrl+S to save
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault();
    save();
  }

  // Escape to close modal
  if (e.key === 'Escape') {
    closeModal();
  }

  // / to focus search
  if (e.key === '/' && !isInputFocused()) {
    e.preventDefault();
    document.querySelector('#search').focus();
  }
});
</script>
```

### Focus Trapping (Modals)
```html
<!-- Modal with focus trap -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  id="modal">
  <h2 id="dialog-title">Dialog Title</h2>

  <button autofocus id="close-btn">Close</button>
  <input type="text" placeholder="Input">
  <button>Cancel</button>
  <button>Confirm</button>
</div>

<script>
function trapFocus(modal) {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );

  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  modal.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        lastElement.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastElement) {
        firstElement.focus();
        e.preventDefault();
      }
    }
  });
}

// Open modal
function openModal() {
  const modal = document.getElementById('modal');
  modal.hidden = false;
  trapFocus(modal);
  document.getElementById('close-btn').focus();
}

// Close modal
function closeModal() {
  const modal = document.getElementById('modal');
  modal.hidden = true;
  // Return focus to trigger element
  document.getElementById('trigger-btn').focus();
}
</script>
```

### Arrow Key Navigation
```html
<!-- Listbox with arrow key navigation -->
<div
  role="listbox"
  aria-label="Choose an option"
  tabindex="0"
  id="listbox">
  <div role="option" id="opt1" aria-selected="false">Option 1</div>
  <div role="option" id="opt2" aria-selected="false">Option 2</div>
  <div role="option" id="opt3" aria-selected="false">Option 3</div>
</div>

<script>
const listbox = document.getElementById('listbox');
const options = listbox.querySelectorAll('[role="option"]');
let currentIndex = 0;

listbox.addEventListener('keydown', (e) => {
  let newIndex = currentIndex;

  switch (e.key) {
    case 'ArrowDown':
      newIndex = Math.min(currentIndex + 1, options.length - 1);
      break;
    case 'ArrowUp':
      newIndex = Math.max(currentIndex - 1, 0);
      break;
    case 'Home':
      newIndex = 0;
      break;
    case 'End':
      newIndex = options.length - 1;
      break;
    case 'Enter':
    case ' ':
      options[currentIndex].setAttribute('aria-selected', 'true');
      return;
    default:
      return;
  }

  // Update selection
  options[currentIndex].setAttribute('aria-selected', 'false');
  options[newIndex].setAttribute('aria-selected', 'true');
  options[newIndex].scrollIntoView({ block: 'nearest' });
  listbox.setAttribute('aria-activedescendant', options[newIndex].id);
  currentIndex = newIndex;
});
</script>
```

### Menu Navigation
```html
<!-- Dropdown menu -->
<div class="dropdown">
  <button
    aria-haspopup="true"
    aria-expanded="false"
    aria-controls="menu1"
    id="menu-button">
    Options
  </button>

  <div
    role="menu"
    id="menu1"
    aria-labelledby="menu-button"
    hidden>
    <div role="menuitem" tabindex="-1">Edit</div>
    <div role="menuitem" tabindex="-1">Duplicate</div>
    <div role="separator" role="none"></div>
    <div role="menuitem" tabindex="-1">Delete</div>
  </div>
</div>

<script>
const button = document.getElementById('menu-button');
const menu = document.getElementById('menu1');
const items = menu.querySelectorAll('[role="menuitem"]');

button.addEventListener('click', () => {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', !expanded);
  menu.hidden = expanded;

  if (!expanded) {
    items[0].focus();
  }
});

menu.addEventListener('keydown', (e) => {
  const currentIndex = Array.from(items).indexOf(document.activeElement);
  let newIndex;

  switch (e.key) {
    case 'ArrowDown':
      newIndex = (currentIndex + 1) % items.length;
      break;
    case 'ArrowUp':
      newIndex = (currentIndex - 1 + items.length) % items.length;
      break;
    case 'Escape':
      button.focus();
      menu.hidden = true;
      button.setAttribute('aria-expanded', 'false');
      return;
    case 'Home':
      newIndex = 0;
      break;
    case 'End':
      newIndex = items.length - 1;
      break;
    default:
      return;
  }

  items[newIndex].focus();
});
</script>
```

## Real-World Use Cases
1. **Web applications**: Full keyboard support required
2. **E-commerce**: Checkout process, product navigation
3. **Enterprise software**: Data entry, complex workflows
4. **Media players**: Playback controls, playlist navigation
5. **Dashboards**: Data visualization, interactive charts
6. **Mobile web**: Touch and keyboard hybrid

## Common Mistakes
1. **Removing focus indicators**: Makes navigation impossible
2. **Using positive tabindex**: Breaks natural tab order
3. **Missing keyboard handlers**: No arrow key support
4. **Trapping focus**: Modal doesn't release focus
5. **No skip links**: Forces users to tab through navigation
6. **Invisible focus**: Focus not visible to users
7. **Mouse-only interactions**: No keyboard alternative

## Best Practices
1. **Never remove focus indicators**: Style them instead
2. **Use logical tab order**: Follow visual order
3. **Implement skip links**: Allow bypassing repetitive content
4. **Support arrow keys**: For composite widgets
5. **Test with keyboard only**: Unplug mouse
6. **Use tabindex="0"**: For focusable elements
7. **Use tabindex="-1"**: For programmatically focusable
8. **Provide visual feedback**: Focus should be obvious

## Performance Considerations
- **Event listeners**: Minimal impact on performance
- **Focus management**: Important for SPA performance
- **Skip links**: No performance impact
- **Keyboard shortcuts**: Consider performance impact

## Interview Questions

### Beginner (5-10)
1. **What is keyboard navigation?**
   - Ability to use all website functionality with keyboard only.

2. **What is tab order?**
   - Sequence in which elements receive focus when pressing Tab.

3. **What is a skip link?**
   - Link that allows users to skip repetitive navigation.

4. **What is focus indicator?**
   - Visual outline showing which element has focus.

5. **What is `tabindex`?**
   - Attribute defining if element is focusable and tab order.

6. **What is the difference between `tabindex="0"` and `tabindex="-1"`?**
    - 0 adds to tab order, -1 is focusable only programmatically.

7. **Why should you never use positive tabindex?**
    - Breaks natural document flow and confuses users.

8. **What is `:focus-visible`?**
    - CSS pseudo-class for keyboard focus, not mouse click.

### Intermediate (5-10)
9. **How do you trap focus in a modal?**
    - Find focusable elements, cycle through on Tab/Shift+Tab.

10. **What is roving tabindex?**
    - Managing tabindex values to create custom navigation patterns.

11. **How do you implement arrow key navigation?**
    - Listen for keydown events, update focus programmatically.

12. **What is `aria-activedescendant`?**
    - Manages focus in composite widgets without moving DOM focus.

13. **How do you handle keyboard navigation in SPAs?**
    - Manage focus on route changes, restore focus, announce changes.

14. **What is focus restoration?**
    - Returning focus to previous element after closing modal/dialog.

15. **How do you test keyboard navigation?**
    - Unplug mouse, use only keyboard, check all functionality.

16. **What is the difference between `tabindex` and `accesskey`?**
    - tabindex defines tab order, accesskey defines keyboard shortcut.

### Senior (10-15)
17. **How do you implement keyboard navigation for complex widgets?**
    - Follow WAI-ARIA patterns, support arrow keys, manage focus.

18. **What are the challenges of keyboard navigation in SPAs?**
    - Focus management, route changes, dynamic content.

19. **How do you handle keyboard navigation with virtual scrolling?**
    - Manage focus for visible items, handle scroll events.

20. **What is the impact of CSS on keyboard navigation?**
    - Focus indicators, visibility, layout can affect accessibility.

21. **How do you implement keyboard shortcuts?**
    - Global event listeners, prevent default, provide alternatives.

22. **What is `aria-keyshortcuts`?**
    - Defines keyboard shortcuts for elements.

23. **How do you handle keyboard navigation in drag-and-drop?**
    - Provide keyboard alternative, aria-grabbed, aria-dropeffect.

24. **What is the role of focus management in accessibility?**
    - Ensures logical navigation, provides context, maintains usability.

### FAANG-style (5-10)
25. **Design a keyboard navigation system for a complex data grid.**
    - Arrow keys, Tab, Enter, Escape, page navigation, selection.

26. **How would you implement keyboard shortcuts in a web application?**
    - Conflict detection, user customization, documentation, alternatives.

27. **What are the trade-offs between different navigation patterns?**
    - Tab vs arrow, linear vs spatial, global vs local.

28. **How do you test keyboard navigation at scale?**
    - Automated testing, manual audits, user testing, metrics.

29. **Design a keyboard-navigable dashboard.**
    - Logical order, focus management, shortcuts, customization.

### Follow-ups (5-10)
30. **How does keyboard navigation affect SEO?**
    - Minimal direct impact, but better UX improves engagement.

31. **What is the future of keyboard navigation?**
    - Better browser support, new patterns, AI assistance.

32. **How do you handle keyboard navigation with frameworks?**
    - Framework-specific patterns, component libraries, documentation.

33. **What are common keyboard navigation issues in React/Vue?**
    - Missing handlers, wrong tabindex, focus management.

34. **How do you train developers on keyboard navigation?**
    - Workshops, documentation, code reviews, testing exercises.

## Summary
Keyboard navigation is essential for accessibility. Use semantic HTML, proper tabindex, skip links, and support arrow keys for composite widgets. Test with keyboard only and follow established patterns. Remember: if you can't reach it with Tab, it's not accessible.

## References & Learn More
- [WCAG 2.1 - Keyboard Accessible](https://www.w3.org/WAI/WCAG21/Understanding/keyboard)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Keyboard Accessibility](https://webaim.org/techniques/keyboard/)
- [MDN Keyboard Navigation](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Keyboard-navigable_JavaScript_widgets)
- [The A11Y Project](https://www.a11yproject.com/checklist/)