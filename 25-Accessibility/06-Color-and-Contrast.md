---
section: Accessibility
category: Quality
tags: [concept, reference, guide]
---

# Color & Contrast

## Definition

**Color and contrast** in accessibility refers to ensuring that visual information is perceivable by users with low vision, color blindness, or in challenging viewing conditions (sunlight, low-quality screens). WCAG 2.1 Success Criterion 1.4.3 (Contrast - Minimum) is one of the most violated rules in production, and is a frequent interview question for senior engineers.

Beyond minimum contrast, accessibility requires that **color is never the only means of conveying information** (SC 1.4.1). Error states, required fields, and chart legends must use icons, text, or patterns in addition to color.

## Why Do We Need It?

1. **Legal compliance**: WCAG 1.4.3 is required for ADA, Section 508, and EAA conformance at AA level
2. **8% of men, 0.5% of women** have some form of color vision deficiency (CVD)
3. **Low vision affects 1 in 30 people**; many more need reading glasses by age 50
4. **Outdoor and bright sun** reduces perceived contrast — designs that pass in office may fail outdoors
5. **High-contrast mode** (Windows, macOS) overrides author styles — design must degrade gracefully
6. **Cognitive accessibility**: poor contrast increases reading load for everyone

## WCAG Contrast Requirements

| Level | Normal Text | Large Text | UI Components |
|-------|-------------|------------|---------------|
| **AA** | 4.5:1 | 3:1 | 3:1 (1.4.11) |
| **AAA** | 7:1 | 4.5:1 | — |

- **Normal text**: < 18pt, or < 14pt bold
- **Large text**: ≥ 18pt, or ≥ 14pt bold
- **UI components**: icons, form borders, focus indicators

## How It Works

### The Contrast Formula

```text
Contrast ratio = (L1 + 0.05) / (L2 + 0.05)
  where L1 = lighter color's relative luminance
        L2 = darker color's relative luminance

Relative luminance:
  L = 0.2126 * R + 0.7152 * G + 0.0722 * B
  (R, G, B are linearized sRGB values, 0-1)

Examples:
  White (#FFF) on Black (#000) = 21:1
  Black on White                = 21:1
  Gray #767676 on White         = 4.54:1 (passes AA)
  Light gray #999 on White      = 2.85:1 (fails AA)
```

### Code: Calculate Contrast Ratio

```typescript
function relativeLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  const [r, g, b] = [rgb.r, rgb.g, rgb.b].map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(fg: string, bg: string): number {
  const l1 = Math.max(relativeLuminance(fg), relativeLuminance(bg));
  const l2 = Math.min(relativeLuminance(fg), relativeLuminance(bg));
  return (l1 + 0.05) / (l2 + 0.05);
}

function passes(fg: string, bg: string, level: 'AA' | 'AAA' = 'AA', large = false): boolean {
  const ratio = contrastRatio(fg, bg);
  if (level === 'AAA') return large ? ratio >= 4.5 : ratio >= 7;
  return large ? ratio >= 3 : ratio >= 4.5;
}
```

## Code Examples

### Accessible Color Palette

```css
:root {
  /* Primary text */
  --text-primary: #1a1a1a;     /* 16.10:1 on white — AAA */
  --text-secondary: #595959;   /* 7.00:1 on white — AAA */
  --text-tertiary: #767676;    /* 4.54:1 on white — AA (normal text) */

  /* Brand colors with AA contrast on white */
  --brand-primary: #1e40af;    /* 8.59:1 — AAA */
  --brand-accent: #b91c1c;     /* 6.39:1 — AA (large/normal) */

  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;     /* 1.06:1 vs text-primary, OK for surfaces */

  /* Focus indicator: 3:1 against adjacent colors (1.4.11) */
  --focus-ring: #2563eb;       /* 5.94:1 on white */
}
```

### Error State with Color + Icon + Text

```html
<!-- ❌ Bad: only red color signals error -->
<input class="error" type="text" />

<!-- ✅ Good: color + icon + text label -->
<label for="email">Email</label>
<div class="field">
  <input
    id="email"
    type="email"
    aria-invalid="true"
    aria-describedby="email-error"
  />
  <span class="error-icon" aria-hidden="true">⚠</span>
</div>
<p id="email-error" class="error-text">
  Please enter a valid email address
</p>
```

