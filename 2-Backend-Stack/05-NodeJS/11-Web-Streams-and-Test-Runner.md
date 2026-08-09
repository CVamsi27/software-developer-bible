---
section: Node.js
category: Backend
tags: [concept]
---

# Web Streams and the Node.js Test Runner

## TL;DR

**Web Streams** (`ReadableStream`, `WritableStream`, `TransformStream`) are the WHATWG-standard stream API, supported in Node.js 18+ as a global. They are the modern alternative to Node's legacy `stream` module for browser-compatible code, Fetch API, and cross-runtime (Node + Deno + Workers). **The Node.js Test Runner** (`node:test`) is the built-in test framework, zero dependencies, supports TAP, parallel execution, mocking, and `node --test` CLI. Both are the modern primitives for senior-level Node work.

## Why It Matters

Senior Node.js engineers know the Web Streams API is the future: it works in browsers, Cloudflare Workers, Deno, and Node — making code portable. The built-in test runner (`node:test`) eliminates the Jest dependency for many projects, ships zero deps, and integrates with `node --watch` for fast feedback. These are the modern defaults; legacy `stream` and `jest` are still common but no longer the recommendation for greenfield work.

## Definition

**Web Streams** are the standard stream API defined by the WHATWG Streams Standard, with `ReadableStream`, `WritableStream`, and `TransformStream` as the core classes. They use promise-based backpressure and are supported in all modern runtimes.

**The Node.js Test Runner** (`node:test`) is a built-in test module that provides `describe`, `it`, `test`, `before/after`, mocking, and TAP output, runnable via `node --test`.

## Why Do We Need It?

1. **Portability** — Web Streams work in Node, Deno, browsers, and edge runtimes (Cloudflare Workers, Vercel Edge)
2. **Promise-based backpressure** — Cleaner async/await integration than Node's event-based streams
3. **Built-in test runner** — No dependency, no `jest.config.js`, no `babel-jest`, no `ts-jest` configuration
4. **Watch mode** — `node --test --watch` for fast feedback
5. **Native TypeScript** — Node 22+ supports running `.ts` files directly with `--experimental-strip-types`

## How It Works

### Web Streams: Readable

```typescript
// Create a ReadableStream from an async iterator
function createReadableStream<T>(source: AsyncIterable<T>): ReadableStream<T> {
  const iterator = source[Symbol.asyncIterator]();
  return new ReadableStream<T>({
    async pull(controller) {
      const { done, value } = await iterator.next();
      if (done) controller.close();
      else controller.enqueue(value);
    },
  });
}

// Use it
const stream = createReadableStream(async function* () {
  for (let i = 0; i < 10; i++) yield i;
}());

// Read with for-await
for await (const chunk of stream) {
  console.log(chunk);
}

// Or pipe to a WritableStream
const writable = new WritableStream({
  write(chunk) { console.log('wrote', chunk); },
});
await stream.pipeTo(writable);
```

### Web Streams: Writable

```typescript
const writable = new WritableStream<string>({
  write(chunk) {
    console.log('received:', chunk);
  },
  close() {
    console.log('stream closed');
  },
});

const writer = writable.getWriter();
await writer.write('hello');
await writer.write('world');
await writer.close();
```

### Web Streams: Transform

```typescript
const upperCaseTransform = new TransformStream<string, string>({
  transform(chunk, controller) {
    controller.enqueue(chunk.toUpperCase());
  },
});

// Pipe: readable → transform → writable
await readableStream
  .pipeThrough(upperCaseTransform)
  .pipeTo(writableStream);
```

### Web Streams: Fetch API Integration

```typescript
// Fetch response body is a ReadableStream
const response = await fetch('https://api.example.com/large-file');
const reader = response.body!.getReader();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // process Uint8Array chunk
  process.stdout.write(Buffer.from(value).toString());
}
```

### Web Streams: HTTP Server Integration

```typescript
import { createServer } from 'node:http';

const server = createServer(async (req, res) => {
  if (req.url === '/stream') {
    // Convert Node IncomingMessage stream to Web ReadableStream
    const webStream = ReadableStream.from(req);
    const transformed = webStream.pipeThrough(
      new TransformStream({
        transform(chunk: Uint8Array, controller) {
          controller.enqueue(new Uint8Array(chunk).map(b => b + 1)); // Caesar cipher
        },
      })
    );
    // Convert back to Node stream to write the response
    const nodeStream = ReadableStream.toNodeStream(transformed);
    res.writeHead(200);
    nodeStream.pipe(res);
  }
});
```

