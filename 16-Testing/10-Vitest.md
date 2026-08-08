---
section: Testing
category: Quality
tags: [concept, reference]
---

# Vitest

## Definition

**Vitest** is a Vite-native unit-test framework designed as a drop-in replacement for Jest. It reuses Vite's transform pipeline (esbuild + Rollup) and dependency graph, so tests run with **native ESM**, no Babel/ts-jest hop, and instant HMR. The API surface mirrors Jest (`describe`/`it`/`expect`/`vi`) so existing tests migrate with minimal changes, while adding features Jest lacks: built-in watch-mode filtering, type-aware assertions (`expectTypeOf`), in-source testing, and worker-thread parallelism by default.

## TL;DR

Vitest trades Jest's decade of maturity for **raw speed** (typically 2-10x faster on cold start) and **zero-config ESM + TS**. It runs each test file in a **worker thread** by default — true parallelism, not Jest's process fork with the same transpiler cost. The trade-off: the ecosystem is younger, and complex Jest plugins (e.g., custom `testEnvironment` shims) don't always have Vitest equivalents. For greenfield Vite/Vue/React/Next projects, Vitest is the default in 2025+; for legacy CRA or ts-jest-heavy codebases, Jest still wins on stability.

## Why it matters

Senior interviews increasingly ask "**why did you pick Jest vs. Vitest?**" — and the honest answer is rarely "because the docs said so." Strong answers cover: cold-start latency in CI (Vitest's esbuild transform vs. ts-jest), HMR-style test re-runs during dev, native ESM (no `"type": "module"` workarounds), and the migration ergonomics (`jest.fn` → `vi.fn`, `jest.mock` → `vi.mock`). You should also know Vitest's **sharp edges**: fake-timer semantics differ slightly, `vi.mock` hoisting has its own gotchas, and snapshot serialization can drift between versions.

## Why Do We Need It?

- **Speed**: Native ESM, no bundling step — tests run 2-10x faster than Jest
- **Vite integration**: Shares Vite config, plugins, and transforms with your app
- **Jest-compatible API**: `describe`, `it`, `expect`, mocks — familiar syntax
- **ESM native**: No experimental warnings or workarounds for ES modules
- **HMR for tests**: Like Vite dev server — instant test feedback on save
- **TypeScript built-in**: `tsconfig` paths, JSX, and decorators work out of the box
- **Worker threads by default**: True parallelism, not Jest's fork-per-test
- **In-source testing**: Co-locate tests with the code under test for utilities

## How It Works

```text
┌─────────────────────────────────────────────────────────────┐
│                      Vitest Test Runner                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │   Vite       │   │  Test API    │   │  Reporter    │    │
│  │  Transform   │   │  (Jest-like) │   │  (CLI/HTML)  │    │
│  │  (esbuild)   │   │              │   │              │    │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘    │
│         │                  │                  │             │
│         └────────┬─────────┴────────┬─────────┘             │
│                  ▼                  ▼                        │
│         ┌────────────────────────────────┐                 │
│         │      Worker Thread Pool          │                 │
│         │  ┌──────┐  ┌──────┐  ┌──────┐   │                 │
│         │  │ W1   │  │ W2   │  │ W3   │   │                 │
│         │  │ 8GB  │  │ 8GB  │  │ 8GB  │   │                 │
│         │  │ ctx  │  │ ctx  │  │ ctx  │   │                 │
│         │  └──────┘  └──────┘  └──────┘   │                 │
│         └────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

- **No Babel/ts-jest hop**: Vite's esbuild transform runs at request time, so a 1,000-test suite starts in ~1s instead of ~15s.
- **Native ESM**: `import.meta.url`, top-level `await`, and bare specifiers work without `--experimental-vm-modules`.
- **Isolated worker contexts**: Each test file runs in a fresh `vm` context inside its own worker — no module-cache leak between files.
- **Watch mode with HMR**: When you save a file, Vite invalidates only the modules that depend on it and re-runs the affected tests.

## Code Examples

### Basic Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,                 // inject describe/it/expect globally (Jest-style)
    environment: "jsdom",          // or "node" / "happy-dom"
    setupFiles: ["./vitest.setup.ts"],
    coverage: {
      provider: "v8",              // V8 native coverage — much faster than istanbul
      reporter: ["text", "html", "lcov"],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },
    isolate: true,                 // per-file VM context isolation
    pool: "threads",               // "forks" or "vmThreads" also valid
    poolOptions: { threads: { singleThread: false } },
  },
  resolve: {
    alias: { "@": resolve(__dirname, "src") },
  },
});
```

### Test File with Mocks, Spies, and Fake Timers

```typescript
// userService.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { UserService } from "./userService";
import * as api from "./api";

// Module-level mock — hoisted automatically
vi.mock("./api", () => ({
  fetchUser: vi.fn(),
  sendEmail: vi.fn(),
}));

const mockedApi = vi.mocked(api);

describe("UserService", () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers(); // restore real timers if any test faked them
  });

  it("should return welcome message with user name", async () => {
    mockedApi.fetchUser.mockResolvedValue({
      id: "1",
      name: "John",
      email: "john@example.com",
    });

    const result = await service.getUserWelcomeEmail("1");

    expect(result).toBe("Welcome, John!");
    expect(mockedApi.fetchUser).toHaveBeenCalledWith("1");
    expect(mockedApi.fetchUser).toHaveBeenCalledTimes(1);
  });

  it("should propagate network errors", async () => {
    mockedApi.fetchUser.mockRejectedValue(new Error("Network error"));
    await expect(service.getUserWelcomeEmail("1")).rejects.toThrow("Network error");
  });

  it("should retry once on 503 with fake timers", async () => {
    vi.useFakeTimers();
    mockedApi.fetchUser
      .mockRejectedValueOnce({ status: 503 })
      .mockResolvedValueOnce({ id: "1", name: "John", email: "j@x.com" });

    const promise = service.getUserWithRetry("1");
    await vi.runAllTimersAsync();
    const result = await promise;

    expect(result.name).toBe("John");
    expect(mockedApi.fetchUser).toHaveBeenCalledTimes(2);
  });
});
```

### Snapshot Testing with Custom Serializers

```typescript
// component.test.tsx
import { render } from "@testing-library/react";
import { expect, it } from "vitest";
import { UserCard } from "./UserCard";

it("renders user card consistently", () => {
  const { container } = render(
    <UserCard name="John Doe" email="john@example.com" role="admin" />
  );
  // Inline snapshot — auto-updated on save with --update
  expect(container).toMatchInlineSnapshot(`
    <div>
      <div class="user-card">
        <h3>John Doe</h3>
        <p>john@example.com</p>
        <span class="badge admin">admin</span>
      </div>
    </div>
  `);
});
```

### Mocking the Fetch API with MSW (Real-Network Mocks)

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users/:id", ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: "John Doe",
      email: "john@example.com",
    });
  }),
  http.post("/api/users", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: "new-id", ...body }, { status: 201 });
  }),
];
```

```typescript
// vitest.setup.ts
import { afterAll, afterEach, beforeAll } from "vitest";
import { setupServer } from "msw/node";
import { handlers } from "./mocks/handlers";