```css
/* Color + icon + text — accessible to all CVD users */
.field {
  display: flex;
  align-items: center;
}
.field input[aria-invalid="true"] {
  border: 2px solid #b91c1c;  /* 6.39:1 contrast */
}
.error-icon {
  color: #b91c1c;
  margin-left: 0.5rem;
}
.error-text {
  color: #b91c1c;
  font-weight: 600;
  /* Plus: pattern in icon, text in error message */
}
```

### Chart with Accessible Patterns

```typescript
// Use line dash patterns, not just colors, for chart series
const lineStyles = {
  'Revenue': { color: '#1e40af', dash: 'solid' },
  'Profit':  { color: '#b91c1c', dash: 'dashed' },
  'Costs':   { color: '#15803d', dash: 'dotted' },
};

// In chart legend, show both color AND pattern:
// [━━━━ Revenue] [-- -- Profit] [···· Costs]
```

### High-Contrast Mode Compatibility

```css
/* Windows High Contrast Mode (forced-colors) */
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;     /* system color, not hardcoded */
    background: ButtonFace;
    color: ButtonText;
    /* forced-colors: preserve parent or use system colors */
  }
  .button:focus {
    outline: 2px solid Highlight;     /* system focus color */
    outline-offset: 2px;
  }
}
```

## Real-World Use Cases

### 1. Design System Token Audit

```typescript
// Token audit script
import { contrastRatio } from './color-utils';

const tokens = [
  { name: 'text-primary', fg: '#1a1a1a', bg: '#ffffff' },
  { name: 'text-secondary', fg: '#595959', bg: '#ffffff' },
  { name: 'link-default', fg: '#1e40af', bg: '#ffffff' },
];

tokens.forEach((t) => {
  const ratio = contrastRatio(t.fg, t.bg);
  const passes = ratio >= 4.5 ? '✅' : '❌';
  console.log(`${passes} ${t.name}: ${ratio.toFixed(2)}:1`);
});
```

### 2. Data Visualization (Color-Blind Safe)

```typescript
// ColorBrewer / Viridis palettes are CVD-safe
const palette = {
  'series-1': '#440154',  // Viridis purple
  'series-2': '#21908d',  // Viridis teal
  'series-3': '#fde725',  // Viridis yellow
};

// Always pair color with another channel: pattern, label, position
```

### 3. Form Validation

```typescript
function validateField(field: HTMLInputElement): { valid: boolean; message: string } {
  if (field.validity.valueMissing) {
    return { valid: false, message: `${field.name} is required` };
  }
  if (field.validity.typeMismatch) {
    return { valid: false, message: `Please enter a valid ${field.type}` };
  }
  return { valid: true, message: '' };
}

// Render: icon + text + color (all three signals)
```

## Common Mistakes

### 1. Using Light Gray for Body Text

```css
/* ❌ Bad: fails AA on white */
body { color: #999; }  /* 2.85:1 */

/* ✅ Good: passes AA */
body { color: #595959; }  /* 7.00:1 */
```

### 2. Color as the Only Signal

```html
<!-- ❌ Bad: red border = error, but no text/icon for CVD users -->
<input style="border: 2px solid red" />

<!-- ✅ Good: red + icon + text -->
<input aria-invalid="true" aria-describedby="error-1" />
<span id="error-1" role="alert">Invalid email</span>
```

### 3. Forgetting Placeholder Color Contrast

Default placeholder text is often 16:1 against the input. Browsers vary:
- Chrome: #757575 (5.7:1 on white — passes AA)
- Some older browsers: lower

Always set explicit placeholder color and test.

### 4. Not Testing in High Contrast Mode

```css
/* ❌ Bad: hardcoded colors that disappear in forced-colors mode */
.thin-border { border: 1px solid #ccc; }  /* may be invisible */

/* ✅ Good: use system colors */
.thin-border { border: 1px solid CanvasText; }
```

### 5. Confusing Hover-Only State Changes

```css
/* ❌ Bad: only color change on hover */
.link:hover { color: #b91c1c; }

/* ✅ Good: color + underline + weight */
.link:hover { color: #b91c1c; text-decoration: underline; font-weight: 600; }
```

## Best Practices