### The Node.js Test Runner: Basic Test

```typescript
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

describe('Math utilities', () => {
  test('adds two numbers', () => {
    assert.equal(2 + 2, 4);
  });

  test('async test', async () => {
    const result = await asyncOperation();
    assert.deepEqual(result, { status: 'ok' });
  });

  test('throws on invalid input', () => {
    assert.throws(() => divide(1, 0), /division by zero/);
  });
});
```

### The Node.js Test Runner: Mocking

```typescript
import { test, mock } from 'node:test';
import assert from 'node:assert/strict';

// Mock a function
const fetchUser = mock.fn(async (id: string) => ({ id, name: 'Test' }));

test('fetches user with retry', async () => {
  // Use the mock
  const user = await fetchUser('123');
  assert.equal(user.name, 'Test');
  assert.equal(fetchUser.mock.calls.length, 1);
});

// Mock a module
mock.module('./db', {
  namedExports: {
    query: mock.fn(async (sql) => [{ id: 1 }]),
  },
});
```

### The Node.js Test Runner: Setup and Teardown

```typescript
import { test, before, after, beforeEach, afterEach } from 'node:test';

let db: Database;
before(async () => {
  db = await Database.connect(process.env.TEST_DATABASE_URL!);
});

after(async () => {
  await db.disconnect();
});

beforeEach(async () => {
  await db.migrate();
});

afterEach(async () => {
  await db.truncateAll();
});

test('creates a user', async () => {
  const user = await db.users.create({ name: 'Alice' });
  assert.ok(user.id);
});
```

### The Node.js Test Runner: Running Tests

```bash
# Run all tests in test/ directory
node --test

# Watch mode
node --test --watch

# Specific file
node --test test/math.test.ts

# With coverage (Node 22+)
node --test --experimental-test-coverage

# TAP output for CI
node --test --test-reporter=tap

# Run tests in parallel (each file is a separate process by default)
node --test --test-concurrency=4
```

## Code Examples

### Real-World: Streaming API Response

```typescript
import { ReadableStream } from 'node:stream/web';

async function streamDatabaseRows<T>(
  query: AsyncIterable<T>
): Promise<ReadableStream<T>> {
  return ReadableStream.from(query);
}

// Use in a route handler
app.get('/api/export', async (req, res) => {
  const rows = db.prepare('SELECT * FROM users').iterate();
  const stream = await streamDatabaseRows(rows);

  res.setHeader('Content-Type', 'application/x-ndjson');
  for await (const row of stream) {
    res.write(JSON.stringify(row) + '\n');
  }
  res.end();
});
```

### Real-World: Integration Test with Test Runner

```typescript
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { request } from 'undici';

let server: ReturnType<typeof createServer>;
let baseUrl: string;

before(async () => {
  server = createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const port = (server.address() as any).port;
  baseUrl = `http://localhost:${port}`;
});

