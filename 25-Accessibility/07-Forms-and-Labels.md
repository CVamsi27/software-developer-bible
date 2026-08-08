---
section: Accessibility
category: Quality
tags: [concept, reference, guide]
---

# Forms & Labels

## Definition

**Accessible forms** ensure that every user — including those using screen readers, voice control, switch devices, or keyboards — can understand, navigate, complete, and submit forms correctly. This requires proper labels, error handling, focus management, field grouping, and avoiding patterns that exclude assistive technology users.

Forms are where accessibility failures hurt users most directly. A user who can't fill out a checkout form loses money. A job applicant who can't submit an application is excluded. The WCAG success criteria for forms (1.3.1, 3.3.1, 3.3.2, 3.3.3, 4.1.2) are among the most frequently violated in production.

## Why Do We Need It?

1. **Legal compliance**: WCAG 3.3 (Input Assistance) and 4.1.2 (Name, Role, Value) are required at AA
2. **Form completion rate**: accessible forms convert 10-30% better (case studies from GOV.UK, others)
3. **Screen reader users**: rely entirely on proper labels to know what each field is
4. **Voice control users**: need visible labels and unique accessible names
5. **Cognitive accessibility**: clear instructions, error recovery, predictable layout

## WCAG Success Criteria for Forms

| SC | Title | What It Requires |
|----|-------|------------------|
| 1.3.1 | Info and Relationships | Labels associated with inputs |
| 3.3.1 | Error Identification | Errors described in text |
| 3.3.2 | Labels or Instructions | Visible labels for inputs |
| 3.3.3 | Error Suggestion | Suggestion for fixing the error |
| 3.3.4 | Error Prevention (Legal, Financial) | Confirm/reverse for critical actions |
| 4.1.2 | Name, Role, Value | Programmatic name for every input |

## How It Works

### The Label-Input Relationship

```text
┌──────────────────────────────────────────────────────────────┐
│                  Label-Input Associations                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Method 1: <label for="x"> wraps the input                   │
│            <input id="x">                                    │
│  ✓ Best for explicit association                              │
│  ✓ Clickable label area                                      │
│                                                              │
│  Method 2: <label> wraps the input                           │
│            <label>Email <input type="email"></label>         │
│  ✓ Compact, implicit association                              │
│  ✓ Clickable label area                                      │
│                                                              │
│  Method 3: aria-labelledby="heading-id"                      │
│            <h2 id="heading-id">Email</h2>                    │
│            <input aria-labelledby="heading-id">              │
│  ✓ When no visible label exists                               │
│  ✗ NOT a substitute for visible label                        │
│                                                              │
│  Method 4: aria-label="Email address"                        │
│            <input aria-label="Email address">                │
│  ✓ When no visible label exists                               │
│  ✗ NOT a substitute for visible label                        │
│                                                              │
│  ❌ NEVER: placeholder as label                               │
│  Placeholder disappears on input, low contrast,              │
│  not announced by all screen readers                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Form Validation Flow

```text
┌──────────────────────────────────────────────────────────────┐
│                Accessible Validation Flow                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User submits form                                        │
│       │                                                      │
│       ▼                                                      │
│  2. JavaScript validates each field                          │
│       │                                                      │
│       ▼                                                      │
│  3. For each error:                                          │
│     • Set aria-invalid="true"                                │
│     • Set role="alert" on the error message                  │
│     • Focus the FIRST invalid field                          │
│     • Show error in DOM (not just on focus loss)             │
│       │                                                      │
│       ▼                                                      │
│  4. Live region announces "X errors found"                   │
│                                                              │
│  5. User fixes errors, error indicators update in real-time   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Accessible Form

```html
<form novalidate>
  <div class="field">
    <label for="email">Email address</label>
    <input
      id="email"
      type="email"
      required
      autocomplete="email"
      aria-describedby="email-hint email-error"
      aria-invalid="false"
    />
    <p id="email-hint" class="hint">
      We'll never share your email with anyone else.
    </p>
    <p id="email-error" class="error" role="alert" hidden>
      Please enter a valid email address.
    </p>
  </div>

  <button type="submit">Sign up</button>
</form>
```

### React Component with Accessible Validation

```typescript
import { useId, useState, useRef } from 'react';

interface FieldProps {
  label: string;
  hint?: string;
  error?: string;
  required?: boolean;
  type?: string;
  value: string;
  onChange: (v: string) => void;
}

function Field({ label, hint, error, required, type = 'text', value, onChange }: FieldProps) {
  const id = useId();
  const hintId = `${id}-hint`;
  const errorId = `${id}-error`;
  const describedBy = [hint && hintId, error && errorId].filter(Boolean).join(' ');

  return (
    <div className="field">
      <label htmlFor={id}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only"> (required)</span>}
      </label>
      {hint && <p id={hintId} className="hint">{hint}</p>}
      <input
        id={id}
        type={type}
        value={value}
        required={required}
        aria-required={required}
        aria-invalid={!!error}
        aria-describedby={describedBy || undefined}
        onChange={(e) => onChange(e.target.value)}
      />
      {error && (
        <p id={errorId} className="error" role="alert">
          <span aria-hidden="true">⚠</span> {error}
        </p>
      )}
    </div>
  );
}
```