1. **Test with real contrast tools** (Stark, axe DevTools, Lighthouse, Colour Contrast Analyser)
2. **Use AA as the minimum** for normal text, AAA for body text
3. **Pair color with another signal** (icon, text, pattern) for all state changes
4. **Use Viridis or ColorBrewer palettes** for data visualization
5. **Support high-contrast mode** with `forced-colors` media query
6. **Design in grayscale first** — if it works in B&W, color adds clarity not burden
7. **Audit design tokens** programmatically with `color-contrast()` or libraries
8. **Test with color blindness simulators** (Chrome DevTools > Rendering > Vision Deficiencies)
9. **Avoid pure red/green pairs** — most common CVD is red-green confusion
10. **Document color tokens** with their contrast ratios in design system docs

## Color Blindness Types

| Type | % of Population | Affected Colors |
|------|-----------------|-----------------|
| Deuteranopia (red-green) | ~6% of men | red ↔ green |
| Protanopia (red-green) | ~2% of men | red appears dark |
| Tritanopia (blue-yellow) | < 1% | blue ↔ green |
| Achromatopsia (no color) | < 0.01% | grayscale only |

## CSS `color-contrast()` Function

```css
/* Experimental: pick the best contrast color automatically */
.button {
  background: #1e40af;
  color: color-contrast(#1e40af vs #fff, #000 to AA);  /* picks white */
}

/* Currently in Chrome 100+ behind flag */
```

## Performance Considerations

- Color calculations: < 1ms per pair, trivially fast
- High-contrast mode detection via `forced-colors`: no perf cost
- Color blindness simulators: only in dev tools, zero runtime cost

## Summary

- WCAG AA requires 4.5:1 contrast for normal text, 3:1 for large text and UI
- WCAG AAA requires 7:1 contrast for normal text
- Color must never be the only signal — pair with icon, text, or pattern
- Test in high-contrast mode (`forced-colors` media query)
- Use CVD-safe palettes (Viridis, ColorBrewer) for data visualization
- Audit design tokens programmatically
- 8% of men have color vision deficiency — design accordingly

---

## Cheat Sheet
```text
COLOR & CONTRAST CHEAT SHEET
============================================================

WCAG CONTRAST (AA):
  • Normal text:  4.5:1
  • Large text:   3:1  (>= 18pt, or >= 14pt bold)
  • UI elements:  3:1  (1.4.11)

WCAG CONTRAST (AAA):
  • Normal text:  7:1
  • Large text:   4.5:1

COMMON FAILURES:
  • Light gray body text on white (#999, #aaa)
  • Placeholder text (varies by browser)
  • Disabled state (often too low)
  • Form borders
  • Hover-only state changes

NEVER USE COLOR ALONE:
  • Errors:  red border + ⚠ icon + "Required" text
  • Charts:  color + pattern + label
  • Status:  color + text label (online/offline)
  • Links:   color + underline

HIGH-CONTRAST MODE:
  @media (forced-colors: active) {
    border: 2px solid ButtonText;
  }
  Use system colors: ButtonText, ButtonFace, Highlight, Canvas

COLOR-BLINDNESS TYPES:
  • Deuteranopia (6% of men)  - red-green
  • Protanopia (2% of men)    - red appears dark
  • Tritanopia (<1%)           - blue-yellow

INTERVIEW TIPS:
  • Quote the 4.5:1 and 3:1 ratios from memory
  • Explain why color can't be the only signal
  • Discuss forced-colors media query
  • Mention real tools: Stark, axe, Lighthouse
```
---

## See Also
- [ARIA](02-ARIA.md)
- [Keyboard Navigation](03-Keyboard-Navigation.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [Testing](../16-Testing/)
- [Testing Accessibility](04-Testing-A11y.md)
- [WCAG Overview](01-WCAG-Overview.md)

## References & Learn More

- [WCAG 2.1 SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Stark (Figma + Chrome plugin)](https://www.getstark.co/)
- [Colour Contrast Analyser (CCA)](https://www.tpgi.com/color-contrast-checker/)
- [ColorBrewer Palettes](https://colorbrewer2.org/)
- [Viridis Colormap](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html)
- [A11y Project - Color](https://www.a11yproject.com/about/#color-and-contrast)