export const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

MSW intercepts the **real `fetch`/`axios`** calls your app makes — no `vi.mock("./api")` shim needed. The tests exercise the actual HTTP serialization path, so a missing header or wrong content-type would be caught.

## Real-World Use Cases

### 1. Vite-Powered React SPA

Vitest is the **default test runner** for new Vite + React + TypeScript apps. Cold start of 1,500 tests drops from ~45s (Jest + ts-jest) to ~6s. Watch mode re-runs only the affected file's test in <300ms because Vite's module graph invalidates incrementally.

### 2. Monorepo with Shared Config

```typescript
// packages/test-config/vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    setupFiles: ["./global-setup.ts"],
    coverage: { provider: "v8" },
  },
});
```

Each package extends this base. New packages inherit a consistent test runtime, and CI can shard via `--shard=1/4` for parallel runs.

### 3. Node.js Library Testing

For a library that targets Node, Vitest's `environment: "node"` and built-in TypeScript support remove the need for `ts-node` or `tsx` to bootstrap tests. Pair with `pool: "forks"` if your library spawns subprocesses — `threads` pool shares memory and can break `child_process` isolation.

### 4. Next.js Component Testing (App Router)

```typescript
// app/components/Button.test.tsx
import { render, screen } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import { Button } from "./Button";

it("calls onClick when clicked", async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Save</Button>);
  await userEvent.click(screen.getByRole("button", { name: /save/i }));
  expect(onClick).toHaveBeenCalledOnce();
});
```

For Next.js App Router server components, Vitest can run them with `environment: "happy-dom"` + `@vitejs/plugin-react` — but you'll want a separate setup for testing the `async` server component behavior (fetch, cookies, headers) using `unstable_cache` mocks.

## Common Mistakes

### 1. Assuming Jest Mocks Work Identically

```typescript
// ❌ BAD: jest.fn() doesn't exist in Vitest
const handler = jest.fn();

// ✅ GOOD: use vi.fn()
const handler = vi.fn();
```