### Fieldset and Legend (for Radio/Checkbox Groups)

```html
<fieldset>
  <legend>Shipping method</legend>
  <label>
    <input type="radio" name="shipping" value="standard" />
    Standard (5-7 days)
  </label>
  <label>
    <input type="radio" name="shipping" value="express" />
    Express (2-3 days)
  </label>
  <label>
    <input type="radio" name="shipping" value="overnight" />
    Overnight (next day)
  </label>
</fieldset>

<fieldset>
  <legend>Notification preferences</legend>
  <label>
    <input type="checkbox" name="notify" value="email" />
    Email
  </label>
  <label>
    <input type="checkbox" name="notify" value="sms" />
    SMS
  </label>
</fieldset>
```

### Error Summary (Top of Form)

```html
<div
  id="error-summary"
  class="error-summary"
  role="alert"
  aria-live="assertive"
  tabindex="-1"
  hidden
>
  <h2>There are 2 errors in this form</h2>
  <ul>
    <li><a href="#email">Email address is required</a></li>
    <li><a href="#password">Password must be at least 8 characters</a></li>
  </ul>
</div>

<script>
  // On form submit with errors:
  errorSummary.hidden = false;
  errorSummary.focus();  // Move focus to the summary
  // First invalid field also gets focused after summary is read
</script>
```

### Required Field Indicators (Multiple Approaches)

```html
<!-- Approach 1: Asterisk with hidden context -->
<label for="email">Email <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>

<!-- Approach 2: Text "required" -->
<label for="email">Email <span>(required)</span></label>

<!-- Approach 3: Visual + aria-required -->
<label for="email">Email *</label>
<input id="email" required aria-required="true" />

<!-- ❌ Bad: only visual asterisk, no programmatic indication -->
<label for="email">Email *</label>
<input id="email" />
```

### Autocomplete Attributes (Critical for Cognitive Accessibility)

```html
<input type="text" name="name" autocomplete="name" />
<input type="email" name="email" autocomplete="email" />
<input type="tel" name="phone" autocomplete="tel" />
<input type="text" name="address" autocomplete="street-address" />
<input type="text" name="city" autocomplete="address-level2" />
<input type="text" name="zip" autocomplete="postal-code" />
<input type="text" name="country" autocomplete="country" />

<!-- Credit card -->
<input type="text" name="cc-number" autocomplete="cc-number" />
<input type="text" name="cc-exp" autocomplete="cc-exp" />
<input type="text" name="cc-csc" autocomplete="cc-csc" />
```

Autocomplete attributes:
- Let browsers autofill correctly
- Help password managers
- Required for WCAG 1.3.5 (Identify Input Purpose, AA)

## Real-World Use Cases

### 1. Multi-Step Form (Wizard)

```typescript
function MultiStepForm() {
  const [step, setStep] = useState(1);
  const totalSteps = 3;

  return (
    <form aria-labelledby="form-title">
      <h1 id="form-title">Create your account</h1>

      {/* Step indicator — must be perceivable */}
      <nav aria-label="Form progress">
        <ol>
          <li aria-current={step === 1 ? 'step' : undefined}>
            Step 1: Account {step > 1 && '✓'}
          </li>
          <li aria-current={step === 2 ? 'step' : undefined}>
            Step 2: Profile
          </li>
          <li aria-current={step === 3 ? 'step' : undefined}>
            Step 3: Confirm
          </li>
        </ol>
      </nav>

      {/* Focus management on step change */}
      <div role="group" aria-labelledby={`step-${step}-title`}>
        <h2 id={`step-${step}-title`}>Step {step}: ...</h2>
        {/* ... */}
      </div>
    </form>
  );
}
```

### 2. Search Form

```html
<!-- ❌ Bad: placeholder as label, no submit button text -->
<form>
  <input type="text" placeholder="Search..." />
  <button>🔍</button>
</form>

<!-- ✅ Good: visible label (visually hidden), accessible button text -->
<form role="search">
  <label for="search" class="sr-only">Search products</label>
  <input id="search" type="search" name="q" placeholder="Search..." />
  <button type="submit">
    <span aria-hidden="true">🔍</span>
    <span class="sr-only">Search</span>
  </button>
</form>
```

### 3. File Upload

```html
<label for="avatar">Profile picture</label>
<input
  id="avatar"
  type="file"
  accept="image/png, image/jpeg"
  aria-describedby="avatar-hint"
/>
<p id="avatar-hint">PNG or JPG, max 5MB</p>
```

## Common Mistakes

### 1. Using Placeholder as a Label

```html
<!-- ❌ Bad: placeholder is not a label -->
<input placeholder="Email" />

<!-- ✅ Good: real label -->
<label for="email">Email</label>
<input id="email" type="email" placeholder="you@example.com" />
```