after(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

test('GET /api/users returns paginated users', async () => {
  const { statusCode, body } = await request(`${baseUrl}/api/users?page=1`);
  assert.equal(statusCode, 200);
  const users = await body.json();
  assert.ok(Array.isArray(users));
});
```

### Real-World: Backing Up Files with Web Streams

```typescript
import { createReadStream, createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { createGzip } from 'node:zlib';
import { Readable } from 'node:stream';

// Mix Node streams and Web streams
async function backupFile(src: string, dest: string) {
  const nodeStream = createReadStream(src);
  // Convert Node stream to Web stream
  const webStream = Readable.toWeb(nodeStream) as ReadableStream<Uint8Array>;
  // Transform: gzip
  const gzip = new CompressionStream('gzip');
  const compressed = webStream.pipeThrough(gzip);
  // Write to disk using Node stream
  await pipeline(
    Readable.fromWeb(compressed as any),
    createWriteStream(dest)
  );
}
```

## Real-World Use Cases

1. **Cross-runtime libraries** — Use Web Streams for code that runs in Node + Cloudflare Workers + Deno
2. **Fetch API body handling** — Process large response bodies without loading them all into memory
3. **NDJSON streaming APIs** — Stream database rows or log lines to the client
4. **Built-in testing** — Use `node:test` for libraries and apps to avoid Jest/Vitest setup overhead
5. **Edge functions** — Web Streams are the only stream API in V8 isolates
6. **Compression pipelines** — `CompressionStream` (gzip, deflate, brotli) as a `TransformStream`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `Response.json()` for huge payloads | Stream the response with a `ReadableStream` |
| Loading large files into memory with `readFile` | Use `createReadStream` (Node) or `ReadableStream` (Web) |
| Treating Web Streams like Node streams (`.on('data')`) | Web Streams use promise-based `getReader()` or `pipeTo` |
| Installing Jest when `node:test` is enough | Default to `node:test` for new projects; use Vitest only if you need its features |
| Using `node --test` without `--watch` for TDD | Use `node --test --watch` for instant feedback |
| Mocking with third-party libraries (sinon) | Use `mock.fn` and `mock.module` from `node:test` |
| Forgetting `--test-concurrency` for slow test suites | Default is sequential; parallelize for speed |
| Using `Readable.fromWeb` / `Readable.toWeb` incorrectly | These are the conversion utilities; check direction (Web → Node vs. Node → Web) |

## Best Practices

1. **Default to Web Streams for new code** — Especially if you might run on the edge or in workers
2. **Use `ReadableStream.from(asyncIterable)` for easy conversion** — From any async iterable to a Web stream
3. **Use `for await` for consumption** — Works with both Node and Web streams
4. **Use `pipeline()` for Node stream composition** — Handles errors and cleanup; Web Streams use `pipeTo`
5. **Default to `node:test` for new projects** — Zero deps, fast, built-in
6. **Use `node --test --watch` during development** — Instant feedback without external tools
7. **Use `node --test --test-reporter=tap` in CI** — TAP output integrates with most CI systems
8. **Use `mock.module` for module mocking** — Not third-party libraries
9. **Run tests in parallel by default** — Each test file is a separate process
10. **Use subtests for hierarchical test organization** — `test('parent', async (t) => { await t.test('child', ...); })`

## Performance Considerations

| Aspect | Web Streams | Node Streams |
|--------|-------------|--------------|
| Backpressure | Promise-based, automatic | Event-based (`drain`, `pause`/`resume`) |
| Bundle size | Smaller (no polyfill needed in modern runtimes) | Larger (Node-specific module) |
| Edge runtime | Native | Not supported |
| Browser | Native | Requires polyfill or Node polyfill bundle |
| Throughput | Comparable | Comparable |
| Type safety | TS types are Promise-based | TS types are event-based (older API style) |
| Test runner startup | `node --test` is ~50ms cold start | Jest is ~500-1500ms cold start |

**Heuristic:**
- New code that might run on the edge? → Web Streams
- New code that needs to interop with Node-only APIs? → Node Streams
- Mixing? → Use the `Readable.toWeb` / `Readable.fromWeb` converters
- Greenfield project? → `node:test`, not Jest
- Need snapshot testing, complex mocking, or extensive plugin ecosystem? → Vitest

## Summary

Web Streams are the modern, cross-runtime stream API; the Node.js Test Runner is the modern, zero-dep test framework. Both are stable, built-in, and the recommendation for greenfield work. Senior engineers reach for them by default and only fall back to legacy `stream` and Jest when a specific feature requires it. `node --test --watch` is the new TDD loop; `ReadableStream` is the new way to handle streaming data.

## Cheat Sheet

| API | Web Streams | Node.js Test Runner |
|-----|-------------|---------------------|
| Read | `ReadableStream` | `stream.Readable` |
| Write | `WritableStream` | `stream.Writable` |
| Transform | `TransformStream` | `stream.Transform` |
| Consume | `for await (const x of stream)` | `stream.on('data', ...)` |
| Backpressure | Promise (automatic) | `drain` / `pause` / `resume` |
| Convert | `Readable.toWeb` / `Readable.fromWeb` | `Readable.toWeb` / `Readable.fromWeb` |
| Test | `import { test } from 'node:test'` | `import { test } from 'jest'` |
| Run | `node --test` | `jest` |
| Watch | `node --test --watch` | `jest --watch` |
| Mock | `mock.fn` / `mock.module` | `jest.fn` / `jest.mock` |
| Coverage | `node --test --experimental-test-coverage` | `jest --coverage` |

---

## See Also
- [Event Loop](01-Event-Loop.md)
- [File System](05-File-System.md)
- [HTTP Module](06-HTTP-Module.md)
- [Process & Environment](08-Process-Environment.md)
- [Streams](02-Streams.md)

## References & Learn More

- [WHATWG Streams Standard](https://streams.spec.whatwg.org/)
- [MDN: Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
- [Node.js: Web Streams API](https://nodejs.org/api/stream_web.html)
- [Node.js: Test Runner](https://nodejs.org/api/test.html)
- [Node.js: node:test documentation](https://nodejs.org/api/test.html)
- [Web Streams Everywhere (Blog)](https://web.dev/articles/streams)