`jest` global is not available by default. Either import from `vitest` or enable `globals: true` in config. Same for `jest.mock` → `vi.mock`, `jest.spyOn` → `vi.spyOn`, `jest.useFakeTimers` → `vi.useFakeTimers`.

### 2. Forgetting to Restore Timers

```typescript
// ❌ BAD: fake timers leak to other tests
it("test A", () => {
  vi.useFakeTimers();
  // ...uses fake timers...
});
it("test B", () => {
  // this test runs with fake timers still active
  setTimeout(() => {}, 1000); // never fires
});

// ✅ GOOD: restore in afterEach
afterEach(() => {
  vi.useRealTimers();
});
```

### 3. Mixing ESM and CJS in the Same Suite

```typescript
// ❌ BAD: CommonJS module dragged into an ESM test
// module.exports = { helper };  // legacy CJS
// import { helper } from "./legacy";  // works but breaks tree-shaking

// ✅ GOOD: convert legacy CJS to ESM, or isolate via dynamic import
const { helper } = await import("./legacy");
```

Mixing causes Vitest to fall back to slower transform paths.

### 4. Using `pool: "threads"` for Code That Spawns Subprocesses

```typescript
// ❌ BAD: tests share the same process — child_process leaks across tests
test("spawns worker", () => spawn("node", ["worker.js"]));

// ✅ GOOD: use "forks" pool for true process isolation
// vitest.config.ts
test: { pool: "forks" }
```

## Best Practices

1. **Use `vi.mocked()` for typed mocks** — gives you full TypeScript inference on the mock, no `as any` needed.
2. **Prefer MSW over `vi.mock` for HTTP** — MSW intercepts at the network layer, so your code uses the real `fetch`/`axios`.
3. **Run E2E in Playwright, not Vitest** — Vitest excels at unit + component, but lacks a real browser engine.
4. **Shard in CI**: `vitest run --shard=1/4 --reporter=junit` to parallelize across 4 CI containers.
5. **Enable `isolate: true`** (default) for production-like test isolation; disable only for trusted internal test suites to gain speed.
6. **Set coverage thresholds on V8 provider** — it's significantly faster than `istanbul` and accurate for V8/Node code.
7. **Use `toMatchInlineSnapshot`** instead of `.snap` files for small, changeable outputs (less noise in diffs).
8. **Co-locate test data builders** — instead of fixtures in `__fixtures__`, use factory functions so each test owns its inputs.

## Performance Considerations

- **Cold start**: Vitest typically warms up 5-15s faster than Jest for a 1,000-test suite. The win compounds in CI.
- **Watch mode**: HMR-style invalidation re-runs only affected tests, typically <500ms for a single file change.
- **Worker pool sizing**: Default is `os.cpus().length - 1`. On memory-constrained CI, reduce to avoid OOM; on beefy runners, increase.
- **V8 vs. istanbul coverage**: V8 is ~3-5x faster, but doesn't instrument untaken branches. For libraries, prefer istanbul for accuracy.
- **Large snapshots**: Snapshots >1MB slow serialization. Use inline snapshots or split tests.

## Summary

- Vitest is a Vite-native, ESM-first test runner with a Jest-compatible API and 2-10x speed gains on cold start
- Uses Vite's esbuild transform, native ESM, and worker-thread parallelism — no Babel/ts-jest hop
- Drop-in for Jest in most projects: `jest.fn` → `vi.fn`, `jest.mock` → `vi.mock`, `jest.spyOn` → `vi.spyOn`
- Best paired with MSW for HTTP mocking and `@testing-library/react` for component tests
- Watch mode with HMR-style invalidation re-runs only affected tests in <500ms
- Use `pool: "forks"` if your code spawns subprocesses; default `threads` is faster but shares memory
- V8 coverage provider is significantly faster than istanbul; use istanbul for library-grade branch coverage
- Shard in CI (`--shard=1/4`) for parallel runs across multiple containers

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Coding Patterns](../19-Coding-Patterns/)
- [E2E Testing](06-E2E-Testing.md)
- [Integration Testing](05-Integration-Testing.md)
- [Jest](02-Jest.md)
- [Mocking](07-Mocking.md)
- [React](../03-React/)
- [Unit Testing](04-Unit-Testing.md)

## References & Learn More

- [Vitest Documentation](https://vitest.dev/)
- [Vitest Config Reference](https://vitest.dev/config/)
- [Why Vitest is Faster than Jest](https://vitest.dev/guide/why.html)
- [Migration from Jest](https://vitest.dev/guide/migration.html)
- [MSW — Mock Service Worker](https://mswjs.io/)
- [V8 Native Code Coverage](https://v8.dev/blog/javascript-code-coverage)
