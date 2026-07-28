---
section: Testing
category: Quality
tags: [concept]
---

# Vitest

## Definition

**Vitest** is a blazing-fast unit test framework powered by Vite. It's designed as a drop-in replacement for Jest with native ESM support, instant hot-module reload, and built-in TypeScript/JSX handling. Vitest shares the same Vite config and transform pipeline, eliminating configuration duplication.

## Why Do We Need It?

1. **Speed**: Native ESM, no bundling step — tests run 2-10x faster than Jest
2. **Vite integration**: Shares Vite config, plugins, and transforms with your app
3. **Jest-compatible API**: `describe`, `it`, `expect`, mocks — familiar syntax
4. **ESM native**: No experimental warnings or workarounds for ES modules
5. **HMR for tests**: Like Vite dev server — instant test feedback on save

## Code Examples

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Basic test
describe('Math operations', () => {
  it('should add numbers', () => {
    expect(1 + 2).toBe(3);
  });

  it('should handle async', async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });
});
```

## Vitest vs Jest

| Feature | Vitest | Jest |
|---------|:------:|:----:|
| Native ESM | ✅ | ❌ |
| HMR | ✅ | ❌ |
| TypeScript (built-in) | ✅ | ❌ (ts-jest) |
| Speed | 2-10x faster | Baseline |
| Vite integration | Native | ❌ |
| Worker threads | ✅ (default) | ⚠️ (experimental) |
| Snapshot | ✅ | ✅ |

---

### See Also

- [Interview Questions](09-Interview-Questions.md)
- [Jest](02-Jest.md)
- [React Testing Library](03-React-Testing-Library.md)
- [Testing Overview](01-Testing-Overview.md)
- [Vite](../23-Build-Tools/02-Vite.md)

## References & Learn More

- [Vitest Documentation](https://vitest.dev/)
- [Vitest Config Reference](https://vitest.dev/config/)