### 2. No Error Description

```html
<!-- ❌ Bad: error only visual, not announced -->
<input style="border: 2px solid red" />
<span style="color: red">*</span>

<!-- ✅ Good: error associated with input, announced by SR -->
<input aria-invalid="true" aria-describedby="err-1" />
<p id="err-1" role="alert">Email is required</p>
```

### 3. Auto-Submit on Change

```text
❌ Bad: <select> that submits on change, disorienting
✅ Good: explicit "Apply" or "Submit" button
```

Auto-submit on change is disorienting for screen reader users who can't predict when the form will submit.

### 4. Required Fields Without Programmatic Indication

```html
<!-- ❌ Bad: only visual asterisk -->
<label>Email *</label>
<input />

<!-- ✅ Good: aria-required + visual + SR-only context -->
<label>Email <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input required aria-required="true" />
```

### 5. Disabling Submit on Invalid

```text
❌ Bad: <button disabled> until form is valid (user can't tell why)
✅ Good: button always enabled, validation on submit with clear errors
```

A disabled button hides the reason for invalidity. Keep the button enabled and show errors.

## Best Practices

1. **Always use `<label for="id">`** with explicit association
2. **Use `aria-describedby`** for hints and error messages
3. **Use `aria-invalid="true"`** for invalid fields
4. **Use `role="alert"`** for error messages that need immediate announcement
5. **Use `<fieldset>` and `<legend>`** for radio/checkbox groups
6. **Include an error summary** at the top of the form for screen reader users
7. **Use `autocomplete` attributes** for common fields (WCAG 1.3.5)
8. **Don't disable the submit button** — show errors instead
9. **Move focus to the first error** after submit (or to error summary)
10. **Test with screen reader** (NVDA, VoiceOver) — automated tools catch ~30% of issues

## Performance Considerations

- No significant performance impact from accessible forms
- `aria-live` regions may cause screen reader to interrupt current speech
- `autocomplete` may slightly speed form completion (browser autofill)

## Summary

- Use `<label for="id">` for every input — never placeholder alone
- Use `aria-describedby` to link hints and error messages
- Use `aria-invalid="true"` and `role="alert"` for error announcements
- Use `<fieldset>` and `<legend>` for grouped controls
- Use `autocomplete` attributes for known input types (WCAG 1.3.5)
- Don't disable the submit button — show errors instead
- Include an error summary and move focus to it on submit

---

## Cheat Sheet
```text
FORMS & LABELS CHEAT SHEET
============================================================

LABEL EVERY INPUT:
  <label for="email">Email</label>
  <input id="email" type="email" />

NEVER: placeholder as label

ASSOCIATE HINTS & ERRORS:
  <input
    aria-describedby="email-hint email-error"
    aria-invalid="true"
  />
  <p id="email-hint">Format: name@domain.com</p>
  <p id="email-error" role="alert">Required</p>

GROUP CONTROLS:
  <fieldset>
    <legend>Shipping method</legend>
    <label><input type="radio" name="ship" /> Standard</label>
    <label><input type="radio" name="ship" /> Express</label>
  </fieldset>

REQUIRED FIELDS:
  <label>Email <span aria-hidden="true">*</span>
    <span class="sr-only">(required)</span>
  </label>
  <input required aria-required="true" />

AUTOCOMPLETE (WCAG 1.3.5):
  autocomplete="email"
  autocomplete="name"
  autocomplete="tel"
  autocomplete="cc-number"

ON SUBMIT ERROR:
  1. Show error summary at top
  2. Focus the summary (tabindex=-1)
  3. Mark first invalid field with aria-invalid
  4. role="alert" on each error message

INTERVIEW TIPS:
  • Always mention <label for="id"> pattern
  • Discuss aria-describedby vs aria-labelledby
  • Explain why disabled submit buttons are bad
  • Mention autocomplete for WCAG 1.3.5
```
---

## See Also
- [ARIA](02-ARIA.md)
- [Color & Contrast](06-Color-and-Contrast.md)
- [Keyboard Navigation](03-Keyboard-Navigation.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [Testing](../16-Testing/)
- [Testing Accessibility](04-Testing-A11y.md)
- [WCAG Overview](01-WCAG-Overview.md)

## References & Learn More

- [WCAG 2.1 SC 3.3 (Input Assistance)](https://www.w3.org/WAI/WCAG21/Understanding/input-assistance.html)
- [WCAG 2.1 SC 1.3.5 (Identify Input Purpose)](https://www.w3.org/WAI/WCAG21/Understanding/identify-input-purpose.html)
- [GOV.UK Design System - Forms](https://design-system.service.gov.uk/components/text-input/)
- [MDN: HTML Forms Accessibility](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#accessibility_concerns)
- [WebAIM: Creating Accessible Forms](https://webaim.org/techniques/forms/)
- [A11y Project - Forms](https://www.a11yproject.com/posts/accessible-forms/)
